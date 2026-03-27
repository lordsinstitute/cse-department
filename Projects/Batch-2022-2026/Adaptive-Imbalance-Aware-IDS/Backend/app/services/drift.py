"""
Adaptive drift monitoring: compare recent feature distribution to baseline.

Uses simple statistical tests (e.g. mean/std comparison or KS) to flag drift per feature.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np
from sqlalchemy.orm import Session

from app.config import DRIFT_PVALUE_THRESHOLD, DRIFT_WINDOW_SIZE
from app.core.logging import get_logger
from app.database import get_db
from app.models import DriftSnapshotDB

logger = get_logger(__name__)

# In-memory baseline and recent window (in production, use DB or Redis)
_baseline: Dict[str, np.ndarray] = {}
_recent_buffer: List[Dict[str, float]] = []
_max_baseline_size = 5000
_max_recent_size = 1000


def update_baseline(feature_rows: List[Dict[str, float]]) -> None:
    """Update baseline statistics from feature rows."""
    global _baseline
    from app.data.features import FEATURE_NAMES, features_to_vector
    if not feature_rows:
        return
    X = np.array([features_to_vector(r, FEATURE_NAMES) for r in feature_rows[: _max_baseline_size]], dtype=np.float64)
    _baseline = {}
    for i, name in enumerate(FEATURE_NAMES):
        if i < X.shape[1]:
            col = X[:, i]
            _baseline[name] = col
    logger.info("Drift baseline updated with %d samples", len(feature_rows))


def push_recent(features: Dict[str, float]) -> None:
    """Append one feature vector to recent buffer for drift check."""
    global _recent_buffer
    _recent_buffer.append(features)
    if len(_recent_buffer) > _max_recent_size:
        _recent_buffer = _recent_buffer[-_max_recent_size:]


def _ks_statistic(baseline: np.ndarray, current: np.ndarray) -> float:
    """Approximate two-sample KS p-value (simplified)."""
    try:
        from scipy import stats
        return float(stats.ks_2samp(baseline, current).pvalue)
    except Exception:
        return 0.5


def _ttest_pvalue(baseline: np.ndarray, current: np.ndarray) -> float:
    """Two-sample t-test p-value."""
    try:
        from scipy import stats
        return float(stats.ttest_ind(baseline, current).pvalue)
    except Exception:
        return 0.5


def compute_drift(
    db: Optional[Session] = None,
    pvalue_threshold: float = DRIFT_PVALUE_THRESHOLD,
) -> Dict[str, Any]:
    """
    Compare recent buffer to baseline; return drift metrics and optionally persist snapshots.
    """
    from app.data.features import FEATURE_NAMES, features_to_vector
    global _recent_buffer
    if not _baseline or not _recent_buffer:
        return {
            "drifted": False,
            "message": "Insufficient baseline or recent data",
            "features": [],
            "baseline_size": sum(len(v) for v in _baseline.values()) // max(len(_baseline), 1),
            "recent_size": len(_recent_buffer),
        }
    X_recent = np.array(
        [features_to_vector(r, FEATURE_NAMES) for r in _recent_buffer[-DRIFT_WINDOW_SIZE:]],
        dtype=np.float64,
    )
    results = []
    any_drifted = False
    for i, name in enumerate(FEATURE_NAMES):
        if name not in _baseline or i >= X_recent.shape[1]:
            continue
        base_col = _baseline[name]
        cur_col = X_recent[:, i]
        base_mean, base_std = float(np.mean(base_col)), float(np.std(base_col)) or 1e-9
        cur_mean, cur_std = float(np.mean(cur_col)), float(np.std(cur_col)) or 1e-9
        pvalue = _ttest_pvalue(base_col, cur_col)
        drifted = pvalue < pvalue_threshold
        if drifted:
            any_drifted = True
        results.append({
            "feature_name": name,
            "baseline_mean": base_mean,
            "baseline_std": base_std,
            "current_mean": cur_mean,
            "current_std": cur_std,
            "pvalue": pvalue,
            "drifted": drifted,
        })
        if db:
            snap = DriftSnapshotDB(
                feature_name=name,
                baseline_mean=base_mean,
                baseline_std=base_std,
                current_mean=cur_mean,
                current_std=cur_std,
                pvalue=pvalue,
                drifted=1 if drifted else 0,
            )
            db.add(snap)
    if db:
        db.commit()
    return {
        "drifted": any_drifted,
        "pvalue_threshold": pvalue_threshold,
        "features": results,
        "baseline_size": len(_baseline.get(FEATURE_NAMES[0], [])),
        "recent_size": len(_recent_buffer),
    }


def get_drift_history(db: Session, limit: int = 100) -> List[Dict[str, Any]]:
    """Return recent drift snapshots from DB."""
    rows = (
        db.query(DriftSnapshotDB)
        .order_by(DriftSnapshotDB.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "feature_name": r.feature_name,
            "baseline_mean": r.baseline_mean,
            "current_mean": r.current_mean,
            "pvalue": r.pvalue,
            "drifted": bool(r.drifted),
        }
        for r in rows
    ]
