from __future__ import annotations

from datetime import datetime
from typing import Optional

from extensions import db


class Dataset(db.Model):
    __tablename__ = "datasets"

    id: int = db.Column(db.Integer, primary_key=True)
    filename: str = db.Column(db.String(255), nullable=False)
    file_path: str = db.Column(db.String(512), nullable=False)
    uploaded_by: Optional[int] = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    upload_time: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    row_count: Optional[int] = db.Column(db.Integer, nullable=True)
    is_active: bool = db.Column(db.Boolean, default=False)

    model_versions = db.relationship("ModelVersion", backref="dataset", lazy=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "uploaded_by": self.uploaded_by,
            "upload_time": self.upload_time.isoformat(),
            "row_count": self.row_count,
            "is_active": self.is_active,
        }
