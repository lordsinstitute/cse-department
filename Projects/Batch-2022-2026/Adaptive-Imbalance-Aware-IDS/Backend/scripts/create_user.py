"""Create an initial user for login (e.g. admin / admin)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.auth import create_user, hash_password
from app.database import SessionLocal
from app.models import UserDB


def main():
    db = SessionLocal()
    try:
        existing = db.query(UserDB).filter(UserDB.username == "admin").first()
        if existing:
            print("User 'admin' already exists.")
            return
        user = create_user(db, "admin", "admin@nids.local", "admin", role="analyst")
        print(f"Created user: {user.username} (id={user.id}). Login with admin / admin")
    finally:
        db.close()


if __name__ == "__main__":
    main()
