import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from .base import Base


def _parse_mitre(raw: Optional[str]) -> List[str]:
    """Parse mitre_techniques from DB (JSON string) to list."""
    if not raw:
        return []
    try:
        out = json.loads(raw)
        return out if isinstance(out, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


class AlertDB(Base):
    """Stored alert with enrichment: confidence, MITRE, severity, uncertainty."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    src_ip = Column(String(45), index=True)
    dst_ip = Column(String(45), index=True)
    src_port = Column(Integer, index=True)
    dst_port = Column(Integer, index=True)
    protocol = Column(String(20), index=True)

    attack_type = Column(String(64), index=True)
    severity = Column(String(20), index=True)
    score = Column(Float)
    confidence = Column(Float, default=0.0)
    uncertainty = Column(Float, default=0.0)  # 1 - max(proba) or entropy
    summary = Column(String(512))
    mitre_techniques = Column(Text)  # JSON array as string


class FlowIn(BaseModel):
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str = Field(example="TCP")
    bytes_sent: int = 0
    bytes_received: int = 0
    packets_sent: int = 0
    packets_received: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class Alert(BaseModel):
    """Alert response with full context for SOC dashboard."""

    id: int
    created_at: datetime
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    attack_type: str
    severity: str
    score: float
    confidence: float = 0.0
    uncertainty: float = 0.0
    summary: str
    mitre_techniques: List[str] = []

    class Config:
        from_attributes = True

    @classmethod
    def from_db(cls, row: "AlertDB") -> "Alert":
        """Build Alert from DB row with mitre_techniques parsed from JSON."""
        return cls(
            id=row.id,
            created_at=row.created_at,
            src_ip=row.src_ip,
            dst_ip=row.dst_ip,
            src_port=row.src_port,
            dst_port=row.dst_port,
            protocol=row.protocol,
            attack_type=row.attack_type,
            severity=row.severity,
            score=row.score,
            confidence=getattr(row, "confidence", None) or 0.0,
            uncertainty=getattr(row, "uncertainty", None) or 0.0,
            summary=row.summary,
            mitre_techniques=_parse_mitre(getattr(row, "mitre_techniques", None)),
        )


class AlertCreate(BaseModel):
    """Internal model for creating a new alert row."""

    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    attack_type: str
    severity: str
    score: float
    confidence: float = 0.0
    uncertainty: float = 0.0
    summary: str
    mitre_techniques: List[str] = []


# -----------------------------------------------------------------------------
# User & Auth
# -----------------------------------------------------------------------------
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(32), default="analyst")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "analyst"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# -----------------------------------------------------------------------------
# Analyst Feedback
# -----------------------------------------------------------------------------
class AnalystFeedbackDB(Base):
    __tablename__ = "analyst_feedback"
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, index=True)
    analyst_id = Column(Integer, index=True)
    correct_label = Column(String(64), index=True)  # ground truth
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalystFeedbackCreate(BaseModel):
    alert_id: int
    correct_label: str
    comment: Optional[str] = None


class AnalystFeedbackResponse(BaseModel):
    id: int
    alert_id: int
    analyst_id: int
    correct_label: str
    comment: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True


# -----------------------------------------------------------------------------
# Drift & Training
# -----------------------------------------------------------------------------
class DriftSnapshotDB(Base):
    __tablename__ = "drift_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    feature_name = Column(String(64), index=True)
    baseline_mean = Column(Float)
    baseline_std = Column(Float)
    current_mean = Column(Float)
    current_std = Column(Float)
    pvalue = Column(Float)  # drift test p-value
    drifted = Column(Integer, default=0)  # 1 if drifted


class TrainingRunDB(Base):
    __tablename__ = "training_runs"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    datasets = Column(Text)  # JSON list e.g. ["nsl_kdd","cicids2017"]
    model_type = Column(String(32))  # svm, rf
    metrics = Column(Text)  # JSON: f1, precision, recall, minority_recall, etc.
    status = Column(String(32))  # running, completed, failed
    artifact_path = Column(String(512))

