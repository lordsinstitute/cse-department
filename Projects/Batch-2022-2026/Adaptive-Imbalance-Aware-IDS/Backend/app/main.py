"""
Real-Time NIDS Backend API.

Ingestion, detection, alerting, explainability, drift, training, and SOC dashboard.
"""

import json
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI
from app.services.splunk_hec import send_alert_to_splunk

app = FastAPI()

@app.get("/test-splunk")
def test_splunk():
    alert = {
        "type": "manual_test",
        "severity": "high",
        "message": "Splunk integration test",
        "source": "fastapi"
    }
    success = send_alert_to_splunk(alert)
    return {"sent_to_splunk": success}


from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.core.logging import get_logger, setup_logging
from app.core.validation import validate_flow_input
from app.database import Base, engine, get_db, ensure_alert_columns
from app.models import (
    Alert,
    AlertCreate,
    AlertDB,
    AnalystFeedbackDB,
    DriftSnapshotDB,
    FlowIn,
    TrainingRunDB,
    UserDB,
)
from app.ml.inference import score_flow
from app.services.alerts import deduplicate_alerts
from app.services.drift import push_recent
from app.services.splunk_hec import send_alert_to_splunk
from app.data.features import flow_to_features
from app.ws_manager import manager

# Routers
from app.routers import auth_router, feedback_router, training_router, explain_router, ingest_router

# Setup logging on load
setup_logging()
logger = get_logger(__name__)

Base.metadata.create_all(bind=engine)
ensure_alert_columns()

app = FastAPI(
    title="NIDS Backend",
    version="1.0.0",
    description="Network Intrusion Detection",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(feedback_router.router)
app.include_router(training_router.router)
app.include_router(explain_router.router)
app.include_router(ingest_router.router)


def _alert_db_to_response(alert_db: AlertDB) -> Alert:
    """Build Alert response with mitre_techniques parsed from JSON."""
    return Alert.from_db(alert_db)


@app.get("/health")
def health_check() -> dict:
    """Liveness probe."""
    return {"status": "ok"}


@app.post("/ingest/flow", response_model=Alert)
def ingest_flow(
    flow: FlowIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Alert:
    """
    Ingest a flow record, run detection (ML or rule-based), store alert, broadcast on WebSocket.
    """
    valid, err = validate_flow_input(
        flow.src_ip,
        flow.dst_ip,
        flow.src_port,
        flow.dst_port,
        flow.protocol,
        flow.bytes_sent,
        flow.bytes_received,
        flow.packets_sent,
        flow.packets_received,
    )
    if not valid:
        raise HTTPException(status_code=400, detail=err)

    score, severity, attack_type, summary, mitre_techniques, confidence, uncertainty = score_flow(flow)

    alert_data = AlertCreate(
        src_ip=flow.src_ip,
        dst_ip=flow.dst_ip,
        src_port=flow.src_port,
        dst_port=flow.dst_port,
        protocol=flow.protocol,
        attack_type=attack_type,
        severity=severity,
        score=score,
        confidence=confidence,
        uncertainty=uncertainty,
        summary=summary,
        mitre_techniques=mitre_techniques or [],
    )
    dump = alert_data.model_dump()
    dump["mitre_techniques"] = json.dumps(dump.get("mitre_techniques", []))

    alert_db = AlertDB(**dump)
    db.add(alert_db)
    db.commit()
    db.refresh(alert_db)

    push_recent(flow_to_features(
        src_ip=flow.src_ip, dst_ip=flow.dst_ip, src_port=flow.src_port, dst_port=flow.dst_port,
        protocol=flow.protocol, bytes_sent=flow.bytes_sent, bytes_received=flow.bytes_received,
        packets_sent=flow.packets_sent, packets_received=flow.packets_received,
    ))
    alert = _alert_db_to_response(alert_db)
    payload = {"type": "alert", "data": alert.model_dump()}
    background_tasks.add_task(manager.broadcast, payload)
    send_alert_to_splunk(alert.model_dump())
    return alert


@app.get("/api/alerts", response_model=List[Alert])
def list_alerts(
    db: Session = Depends(get_db),
    limit: int = Query(100, ge=1, le=1000),
    attack_type: Optional[str] = Query(None, description="Filter by attack type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    time_from: Optional[datetime] = Query(None, description="Alerts after this time (ISO)"),
    time_to: Optional[datetime] = Query(None, description="Alerts before this time (ISO)"),
    search: Optional[str] = Query(None, description="Search in src_ip or dst_ip"),
    sort: str = Query("created_at", description="Sort field: created_at, severity, score"),
    dedupe: bool = Query(False, description="Apply deduplication"),
) -> List[Alert]:
    """
    List alerts with filters (attack type, severity, time range, IP search) and sorting.
    """
    query = db.query(AlertDB)
    if attack_type:
        query = query.filter(AlertDB.attack_type == attack_type)
    if severity:
        query = query.filter(AlertDB.severity == severity)
    if time_from:
        query = query.filter(AlertDB.created_at >= time_from)
    if time_to:
        query = query.filter(AlertDB.created_at <= time_to)
    if search:
        term = f"%{search}%"
        query = query.filter(
            or_(AlertDB.src_ip.like(term), AlertDB.dst_ip.like(term))
        )
    if sort == "severity":
        order = AlertDB.severity.desc()
    elif sort == "score":
        order = AlertDB.score.desc()
    else:
        order = AlertDB.created_at.desc()
    query = query.order_by(order).limit(limit)
    results = query.all()
    out = [_alert_db_to_response(a) for a in results]
    if dedupe:
        raw = [a.model_dump() for a in out]
        raw = deduplicate_alerts(raw)
        # Rebuild Alert from dicts (they may have 'count' key)
        out = [Alert(**{k: v for k, v in r.items() if k != "count"}) for r in raw]
    return out


@app.get("/api/alerts/{alert_id}", response_model=Alert)
def get_alert(alert_id: int, db: Session = Depends(get_db)) -> Alert:
    """Get a single alert by ID."""
    alert = db.query(AlertDB).filter(AlertDB.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return _alert_db_to_response(alert)


@app.get("/api/stats")
def get_stats(
    db: Session = Depends(get_db),
    time_from: Optional[datetime] = Query(None),
    time_to: Optional[datetime] = Query(None),
) -> dict:
    """
    Statistics for dashboard: total alerts, by severity, by attack type, top source IPs.
    """
    def _filter(q):
        if time_from:
            q = q.filter(AlertDB.created_at >= time_from)
        if time_to:
            q = q.filter(AlertDB.created_at <= time_to)
        return q

    total = _filter(db.query(AlertDB)).count()
    q_sev = _filter(db.query(AlertDB.severity, func.count(AlertDB.id)))
    by_severity = q_sev.group_by(AlertDB.severity).all()

    q_at = _filter(db.query(AlertDB.attack_type, func.count(AlertDB.id)))
    by_attack_type = q_at.group_by(AlertDB.attack_type).all()

    q_ip = _filter(db.query(AlertDB.src_ip, func.count(AlertDB.id)))
    top_src_ips = q_ip.group_by(AlertDB.src_ip).order_by(func.count(AlertDB.id).desc()).limit(10).all()

    return {
        "total_alerts": total,
        "by_severity": {s: c for s, c in by_severity},
        "by_attack_type": {a: c for a, c in by_attack_type},
        "top_source_ips": [{"ip": ip, "count": c} for ip, c in top_src_ips],
    }


@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket) -> None:
    """Real-time alert stream."""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
