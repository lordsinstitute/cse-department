"""
Application configuration and environment settings.

Uses environment variables with sensible defaults for development.
"""
from dotenv import load_dotenv
import os

load_dotenv()

SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")
SPLUNK_INDEX = os.getenv("SPLUNK_INDEX", "main")

import os
from typing import Optional

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./alerts.db",
)
# For PostgreSQL: postgresql://user:pass@localhost:5432/nids

# -----------------------------------------------------------------------------
# API & Security
# -----------------------------------------------------------------------------
API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "9000"))
API_SECRET_KEY: Optional[str] = os.getenv("API_SECRET_KEY", "nids-dev-secret-change-in-production")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
REQUIRE_AUTH: bool = os.getenv("REQUIRE_AUTH", "false").lower() in ("1", "true", "yes")

# -----------------------------------------------------------------------------
# Ingestion & Rate Limiting
# -----------------------------------------------------------------------------
INGEST_RATE_LIMIT: int = int(os.getenv("INGEST_RATE_LIMIT", "10000"))
INGEST_BUFFER_SIZE: int = int(os.getenv("INGEST_BUFFER_SIZE", "5000"))
INGEST_BATCH_SIZE: int = int(os.getenv("INGEST_BATCH_SIZE", "100"))
LIVE_CAPTURE_INTERFACE: Optional[str] = os.getenv("LIVE_CAPTURE_INTERFACE")  # e.g. eth0

# -----------------------------------------------------------------------------
# ML Model
# -----------------------------------------------------------------------------
MODEL_PATH: str = os.getenv("MODEL_PATH", "models/detector.joblib")
MODEL_FEATURE_ORDER_PATH: str = os.getenv(
    "MODEL_FEATURE_ORDER_PATH", "models/feature_order.json"
)
USE_RULE_FALLBACK: bool = os.getenv("USE_RULE_FALLBACK", "true").lower() in (
    "1", "true", "yes",
)

# -----------------------------------------------------------------------------
# Splunk HTTP Event Collector
# -----------------------------------------------------------------------------
SPLUNK_HEC_URL: Optional[str] = os.getenv("SPLUNK_HEC_URL")  # https://splunk:8088/services/collector/event
SPLUNK_HEC_TOKEN: Optional[str] = os.getenv("SPLUNK_HEC_TOKEN")
SPLUNK_INDEX: str = os.getenv("SPLUNK_INDEX", "nids")

# -----------------------------------------------------------------------------
# Drift & Feedback
# -----------------------------------------------------------------------------
DRIFT_WINDOW_SIZE: int = int(os.getenv("DRIFT_WINDOW_SIZE", "1000"))
DRIFT_PVALUE_THRESHOLD: float = float(os.getenv("DRIFT_PVALUE_THRESHOLD", "0.05"))

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = os.getenv(
    "LOG_FORMAT",
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
