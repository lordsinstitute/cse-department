"""
Imbalance-aware SVM training optimized for F1-score and minority recall.

Uses class_weight='balanced' and optional custom scoring for minority classes.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

from app.core.logging import get_logger
from app.data.features import FEATURE_NAMES, features_to_vector
from app.ml.attack_categories import ATTACK_LABELS

logger = get_logger(__name__)


def _minority_recall_scorer(estimator, X, y_true):
    """Custom scorer: minimum recall across all classes (minority recall)."""
    y_pred = estimator.predict(X)
    classes = np.unique(y_true)
    recalls = []
    for c in classes:
        mask = y_true == c
        if mask.sum() == 0:
            continue
        rec = recall_score(y_true[mask], y_pred[mask], labels=[c], average="micro", zero_division=0)
        recalls.append(rec)
    return float(np.min(recalls)) if recalls else 0.0


def _f1_weighted_scorer(estimator, X, y_true):
    return f1_score(y_true, estimator.predict(X), average="weighted", zero_division=0)


def load_training_data(
    feature_rows: List[Dict[str, float]],
    labels: List[str],
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, LabelEncoder, Optional[StandardScaler]]:
    """
    Build X, y from feature dicts and labels; split train/val/test; optionally scale.
    """
    X = np.array([features_to_vector(r, FEATURE_NAMES) for r in feature_rows], dtype=np.float64)
    le = LabelEncoder()
    le.fit(ATTACK_LABELS)
    y = []
    for lbl in labels:
        y.append(lbl if lbl in le.classes_ else "unknown")
    y = le.transform(y)

    X_rest, X_test, y_rest, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_rest, y_rest, test_size=val_ratio, random_state=random_state, stratify=y_rest
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    return X_train, X_val, X_test, y_train, y_val, y_test, le, scaler


def train_svm(
    X_train: np.ndarray,
    y_train: np.ndarray,
    class_weight: str = "balanced",
    kernel: str = "rbf",
    C: float = 1.0,
    gamma: str = "scale",
    probability: bool = True,
    calibrate: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Train a class-weighted SVM. If calibrate=True, wrap in CalibratedClassifierCV for predict_proba.
    """
    clf = SVC(
        kernel=kernel,
        C=C,
        gamma=gamma,
        class_weight=class_weight,
        probability=probability,
        random_state=42,
        **kwargs,
    )
    if calibrate and probability:
        clf = CalibratedClassifierCV(clf, method="isotonic", cv=3)
    clf.fit(X_train, y_train)
    return clf


def evaluate(
    model: Any,
    X: np.ndarray,
    y_true: np.ndarray,
    label_encoder: LabelEncoder,
) -> Dict[str, Any]:
    """Compute accuracy, precision, recall, F1 (weighted/macro), minority recall, confusion matrix."""
    y_pred = model.predict(X)
    n_classes = len(np.unique(y_true))
    average = "weighted" if n_classes > 2 else "binary"

    # Minority recall: min over per-class recalls
    classes = label_encoder.classes_
    per_class_recall = {}
    for i, c in enumerate(classes):
        mask = y_true == i
        if mask.sum() > 0:
            per_class_recall[c] = float(
                recall_score(y_true[mask], y_pred[mask], labels=[i], average="micro", zero_division=0)
            )
        else:
            per_class_recall[c] = 0.0
    minority_recall = float(np.min(list(per_class_recall.values()))) if per_class_recall else 0.0

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average=average, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average=average, zero_division=0)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "minority_recall": minority_recall,
        "per_class_recall": per_class_recall,
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "labels": list(classes),
        "classification_report": classification_report(
            y_true, y_pred, target_names=classes, zero_division=0
        ),
    }


def run_svm_pipeline(
    feature_rows: List[Dict[str, float]],
    labels: List[str],
    output_dir: str = "models",
    test_size: float = 0.2,
    val_size: float = 0.1,
    save_model: bool = True,
    class_weight: str = "balanced",
    C: float = 1.0,
) -> Dict[str, Any]:
    """
    Full SVM pipeline: scale, split, train with class_weight, evaluate, save.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    X_train, X_val, X_test, y_train, y_val, y_test, le, scaler = load_training_data(
        feature_rows, labels, test_size=test_size, val_size=val_size
    )

    model = train_svm(X_train, y_train, class_weight=class_weight, C=C)
    train_metrics = evaluate(model, X_train, y_train, le)
    val_metrics = evaluate(model, X_val, y_val, le)
    test_metrics = evaluate(model, X_test, y_test, le)

    results = {
        "train": train_metrics,
        "validation": val_metrics,
        "test": test_metrics,
        "feature_order": FEATURE_NAMES,
        "model_type": "svm",
    }

    if save_model:
        import joblib
        model_path = os.path.join(output_dir, "detector.joblib")
        joblib.dump({
            "model": model,
            "label_encoder": le,
            "scaler": scaler,
        }, model_path)
        results["model_path"] = model_path
        feature_order_path = os.path.join(output_dir, "feature_order.json")
        with open(feature_order_path, "w") as f:
            json.dump(FEATURE_NAMES, f, indent=2)
        results["feature_order_path"] = feature_order_path
        logger.info("SVM model saved to %s", model_path)

    return results
