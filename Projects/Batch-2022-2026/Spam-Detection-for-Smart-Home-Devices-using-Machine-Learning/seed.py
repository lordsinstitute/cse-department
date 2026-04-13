"""
Run once to seed the database with default admin and user accounts.
Usage: python3 seed.py
"""
from app import create_app
from extensions import db
from models.user import User


def seed() -> None:
    app = create_app("development")
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", role="admin")
            admin.set_password("admin")
            db.session.add(admin)
            print("Created admin user")

        if not User.query.filter_by(username="user").first():
            user = User(username="user", role="user")
            user.set_password("user")
            db.session.add(user)
            print("Created user")

        db.session.commit()
        print("Seeding complete.")


if __name__ == "__main__":
    seed()
