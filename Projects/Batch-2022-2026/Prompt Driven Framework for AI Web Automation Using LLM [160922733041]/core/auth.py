"""User authentication using SQLite and Flask-Login."""

import os
import sqlite3
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "auth.db")


class User(UserMixin):
    """User model for Flask-Login."""

    def __init__(self, id, username, password_hash, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():
    """Create the users table if it doesn't exist."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def seed_default_user():
    """Create default admin user if no users exist."""
    conn = _get_conn()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count == 0:
        conn.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("admin123"), datetime.now().isoformat()),
        )
        conn.commit()
    conn.close()


def get_user_by_id(user_id):
    """Load user by ID (for Flask-Login user_loader)."""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return User(id=row["id"], username=row["username"],
                     password_hash=row["password_hash"], created_at=row["created_at"])
    return None


def get_user_by_username(username):
    """Load user by username (for login validation)."""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if row:
        return User(id=row["id"], username=row["username"],
                     password_hash=row["password_hash"], created_at=row["created_at"])
    return None


def verify_password(user, password):
    """Check if the provided password matches the stored hash."""
    return check_password_hash(user.password_hash, password)
