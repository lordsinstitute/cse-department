"""
Model training, validation, and testing pipeline.

Trains a classifier on CICIDS/UNSW-style data, computes metrics
(accuracy, precision, recall, F1, confusion matrix), and saves the model.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from app.core.logging import get_logger
from app.data.features import FEATURE_NAMES, features_to_vector
from app.ml.attack_categories import ATTACK_LABELS

logger = get_logger(__name__)


def load_training_data(
    feature_rows: List[Dict[str, float]],
    labels: List[str],
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, LabelEncoder]:
    """
    Build X, y from feature dicts and labels; split into train/val/test.

    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test, label_encoder
    """
    X = np.array([features_to_vector(r, FEATURE_NAMES) for r in feature_rows], dtype=np.float64)
    le = LabelEncoder()
    le.fit(ATTACK_LABELS)
    # Map unknown labels to "unknown"
    y = []
    for lbl in labels:
        if lbl in le.classes_:
            y.append(lbl)
        else:
            y.append("unknown")
    y = le.transform(y)

    X_rest, X_test, y_rest, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_rest, y_rest, test_size=val_ratio, random_state=random_state, stratify=y_rest
    )
    return X_train, X_val, X_test, y_train, y_val, y_test, le


def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    **kwargs: Any,
) -> RandomForestClassifier:
    """
    Train a RandomForest classifier. kwargs passed to RandomForestClassifier.
    """
    default = dict(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
    default.update(kwargs)
    clf = RandomForestClassifier(**default)
    clf.fit(X_train, y_train)
    return clf


def evaluate(
    model: RandomForestClassifier,
    X: np.ndarray,
    y_true: np.ndarray,
    label_encoder: LabelEncoder,
) -> Dict[str, Any]:
    """
    Compute accuracy, precision, recall, F1, and confusion matrix.
    """
    y_pred = model.predict(X)
    # Handle binary/multiclass
    average = "weighted" if len(np.unique(y_true)) > 2 else "binary"
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, average=average, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "labels": list(label_encoder.classes_),
        "classification_report": classification_report(
            y_true, y_pred, target_names=label_encoder.classes_, zero_division=0
        ),
    }


def run_pipeline(
    feature_rows: List[Dict[str, float]],
    labels: List[str],
    output_dir: str = "models",
    test_size: float = 0.2,
    val_size: float = 0.1,
    save_model: bool = True,
) -> Dict[str, Any]:
    """
    Full pipeline: split data, train, validate, test, save model and metrics.

    Returns dict with train/val/test metrics and paths.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    X_train, X_val, X_test, y_train, y_val, y_test, le = load_training_data(
        feature_rows, labels, test_size=test_size, val_size=val_size
    )

    model = train_model(X_train, y_train)
    train_metrics = evaluate(model, X_train, y_train, le)
    val_metrics = evaluate(model, X_val, y_val, le)
    test_metrics = evaluate(model, X_test, y_test, le)

    results = {
        "train": train_metrics,
        "validation": val_metrics,
        "test": test_metrics,
        "feature_order": FEATURE_NAMES,
    }

    if save_model:
        import joblib
        model_path = os.path.join(output_dir, "detector.joblib")
        joblib.dump({"model": model, "label_encoder": le}, model_path)
        results["model_path"] = model_path
        feature_order_path = os.path.join(output_dir, "feature_order.json")
        with open(feature_order_path, "w") as f:
            json.dump(FEATURE_NAMES, f, indent=2)
        results["feature_order_path"] = feature_order_path
        logger.info("Model saved to %s", model_path)

    return results
