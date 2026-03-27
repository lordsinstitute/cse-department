"""
Analyst feedback loop: submit and list feedback for alerts.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AnalystFeedbackDB, AnalystFeedbackCreate, AnalystFeedbackResponse
from app.routers.auth_router import get_current_user_optional

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=AnalystFeedbackResponse)
def submit_feedback(
    body: AnalystFeedbackCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_optional),
):
    """Submit analyst feedback for an alert (correct label + optional comment)."""
    analyst_id = user.id if user else 0
    fb = AnalystFeedbackDB(
        alert_id=body.alert_id,
        analyst_id=analyst_id,
        correct_label=body.correct_label,
        comment=body.comment,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return AnalystFeedbackResponse(
        id=fb.id,
        alert_id=fb.alert_id,
        analyst_id=fb.analyst_id,
        correct_label=fb.correct_label,
        comment=fb.comment,
        created_at=fb.created_at,
    )


@router.get("", response_model=List[AnalystFeedbackResponse])
def list_feedback(
    db: Session = Depends(get_db),
    alert_id: Optional[int] = None,
    limit: int = 100,
):
    """List feedback entries, optionally filtered by alert_id."""
    q = db.query(AnalystFeedbackDB)
    if alert_id is not None:
        q = q.filter(AnalystFeedbackDB.alert_id == alert_id)
    rows = q.order_by(AnalystFeedbackDB.created_at.desc()).limit(limit).all()
    return [
        AnalystFeedbackResponse(
            id=r.id,
            alert_id=r.alert_id,
            analyst_id=r.analyst_id,
            correct_label=r.correct_label,
            comment=r.comment,
            created_at=r.created_at,
        )
        for r in rows
    ]
