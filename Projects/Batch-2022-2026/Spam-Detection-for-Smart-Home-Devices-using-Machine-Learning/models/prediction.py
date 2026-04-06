from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from extensions import db


class Prediction(db.Model):
    __tablename__ = "predictions"

    id: int = db.Column(db.Integer, primary_key=True)
    user_id: Optional[int] = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    parameters: str = db.Column(db.Text, nullable=False)  # JSON list of 10 floats
    result: int = db.Column(db.Integer, nullable=False)  # 0 = valid, 1 = spam
    source: str = db.Column(db.String(20), default="manual")  # 'manual', 'api', 'csv'
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    model_version_id: Optional[int] = db.Column(
        db.Integer, db.ForeignKey("model_versions.id"), nullable=True
    )

    def set_parameters(self, params: list[float]) -> None:
        self.parameters = json.dumps(params)

    def get_parameters(self) -> list[float]:
        return json.loads(self.parameters)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "parameters": self.get_parameters(),
            "result": self.result,
            "label": "spam" if self.result == 1 else "valid",
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "model_version_id": self.model_version_id,
        }
