import sqlite3
from typing import Optional

from app.core.config import settings


def get_config_value(conn: sqlite3.Connection, key: str) -> Optional[str]:
    row = conn.execute("SELECT value FROM app_config WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None


def set_config_value(conn: sqlite3.Connection, key: str, value: str):
    conn.execute(
        "INSERT INTO app_config (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?",
        (key, value, value)
    )
    conn.commit()


def get_active_api_key(conn: sqlite3.Connection) -> str:
    db_key = get_config_value(conn, "anthropic_api_key")
    return db_key or settings.ANTHROPIC_API_KEY


def get_active_model(conn: sqlite3.Connection) -> str:
    return get_config_value(conn, "claude_model") or settings.CLAUDE_MODEL


def get_active_top_k(conn: sqlite3.Connection) -> int:
    val = get_config_value(conn, "retrieval_top_k")
    return int(val) if val else settings.RETRIEVAL_TOP_K


def get_active_temperature(conn: sqlite3.Connection) -> float:
    val = get_config_value(conn, "llm_temperature")
    return float(val) if val else settings.LLM_TEMPERATURE
