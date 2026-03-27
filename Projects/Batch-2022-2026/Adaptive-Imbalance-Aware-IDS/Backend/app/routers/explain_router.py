"""
Explainability and drift API.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.ml.explainability import explain_alert, get_global_feature_importance
from app.services.drift import compute_drift, get_drift_history

router = APIRouter(tags=["explainability"])


class ExplainFlowBody(BaseModel):
    src_ip: str = "0.0.0.0"
    dst_ip: str = "0.0.0.0"
    src_port: int = 0
    dst_port: int = 0
    protocol: str = "TCP"
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0


@router.get("/api/explain/global")
def global_importance():
    """Global feature importance from the loaded model."""
    imp = get_global_feature_importance()
    if imp is None:
        raise HTTPException(status_code=503, detail="No model loaded")
    return imp


@router.post("/api/explain/alert/{alert_id}")
def explain_alert_by_id(alert_id: int, db: Session = Depends(get_db)):
    """Explain a stored alert by ID (fetch flow from alert, then explain)."""
    from app.models import AlertDB
    row = db.query(AlertDB).filter(AlertDB.id == alert_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Alert not found")
    flow_dict = {
        "src_ip": row.src_ip,
        "dst_ip": row.dst_ip,
        "src_port": row.src_port,
        "dst_port": row.dst_port,
        "protocol": row.protocol,
        "bytes_sent": 0,
        "bytes_received": 0,
        "packets_sent": 0,
        "packets_received": 0,
    }
    return explain_alert(flow_dict)


@router.post("/api/explain/flow")
def explain_flow(body: ExplainFlowBody):
    """Explain a flow (feature values + importance + prediction)."""
    return explain_alert(body.model_dump())


@router.get("/api/drift")
def drift_status(db: Session = Depends(get_db)):
    """Current drift metrics (recent vs baseline)."""
    return compute_drift(db=db)


@router.get("/api/drift/history")
def drift_history(db: Session = Depends(get_db), limit: int = 100):
    """Historical drift snapshots."""
    return get_drift_history(db, limit=limit)
