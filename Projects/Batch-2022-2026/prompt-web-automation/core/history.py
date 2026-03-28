"""Task history storage using SQLite."""

import os
import sqlite3
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the task_runs table if it doesn't exist."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS task_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            module TEXT NOT NULL,
            url TEXT NOT NULL,
            task_description TEXT NOT NULL,
            status TEXT NOT NULL,
            summary TEXT,
            steps INTEGER DEFAULT 0,
            items_collected INTEGER DEFAULT 0,
            download_filename TEXT,
            duration_seconds REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def save_run(module, url, task_description, status, summary="",
             steps=0, items_collected=0, download_filename=None,
             duration_seconds=0):
    """Save a completed agent run to history.

    Args:
        module: "scraper" or "form_filler"
        url: Target URL
        task_description: User's task prompt
        status: "success", "failed", or "stopped"
        summary: Agent's completion summary
        steps: Number of steps taken
        items_collected: Number of items extracted (scraper only)
        download_filename: Excel filename if applicable
        duration_seconds: How long the run took
    """
    conn = _get_conn()
    conn.execute("""
        INSERT INTO task_runs
            (timestamp, module, url, task_description, status, summary,
             steps, items_collected, download_filename, duration_seconds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        module,
        url,
        task_description,
        status,
        summary,
        steps,
        items_collected,
        download_filename,
        round(duration_seconds, 1),
    ))
    conn.commit()
    conn.close()


def get_history(limit=50):
    """Get recent task runs, newest first.

    Returns:
        list of dicts
    """
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM task_runs ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_run(run_id):
    """Get a single run by ID."""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM task_runs WHERE id = ?", (run_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def clear_history():
    """Delete all history records."""
    conn = _get_conn()
    conn.execute("DELETE FROM task_runs")
    conn.commit()
    conn.close()


# Initialize database on import
init_db()
