from __future__ import annotations

from datetime import datetime
from typing import Optional

from flask import current_app

from extensions import db
from models.user import User


class AuthService:
    def authenticate(self, username: str, password: str, role: str) -> Optional[User]:
        user = User.query.filter_by(username=username, role=role).first()
        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            current_app.logger.info("Login success", extra={"username": username, "role": role})
            return user
        current_app.logger.warning("Login failed", extra={"username": username, "role": role})
        return None

    def authenticate_admin(self, username: str, password: str) -> Optional[User]:
        return self.authenticate(username, password, "admin")

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        # Users can log in with either 'user' or 'admin' role
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        return None
