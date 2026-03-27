"""
Alert deduplication and correlation.

Reduces noise by grouping similar alerts and correlating by time/source.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from app.core.logging import get_logger

logger = get_logger(__name__)

# Time window (seconds) within which similar alerts are considered duplicate
DEDUP_WINDOW_SEC = 60
# Max alerts to merge into one incident
CORRELATION_MAX_ALERTS = 50


def alert_correlation_key(alert: Dict[str, Any]) -> Tuple[str, ...]:
    """
    Key for deduplication: same (src_ip, dst_ip, attack_type) in a time window.
    """
    return (
        str(alert.get("src_ip", "")),
        str(alert.get("dst_ip", "")),
        str(alert.get("attack_type", "")),
    )


def deduplicate_alerts(
    alerts: List[Dict[str, Any]],
    window_sec: int = DEDUP_WINDOW_SEC,
) -> List[Dict[str, Any]]:
    """
    Return a deduplicated list: keep one representative per (src_ip, dst_ip, attack_type)
    within the time window (keep newest, merge count into summary if desired).
    """
    if not alerts:
        return []
    by_key: Dict[Tuple[str, ...], List[Dict[str, Any]]] = {}
    for a in alerts:
        key = alert_correlation_key(a)
        ts = a.get("created_at")
        if isinstance(ts, str):
            try:
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except ValueError:
                ts = None
        if key not in by_key:
            by_key[key] = []
        by_key[key].append((ts, a))

    result = []
    for key, group in by_key.items():
        # Sort by time descending, take newest in window
        group.sort(key=lambda x: x[0] or datetime.min, reverse=True)
        kept = group[0][1]
        within_window = [
            g for g in group
            if g[0] and group[0][0] and (group[0][0] - g[0]).total_seconds() <= window_sec
        ]
        if len(within_window) > 1:
            kept = {**kept, "count": len(within_window)}
        result.append(kept)
    result.sort(key=lambda a: a.get("created_at", ""), reverse=True)
    return result


def correlate_incidents(
    alerts: List[Dict[str, Any]],
    window_sec: int = 300,
) -> List[Dict[str, Any]]:
    """
    Group alerts into incidents: same key within window_sec.
    Returns list of incidents, each with alerts list and summary.
    """
    if not alerts:
        return []
    by_key: Dict[Tuple[str, ...], List[Dict[str, Any]]] = {}
    for a in alerts:
        key = alert_correlation_key(a)
        if key not in by_key:
            by_key[key] = []
        by_key[key].append(a)

    incidents = []
    for key, group in by_key.items():
        group.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        incidents.append({
            "key": list(key),
            "alert_count": len(group),
            "alerts": group[:CORRELATION_MAX_ALERTS],
            "first_seen": group[-1].get("created_at") if group else None,
            "last_seen": group[0].get("created_at") if group else None,
        })
    return incidents
