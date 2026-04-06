from __future__ import annotations

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: str = db.Column(db.String(256), nullable=False)
    role: str = db.Column(db.String(20), nullable=False, default="user")  # 'admin' or 'user'
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    last_login: datetime = db.Column(db.DateTime, nullable=True)

    predictions = db.relationship("Prediction", backref="user", lazy=True)
    datasets = db.relationship("Dataset", backref="uploader", lazy=True)
    model_versions = db.relationship("ModelVersion", backref="trainer", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
