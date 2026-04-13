from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from extensions import db


class ModelVersion(db.Model):
    __tablename__ = "model_versions"

    id: int = db.Column(db.Integer, primary_key=True)
    version: str = db.Column(db.String(20), nullable=False)
    file_path: str = db.Column(db.String(512), nullable=False)
    accuracy: float = db.Column(db.Float, nullable=False)
    trained_by: Optional[int] = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    trained_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    dataset_id: Optional[int] = db.Column(db.Integer, db.ForeignKey("datasets.id"), nullable=True)
    algorithm_metrics: Optional[str] = db.Column(db.Text, nullable=True)  # JSON blob
    is_active: bool = db.Column(db.Boolean, default=False)

    predictions = db.relationship("Prediction", backref="model_version", lazy=True)

    def set_algorithm_metrics(self, metrics: dict) -> None:
        self.algorithm_metrics = json.dumps(metrics)

    def get_algorithm_metrics(self) -> Optional[dict]:
        return json.loads(self.algorithm_metrics) if self.algorithm_metrics else None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "version": self.version,
            "file_path": self.file_path,
            "accuracy": round(self.accuracy, 4),
            "trained_by": self.trained_by,
            "trained_at": self.trained_at.isoformat(),
            "dataset_id": self.dataset_id,
            "algorithm_metrics": self.get_algorithm_metrics(),
            "is_active": self.is_active,
        }
