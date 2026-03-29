from fastapi import APIRouter, Depends
import sqlite3

from app.core.database import get_db
from app.core.security import require_admin, get_current_user
from app.schemas.schemas import AppConfigUpdate
from app.services.config_service import set_config_value, get_active_api_key

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.put("/config")
def update_config(
    req: AppConfigUpdate,
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    updated = []
    if req.anthropic_api_key is not None:
        set_config_value(conn, "anthropic_api_key", req.anthropic_api_key)
        updated.append("anthropic_api_key")

    return {"message": f"Updated config: {', '.join(updated)}" if updated else "No changes"}


@router.get("/config")
def get_config(
    conn: sqlite3.Connection = Depends(get_db),
    admin: dict = Depends(require_admin),
):
    key = get_active_api_key(conn)
    return {
        "anthropic_api_key": "***configured***" if key else "not set",
    }


@router.get("/config/status")
def get_config_status(
    conn: sqlite3.Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Check if API key is configured. Available to all authenticated users."""
    key = get_active_api_key(conn)
    return {"api_key_configured": bool(key)}
