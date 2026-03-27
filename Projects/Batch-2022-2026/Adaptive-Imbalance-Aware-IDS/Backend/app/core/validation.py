"""
Input validation for ingestion and API.

Prevents alert spoofing and invalid data.
"""

import re
from typing import Optional, Tuple

# IP v4 simple validation
IPV4_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}"
    r"(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
)

# Allowed protocols
ALLOWED_PROTOCOLS = frozenset({"TCP", "UDP", "ICMP", "GRE", "OTHER"})


def validate_ip(ip: str) -> bool:
    """Return True if string looks like a valid IPv4 address."""
    if not ip or not isinstance(ip, str):
        return False
    return bool(IPV4_PATTERN.match(ip.strip()))


def validate_port(port: int) -> bool:
    """Return True if port is in valid range."""
    return isinstance(port, int) and 0 <= port <= 65535


def validate_flow_input(
    src_ip: str,
    dst_ip: str,
    src_port: int,
    dst_port: int,
    protocol: str,
    bytes_sent: int = 0,
    bytes_received: int = 0,
    packets_sent: int = 0,
    packets_received: int = 0,
) -> Tuple[bool, Optional[str]]:
    """
    Validate flow fields. Returns (valid, error_message).
    error_message is None when valid is True.
    """
    if not validate_ip(src_ip):
        return False, "Invalid src_ip"
    if not validate_ip(dst_ip):
        return False, "Invalid dst_ip"
    if not validate_port(src_port):
        return False, "Invalid src_port"
    if not validate_port(dst_port):
        return False, "Invalid dst_port"
    if protocol.upper() not in ALLOWED_PROTOCOLS:
        return False, "Invalid protocol"
    if any(
        not isinstance(x, int) or x < 0
        for x in (bytes_sent, bytes_received, packets_sent, packets_received)
    ):
        return False, "Bytes and packets must be non-negative integers"
    return True, None
