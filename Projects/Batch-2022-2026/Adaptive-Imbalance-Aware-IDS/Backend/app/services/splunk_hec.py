"""
Splunk HTTP Event Collector (HEC) integration.

Sends alert events to Splunk when SPLUNK_HEC_URL and SPLUNK_HEC_TOKEN are set.
"""

import json
from typing import Any, Dict, Optional
from datetime import datetime

import requests

from app.config import SPLUNK_HEC_TOKEN, SPLUNK_HEC_URL, SPLUNK_INDEX
from app.core.logging import get_logger

logger = get_logger(__name__)

def send_alert_to_splunk(alert: dict) -> bool:
    if not SPLUNK_HEC_URL or not SPLUNK_HEC_TOKEN:
        return False

    def json_safe(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return obj

    try:
        payload = {
            "event": alert,
            "sourcetype": "nids:alert",
            "index": SPLUNK_INDEX,
        }

        safe_payload = json.loads(json.dumps(payload, default=json_safe))

        headers = {
            "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
            "Content-Type": "application/json",
        }

        r = requests.post(
            SPLUNK_HEC_URL,
            json=safe_payload,
            headers=headers,
            timeout=5,
            verify=False
        )

        if r.status_code in (200, 201):
            return True

        logger.warning("Splunk HEC returned %s: %s", r.status_code, r.text[:200])

    except Exception as e:
        logger.warning("Splunk HEC send failed: %s", e)

    return False