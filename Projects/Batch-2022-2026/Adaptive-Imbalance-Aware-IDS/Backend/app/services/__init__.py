"""Business logic: alert deduplication, correlation."""

from app.services.alerts import deduplicate_alerts, alert_correlation_key

__all__ = ["deduplicate_alerts", "alert_correlation_key"]
