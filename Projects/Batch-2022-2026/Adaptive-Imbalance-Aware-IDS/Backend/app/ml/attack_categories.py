"""
Attack categories and MITRE ATT&CK mapping.

Supports multiple attack types and maps them to MITRE ATT&CK for SOC reporting.
"""

from typing import Dict, List, Optional

# Attack type to severity (for alerting)
ATTACK_SEVERITY: Dict[str, str] = {
    "benign": "info",
    "dos": "high",
    "ddos": "critical",
    "port_scan": "medium",
    "brute_force": "high",
    "botnet": "critical",
    "web_attack": "high",
    "exploit": "high",
    "infiltration": "critical",
    "data_exfiltration": "high",
    "malicious": "medium",
    "unknown": "low",
}

# MITRE ATT&CK technique IDs (simplified mapping for NIDS context)
# https://attack.mitre.org/
MITRE_ATTACK_MAP: Dict[str, List[str]] = {
    "benign": [],
    "dos": ["T1498", "T1499"],           # Network Denial of Service, Endpoint Denial of Service
    "ddos": ["T1498", "T1499"],
    "port_scan": ["T1046"],             # Network Service Discovery
    "brute_force": ["T1110"],           # Brute Force
    "botnet": ["T1583", "T1584", "T1585"],  # Acquire Infrastructure, etc.
    "web_attack": ["T1190"],            # Exploit Public-Facing Application
    "exploit": ["T1190", "T1203"],
    "infiltration": ["T1048"],           # Exfiltration Over Alternative Protocol
    "data_exfiltration": ["T1048", "T1041"],
    "malicious": ["T1046"],
    "unknown": [],
}

# All supported attack labels (for classification)
ATTACK_LABELS: List[str] = [
    "benign",
    "dos",
    "ddos",
    "port_scan",
    "brute_force",
    "botnet",
    "web_attack",
    "exploit",
    "infiltration",
    "data_exfiltration",
    "malicious",
    "unknown",
]


def get_severity(attack_type: str) -> str:
    """Return severity level for an attack type."""
    return ATTACK_SEVERITY.get(attack_type.lower(), "low")


def get_mitre_techniques(attack_type: str) -> List[str]:
    """Return MITRE ATT&CK technique IDs for an attack type."""
    return MITRE_ATTACK_MAP.get(attack_type.lower(), [])
