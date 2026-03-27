"""
Detection scoring: re-export from ML module.

Legacy module for backward compatibility. Use app.ml.inference for full API.
"""

from app.ml.inference import score_flow

__all__ = ["score_flow"]
