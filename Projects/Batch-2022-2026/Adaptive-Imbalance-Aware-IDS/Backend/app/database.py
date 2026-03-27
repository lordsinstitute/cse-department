"""
Database configuration: SQLite (default) or PostgreSQL.

Use DATABASE_URL environment variable for PostgreSQL:
  postgresql://user:password@localhost:5432/nids
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.core.logging import get_logger
from app.base import Base   # <-- IMPORT Base ONLY (do not redefine)

logger = get_logger(__name__)

# PostgreSQL needs different connect_args than SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    connect_args.setdefault("connect_timeout", 10)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True if "postgresql" in DATABASE_URL else False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """Dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def ensure_alert_columns():
    """
    Add new columns to alerts table if missing (e.g. after upgrade).
    Safe for SQLite; no-op for fresh DB or PostgreSQL.
    """
    if "sqlite" not in DATABASE_URL:
        return

    with engine.connect() as conn:
        try:
            r = conn.execute(
                text("""
                SELECT name FROM pragma_table_info('alerts')
                WHERE name IN ('confidence', 'mitre_techniques', 'uncertainty')
                """)
            )
            existing = {row[0] for row in r}

            if "confidence" not in existing:
                conn.execute(text(
                    "ALTER TABLE alerts ADD COLUMN confidence REAL DEFAULT 0"
                ))

            if "mitre_techniques" not in existing:
                conn.execute(text(
                    "ALTER TABLE alerts ADD COLUMN mitre_techniques TEXT"
                ))

            if "uncertainty" not in existing:
                conn.execute(text(
                    "ALTER TABLE alerts ADD COLUMN uncertainty REAL DEFAULT 0"
                ))

            conn.commit()

        except Exception as e:
            logger.debug("ensure_alert_columns: %s", e)
