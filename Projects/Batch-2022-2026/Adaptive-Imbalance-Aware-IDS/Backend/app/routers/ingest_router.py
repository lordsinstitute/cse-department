"""
PCAP upload and batch flow ingestion.
"""

import io
import tempfile
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.logging import get_logger
from app.core.validation import validate_flow_input
from app.data.pcap_ingest import flows_from_pcap
from app.data.features import flow_to_features
from app.services.drift import push_recent
from app.ws_manager import manager

logger = get_logger(__name__)

router = APIRouter(tags=["ingest"])


class FlowInBatch(BaseModel):
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str = "TCP"
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0


def _ingest_flow_and_detect(flow_dict: dict, background_tasks: BackgroundTasks):
    """Single place to enqueue flow for detection + storage + broadcast (called from main)."""
    from app.main import ingest_flow
    from app.models import FlowIn
    flow = FlowIn(**flow_dict)
    # We need to run the actual ingest (DB + broadcast) - so we call the app's ingest logic.
    # The app doesn't export a function; we'll have to duplicate or refactor.
    # Simpler: POST to internal or call score_flow + db add + broadcast.
    # For batch we'll use a shared helper. Here we just validate and return flow for the caller to process.
    return flow


@router.post("/ingest/pcap")
async def upload_pcap(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    max_flows: int = 10000,
):
    """
    Upload a PCAP file; parse flows and ingest each (detection + alert + WebSocket).
    Returns count of flows processed and any errors.
    """
    if not file.filename or not file.filename.lower().endswith((".pcap", ".pcapng", ".cap")):
        raise HTTPException(status_code=400, detail="File must be .pcap, .pcapng, or .cap")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")
    tmp = tempfile.NamedTemporaryFile(suffix=".pcap", delete=False)
    try:
        tmp.write(content)
        tmp.close()
        count = 0
        errors = []
        from app.database import SessionLocal
        from app.models import AlertDB, AlertCreate
        from app.ml.inference import score_flow
        import json

        db = SessionLocal()
        try:
            for flow_rec in flows_from_pcap(tmp.name, max_packets=max_flows * 2):
                if count >= max_flows:
                    break
                valid, err = validate_flow_input(
                    flow_rec.get("src_ip", ""),
                    flow_rec.get("dst_ip", ""),
                    flow_rec.get("src_port", 0),
                    flow_rec.get("dst_port", 0),
                    flow_rec.get("protocol", "TCP"),
                    flow_rec.get("bytes_sent", 0),
                    flow_rec.get("bytes_received", 0),
                    flow_rec.get("packets_sent", 0),
                    flow_rec.get("packets_received", 0),
                )
                if not valid:
                    errors.append(err)
                    continue
                score, severity, attack_type, summary, mitre, confidence, uncertainty = score_flow(
                    flow_rec
                )
                push_recent(flow_to_features(**{k: flow_rec.get(k) for k in [
                    "src_ip", "dst_ip", "src_port", "dst_port", "protocol",
                    "bytes_sent", "bytes_received", "packets_sent", "packets_received", "duration_sec"
                ] if k in flow_rec}))
                alert_data = AlertCreate(
                    src_ip=flow_rec["src_ip"],
                    dst_ip=flow_rec["dst_ip"],
                    src_port=flow_rec["src_port"],
                    dst_port=flow_rec["dst_port"],
                    protocol=flow_rec["protocol"],
                    attack_type=attack_type,
                    severity=severity,
                    score=score,
                    confidence=confidence,
                    uncertainty=uncertainty,
                    summary=summary,
                    mitre_techniques=mitre or [],
                )
                dump = alert_data.model_dump()
                dump["mitre_techniques"] = json.dumps(dump.get("mitre_techniques", []))
                alert_db = AlertDB(**dump)
                db.add(alert_db)
                db.commit()
                db.refresh(alert_db)
                from app.models import Alert
                alert = Alert.from_db(alert_db)
                background_tasks.add_task(manager.broadcast, {"type": "alert", "data": alert.model_dump()})
                from app.services.splunk_hec import send_alert_to_splunk
                send_alert_to_splunk(alert.model_dump())
                count += 1
        finally:
            db.close()
        return {"flows_ingested": count, "errors": errors[:20]}
    except Exception as e:
        logger.exception("PCAP ingest failed: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        Path(tmp.name).unlink(missing_ok=True)


@router.post("/ingest/flows/batch")
async def ingest_flows_batch(
    body: List[FlowInBatch],
    background_tasks: BackgroundTasks,
):
    """Ingest multiple flows in one request (e.g. from live capture or simulator)."""
    from app.database import SessionLocal
    from app.models import AlertDB, AlertCreate, Alert
    from app.ml.inference import score_flow
    import json

    results = []
    db = SessionLocal()
    try:
        for flow_in in body[:500]:  # cap at 500
            fd = flow_in.model_dump()
            valid, err = validate_flow_input(
                fd["src_ip"], fd["dst_ip"], fd["src_port"], fd["dst_port"], fd["protocol"],
                fd["bytes_sent"], fd["bytes_received"], fd["packets_sent"], fd["packets_received"],
            )
            if not valid:
                results.append({"index": len(results), "error": err})
                continue
            score, severity, attack_type, summary, mitre, confidence, uncertainty = score_flow(fd)
            push_recent(flow_to_features(
                src_ip=fd["src_ip"], dst_ip=fd["dst_ip"], src_port=fd["src_port"], dst_port=fd["dst_port"],
                protocol=fd["protocol"], bytes_sent=fd["bytes_sent"], bytes_received=fd["bytes_received"],
                packets_sent=fd["packets_sent"], packets_received=fd["packets_received"],
            ))
            alert_data = AlertCreate(
                src_ip=fd["src_ip"], dst_ip=fd["dst_ip"], src_port=fd["src_port"], dst_port=fd["dst_port"],
                protocol=fd["protocol"], attack_type=attack_type, severity=severity, score=score,
                confidence=confidence, uncertainty=uncertainty, summary=summary, mitre_techniques=mitre or [],
            )
            dump = alert_data.model_dump()
            dump["mitre_techniques"] = json.dumps(dump.get("mitre_techniques", []))
            alert_db = AlertDB(**dump)
            db.add(alert_db)
            db.commit()
            db.refresh(alert_db)
            alert = Alert.from_db(alert_db)
            results.append(alert.model_dump())
            background_tasks.add_task(manager.broadcast, {"type": "alert", "data": alert.model_dump()})
            from app.services.splunk_hec import send_alert_to_splunk
            send_alert_to_splunk(alert.model_dump())
        return {"ingested": len(results), "alerts": results}
    finally:
        db.close()
