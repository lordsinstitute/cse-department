"""
Flow-level and packet-level feature extraction.

Produces a fixed-size feature vector suitable for ML models.
Handles missing/invalid values with safe defaults.
"""

import math
from typing import Any, Dict, List, Optional, Union

# Feature names in the order expected by the trained model
FEATURE_NAMES: List[str] = [
    "duration",
    "protocol_type_tcp",
    "protocol_type_udp",
    "src_bytes",
    "dst_bytes",
    "total_bytes",
    "packets_sent",
    "packets_received",
    "total_packets",
    "bytes_per_packet",
    "packets_per_second",
    "dst_port",
    "src_port",
    "is_privileged_dst",
    "is_privileged_src",
    "is_common_service_port",
]


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Convert to float; use default on failure or NaN/Inf."""
    try:
        x = float(value)
        if math.isfinite(x):
            return x
    except (TypeError, ValueError):
        pass
    return default


def _safe_int(value: Any, default: int = 0) -> int:
    """Convert to int; use default on failure."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def flow_to_features(
    src_ip: str,
    dst_ip: str,
    src_port: int,
    dst_port: int,
    protocol: str,
    bytes_sent: int = 0,
    bytes_received: int = 0,
    packets_sent: int = 0,
    packets_received: int = 0,
    duration_sec: Optional[float] = None,
    **kwargs: Any,
) -> Dict[str, float]:
    """
    Extract a fixed set of numerical features from a flow.

    Handles noisy/incomplete data: missing or invalid values are replaced
    with safe defaults (e.g. 0 or derived values). All returned values
    are finite floats suitable for ML.

    Args:
        src_ip, dst_ip: Not used numerically; kept for API compatibility.
        src_port, dst_port: Port numbers.
        protocol: e.g. TCP, UDP.
        bytes_sent, bytes_received, packets_sent, packets_received: Counts.
        duration_sec: Flow duration in seconds. If None, inferred from kwargs
            or set to 1.0 to avoid division by zero.
        **kwargs: Optional extra fields (e.g. start_time, end_time) for duration.

    Returns:
        Dictionary mapping FEATURE_NAMES to float values.
    """
    total_bytes = _safe_int(bytes_sent, 0) + _safe_int(bytes_received, 0)
    total_packets = _safe_int(packets_sent, 0) + _safe_int(packets_received, 0)

    duration = duration_sec
    if duration is None and kwargs.get("start_time") and kwargs.get("end_time"):
        try:
            start = kwargs["start_time"]
            end = kwargs["end_time"]
            if hasattr(start, "timestamp") and hasattr(end, "timestamp"):
                duration = end.timestamp() - start.timestamp()
        except (TypeError, ValueError, AttributeError):
            pass
    if duration is None or duration <= 0:
        duration = 1.0

    protocol_upper = (protocol or "TCP").upper()
    protocol_type_tcp = 1.0 if protocol_upper == "TCP" else 0.0
    protocol_type_udp = 1.0 if protocol_upper == "UDP" else 0.0

    bytes_per_packet = (
        total_bytes / total_packets if total_packets > 0 else 0.0
    )
    packets_per_second = total_packets / duration if duration > 0 else 0.0

    # Privileged ports: 0-1023
    is_privileged_dst = 1.0 if 0 <= dst_port <= 1023 else 0.0
    is_privileged_src = 1.0 if 0 <= src_port <= 1023 else 0.0
    common_services = {21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 8080}
    is_common_service_port = 1.0 if dst_port in common_services else 0.0

    return {
        "duration": _safe_float(duration),
        "protocol_type_tcp": protocol_type_tcp,
        "protocol_type_udp": protocol_type_udp,
        "src_bytes": _safe_float(bytes_sent),
        "dst_bytes": _safe_float(bytes_received),
        "total_bytes": _safe_float(total_bytes),
        "packets_sent": _safe_float(packets_sent),
        "packets_received": _safe_float(packets_received),
        "total_packets": _safe_float(total_packets),
        "bytes_per_packet": _safe_float(bytes_per_packet),
        "packets_per_second": _safe_float(packets_per_second),
        "dst_port": _safe_float(dst_port),
        "src_port": _safe_float(src_port),
        "is_privileged_dst": is_privileged_dst,
        "is_privileged_src": is_privileged_src,
        "is_common_service_port": is_common_service_port,
    }


def features_to_vector(features: Dict[str, float], feature_order: List[str]) -> List[float]:
    """
    Return a list of feature values in the order expected by the model.

    Missing keys are filled with 0.0.
    """
    return [features.get(name, 0.0) for name in feature_order]
