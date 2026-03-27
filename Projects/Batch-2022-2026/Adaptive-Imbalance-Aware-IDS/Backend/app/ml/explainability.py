"""
Explainability: feature importance and per-prediction contributions.

Uses model-specific methods: tree feature_importances_ for RF, permutation or coefficients for SVM.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.logging import get_logger
from app.data.features import FEATURE_NAMES, flow_to_features, features_to_vector

logger = get_logger(__name__)

_cached_bundle: Optional[Dict[str, Any]] = None


def _load_bundle(model_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    global _cached_bundle
    if _cached_bundle is not None:
        return _cached_bundle
    from app.config import MODEL_PATH
    path = Path(model_path or MODEL_PATH)
    if not path.exists():
        return None
    try:
        import joblib
        _cached_bundle = joblib.load(path)
        return _cached_bundle
    except Exception as e:
        logger.warning("Explainability: failed to load model: %s", e)
        return None


def _flow_to_feature_dict(flow_dict: Dict[str, Any]) -> Dict[str, float]:
    """Build feature dict from flow for explanation."""
    return flow_to_features(
        src_ip=flow_dict.get("src_ip", ""),
        dst_ip=flow_dict.get("dst_ip", ""),
        src_port=int(flow_dict.get("src_port", 0)),
        dst_port=int(flow_dict.get("dst_port", 0)),
        protocol=str(flow_dict.get("protocol", "TCP")),
        bytes_sent=int(flow_dict.get("bytes_sent", 0)),
        bytes_received=int(flow_dict.get("bytes_received", 0)),
        packets_sent=int(flow_dict.get("packets_sent", 0)),
        packets_received=int(flow_dict.get("packets_received", 0)),
        duration_sec=flow_dict.get("duration_sec"),
        start_time=flow_dict.get("start_time"),
        end_time=flow_dict.get("end_time"),
    )


def get_global_feature_importance(model_path: Optional[str] = None) -> Optional[Dict[str, float]]:
    """
    Return global feature importance (e.g. from RandomForest feature_importances_).
    For SVM without tree, returns equal or from permutation (not implemented here for speed).
    """
    bundle = _load_bundle(model_path)
    if not bundle:
        return None
    model = bundle.get("model")
    if model is None:
        return None
    # Unwrap CalibratedClassifierCV
    if hasattr(model, "estimators_"):
        base = model.calibrated_classifiers_[0].estimator if hasattr(model, "calibrated_classifiers_") else model
    else:
        base = model
    if hasattr(base, "feature_importances_"):
        imp = base.feature_importances_
        return dict(zip(FEATURE_NAMES, [float(x) for x in imp]))
    # SVM: use abs of coef for linear, else return normalized names as placeholder
    if hasattr(base, "coef_") and base.coef_ is not None:
        coef = base.coef_
        if coef.ndim > 1:
            coef = coef[0]
        importance = [float(abs(c)) for c in coef]
        if len(importance) == len(FEATURE_NAMES):
            total = sum(importance) or 1.0
            return {n: imp / total for n, imp in zip(FEATURE_NAMES, importance)}
    # Default: equal importance
    n = len(FEATURE_NAMES)
    return {name: 1.0 / n for name in FEATURE_NAMES}


def explain_alert(
    flow_dict: Dict[str, Any],
    model_path: Optional[str] = None,
    feature_order_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Explain a single prediction: feature values + global importance as contribution proxy.
    Returns dict with feature_values, feature_importance, prediction_summary.
    """
    from app.ml.inference import _load_feature_order, _load_model, score_flow_ml
    order_path = feature_order_path or os.getenv("MODEL_FEATURE_ORDER_PATH", "models/feature_order.json")
    path = model_path or os.getenv("MODEL_PATH", "models/detector.joblib")
    features = _flow_to_feature_dict(flow_dict)
    feature_order = _load_feature_order(order_path)
    importance = get_global_feature_importance(path)
    if importance is None:
        importance = {n: 1.0 / len(FEATURE_NAMES) for n in FEATURE_NAMES}
    # Top contributors: sort by importance * abs(value) as proxy for impact
    values = {k: features.get(k, 0.0) for k in feature_order}
    contribution = [
        {"feature": k, "value": values[k], "importance": importance.get(k, 0), "impact": values[k] * importance.get(k, 0)}
        for k in feature_order
    ]
    contribution.sort(key=lambda x: abs(x["impact"]), reverse=True)
    score, severity, attack_type, summary, _, confidence, uncertainty = score_flow_ml(
        flow_dict, path, order_path
    )
    return {
        "feature_values": values,
        "feature_importance": importance,
        "top_contributors": contribution[:10],
        "prediction": {
            "attack_type": attack_type,
            "severity": severity,
            "confidence": confidence,
            "uncertainty": uncertainty,
            "summary": summary,
        },
    }
