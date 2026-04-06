from __future__ import annotations

from datetime import datetime

from flask import Blueprint, current_app
from sqlalchemy import text

from extensions import db

health_bp = Blueprint("health_bp", __name__)


@health_bp.route("/health")
def health() -> tuple:
    checks: dict[str, str] = {}

    # DB check
    try:
        db.session.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception as exc:
        current_app.logger.error("Health DB check failed: %s", exc)
        checks["db"] = "error"

    # Model check
    ml_service = current_app.extensions.get("ml_service")
    checks["model"] = "loaded" if (ml_service and ml_service._model is not None) else "not_loaded"

    status = "healthy" if all(v in ("ok", "loaded") for v in checks.values()) else "degraded"
    http_code = 200 if status == "healthy" else 503

    return {
        "status": status,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }, http_code
