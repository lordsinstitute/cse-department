"""
Inference: score flows with trained ML model or rule-based fallback.

Returns attack_type, severity, confidence score, and MITRE ATT&CK mapping.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.core.logging import get_logger
from app.data.features import flow_to_features, features_to_vector
from app.ml.attack_categories import get_mitre_techniques, get_severity

logger = get_logger(__name__)

# Module-level cache for loaded model
_cached_model: Optional[Dict[str, Any]] = None
_cached_feature_order: Optional[List[str]] = None


def _load_model(model_path: str) -> Optional[Dict[str, Any]]:
    """Load joblib model and label encoder from path."""
    global _cached_model
    if _cached_model is not None:
        return _cached_model
    path = Path(model_path)
    if not path.exists():
        logger.debug("No model file at %s; using rule fallback", model_path)
        return None
    try:
        import joblib
        _cached_model = joblib.load(path)
        logger.info("Loaded ML model from %s", model_path)
        return _cached_model
    except Exception as e:
        logger.warning("Failed to load model from %s: %s", model_path, e)
        return None


def _load_feature_order(feature_order_path: str) -> List[str]:
    """Load feature order JSON; fallback to FEATURE_NAMES."""
    global _cached_feature_order
    if _cached_feature_order is not None:
        return _cached_feature_order
    path = Path(feature_order_path)
    if path.exists():
        try:
            with open(path) as f:
                _cached_feature_order = json.load(f)
            return _cached_feature_order
        except Exception as e:
            logger.warning("Failed to load feature order: %s", e)
    from app.data.features import FEATURE_NAMES
    _cached_feature_order = FEATURE_NAMES
    return _cached_feature_order


def _flow_to_dict(flow: Any) -> Dict[str, Any]:
    """Normalize flow (Pydantic model or dict) to dict."""
    if hasattr(flow, "model_dump"):
        return flow.model_dump()
    if isinstance(flow, dict):
        return flow
    return {
        "src_ip": getattr(flow, "src_ip", ""),
        "dst_ip": getattr(flow, "dst_ip", ""),
        "src_port": getattr(flow, "src_port", 0),
        "dst_port": getattr(flow, "dst_port", 0),
        "protocol": getattr(flow, "protocol", "TCP"),
        "bytes_sent": getattr(flow, "bytes_sent", 0),
        "bytes_received": getattr(flow, "bytes_received", 0),
        "packets_sent": getattr(flow, "packets_sent", 0),
        "packets_received": getattr(flow, "packets_received", 0),
        "duration_sec": getattr(flow, "duration_sec", None),
        "start_time": getattr(flow, "start_time", None),
        "end_time": getattr(flow, "end_time", None),
    }


def score_flow_ml(
    flow_dict: Dict[str, Any],
    model_path: str,
    feature_order_path: str,
) -> Tuple[float, str, str, str, List[str], float, float]:
    """
    Score a flow with the trained model.

    Returns:
        score, severity, attack_type, summary, mitre_techniques, confidence, uncertainty
    """
    fd = _flow_to_dict(flow_dict)
    features = flow_to_features(
        src_ip=fd.get("src_ip", ""),
        dst_ip=fd.get("dst_ip", ""),
        src_port=fd.get("src_port", 0),
        dst_port=fd.get("dst_port", 0),
        protocol=fd.get("protocol", "TCP"),
        bytes_sent=fd.get("bytes_sent", 0),
        bytes_received=fd.get("bytes_received", 0),
        packets_sent=fd.get("packets_sent", 0),
        packets_received=fd.get("packets_received", 0),
        duration_sec=fd.get("duration_sec"),
        start_time=fd.get("start_time"),
        end_time=fd.get("end_time"),
    )
    feature_order = _load_feature_order(feature_order_path)
    X = [features_to_vector(features, feature_order)]

    bundle = _load_model(model_path)
    if bundle is None:
        return 0.0, "info", "benign", "No model loaded", [], 0.0, 1.0

    model = bundle.get("model")
    le = bundle.get("label_encoder")
    if model is None or le is None:
        return 0.0, "info", "benign", "Invalid model bundle", [], 0.0, 1.0

    try:
        scaler = bundle.get("scaler")
        if scaler is not None:
            X = scaler.transform(X)
        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0] if hasattr(model, "predict_proba") else None
        if proba is not None:
            confidence = float(proba.max())
            uncertainty = float(1.0 - confidence)
        else:
            confidence = 1.0
            uncertainty = 0.0
        attack_type = le.inverse_transform([pred])[0]
        severity = get_severity(attack_type)
        mitre = get_mitre_techniques(attack_type)
        score = confidence if attack_type != "benign" else 1.0 - confidence
        summary = f"ML: {attack_type} (confidence={confidence:.2f})"
        if mitre:
            summary += " [" + ", ".join(mitre) + "]"
        return score, severity, attack_type, summary, mitre, confidence, uncertainty
    except Exception as e:
        logger.debug("ML inference error: %s", e)
        return 0.0, "info", "benign", "Inference error", [], 0.0, 1.0


def score_flow_rules(
    flow_dict: Dict[str, Any],
) -> Tuple[float, str, str, str, List[str], float, float]:
    """
    Rule-based scoring (fallback). Returns same signature as score_flow_ml.
    """
    fd = _flow_to_dict(flow_dict)
    total_bytes = fd.get("bytes_sent", 0) + fd.get("bytes_received", 0)
    total_packets = fd.get("packets_sent", 0) + fd.get("packets_received", 0)
    dst_port = fd.get("dst_port", 0)

    score = 0.0
    attack_type = "benign"
    severity = "info"
    summary = "Benign flow"
    confidence = 0.0

    if dst_port in (22, 23, 3389) and total_packets > 50:
        score = 0.85
        attack_type = "brute_force"
        severity = "high"
        summary = "High packet volume to remote access service"
        confidence = 0.85
    elif total_bytes > 10_000_000:
        score = 0.75
        attack_type = "data_exfiltration"
        severity = "medium"
        summary = "Unusually large data transfer in single flow"
        confidence = 0.75
    elif total_packets > 5_000:
        score = 0.7
        attack_type = "dos"
        severity = "medium"
        summary = "High packet rate suggesting DoS-like behavior"
        confidence = 0.7

    mitre = get_mitre_techniques(attack_type)
    uncertainty = 1.0 - confidence
    return score, severity, attack_type, summary, mitre, confidence, uncertainty


def score_flow(
    flow: Any,
    model_path: Optional[str] = None,
    feature_order_path: Optional[str] = None,
    use_rule_fallback: bool = True,
) -> Tuple[float, str, str, str, List[str], float, float]:
    """
    Score a flow: use ML model if available, else rule-based.

    Returns:
        score, severity, attack_type, summary, mitre_techniques, confidence, uncertainty
    """
    from app.config import MODEL_FEATURE_ORDER_PATH, MODEL_PATH, USE_RULE_FALLBACK
    path = model_path or MODEL_PATH
    order_path = feature_order_path or MODEL_FEATURE_ORDER_PATH
    fallback = use_rule_fallback and USE_RULE_FALLBACK
    flow_dict = _flow_to_dict(flow)

    bundle = _load_model(path)
    if bundle is not None:
        return score_flow_ml(flow_dict, path, order_path)
    if fallback:
        return score_flow_rules(flow_dict)
    return 0.0, "info", "benign", "No detector available", [], 0.0, 1.0
