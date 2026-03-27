"""
Training API: multi-dataset training with SVM, metrics, and run history.
"""

import os
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.data.datasets import (
    get_dataset_path,
    load_botiot_csv,
    load_cicids2018_csv,
    load_cicids_csv,
    load_nslkdd_csv,
    load_unsw_csv,
)
from app.data.features import FEATURE_NAMES
from app.database import get_db
from app.ml.attack_categories import ATTACK_LABELS
from app.ml.svm_pipeline import run_svm_pipeline
from app.models import TrainingRunDB

router = APIRouter(prefix="/api/training", tags=["training"])

DATASET_LOADERS = {
    "nsl_kdd": load_nslkdd_csv,
    "nslkdd": load_nslkdd_csv,
    "unsw": load_unsw_csv,
    "unsw_nb15": load_unsw_csv,
    "cicids": load_cicids_csv,
    "cicids2017": load_cicids_csv,
    "cicids2018": load_cicids2018_csv,
    "botiot": load_botiot_csv,
    "bot_iot": load_botiot_csv,
}


class TrainRequest(BaseModel):
    datasets: List[str]  # e.g. ["nsl_kdd", "cicids2017"]
    max_rows_per_dataset: Optional[int] = 100000
    test_size: float = 0.2
    val_size: float = 0.1
    class_weight: str = "balanced"
    C: float = 1.0


def _collect_features_and_labels(datasets: List[str], max_rows: Optional[int]) -> tuple:
    """Load all requested datasets and return (feature_rows, labels)."""
    feature_rows = []
    labels = []
    for ds_name in datasets:
        loader = DATASET_LOADERS.get(ds_name.lower())
        if not loader:
            continue
        path = get_dataset_path(ds_name)
        if not path or not os.path.isfile(path):
            continue
        for feat, label in loader(path, max_rows=max_rows):
            feature_rows.append(feat)
            labels.append(label)
    return feature_rows, labels


def _run_training_sync(
    datasets: List[str],
    max_rows: Optional[int],
    test_size: float,
    val_size: float,
    class_weight: str,
    C: float,
    run_id: int,
    db: Session,
):
    """Background task: run pipeline and update TrainingRunDB."""
    try:
        feature_rows, labels = _collect_features_and_labels(datasets, max_rows)
        if not feature_rows:
            db.query(TrainingRunDB).filter(TrainingRunDB.id == run_id).update(
                {"status": "failed", "metrics": '{"error": "No data loaded"}'}
            )
            db.commit()
            return
        results = run_svm_pipeline(
            feature_rows,
            labels,
            output_dir="models",
            test_size=test_size,
            val_size=val_size,
            save_model=True,
            class_weight=class_weight,
            C=C,
        )
        import json
        metrics = {
            "test_f1_weighted": results["test"]["f1_weighted"],
            "test_f1_macro": results["test"]["f1_macro"],
            "test_minority_recall": results["test"]["minority_recall"],
            "test_accuracy": results["test"]["accuracy"],
            "per_class_recall": results["test"].get("per_class_recall", {}),
        }
        db.query(TrainingRunDB).filter(TrainingRunDB.id == run_id).update(
            {
                "status": "completed",
                "metrics": json.dumps(metrics),
                "artifact_path": results.get("model_path", ""),
            }
        )
        db.commit()
    except Exception as e:
        import json
        db.query(TrainingRunDB).filter(TrainingRunDB.id == run_id).update(
            {"status": "failed", "metrics": json.dumps({"error": str(e)})}
        )
        db.commit()


@router.post("/run")
def start_training(
    req: TrainRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Start a training run (async). Returns run id and status."""
    import json
    run = TrainingRunDB(
        datasets=json.dumps(req.datasets),
        model_type="svm",
        metrics="{}",
        status="running",
        artifact_path="",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    background_tasks.add_task(
        _run_training_sync,
        req.datasets,
        req.max_rows_per_dataset,
        req.test_size,
        req.val_size,
        req.class_weight,
        req.C,
        run.id,
        db,
    )
    return {"run_id": run.id, "status": "running", "datasets": req.datasets}


@router.get("/runs")
def list_runs(db: Session = Depends(get_db), limit: int = 20):
    """List recent training runs."""
    import json
    rows = (
        db.query(TrainingRunDB)
        .order_by(TrainingRunDB.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "datasets": json.loads(r.datasets) if r.datasets else [],
            "model_type": r.model_type,
            "status": r.status,
            "metrics": json.loads(r.metrics) if r.metrics else {},
            "artifact_path": r.artifact_path,
        }
        for r in rows
    ]


@router.get("/datasets")
def list_datasets():
    """List supported dataset names and whether path is configured."""
    out = {}
    for name in ["nsl_kdd", "unsw", "unsw_nb15", "cicids", "cicids2017", "cicids2018", "botiot"]:
        path = get_dataset_path(name)
        out[name] = {"configured": path is not None, "path": path or ""}
    return out
