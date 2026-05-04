from __future__ import annotations

"""
Data Ingestion API
==================
Provides three endpoints for bulk/automated spam detection:

  POST /api/ingest          – single JSON record
  POST /api/ingest/batch    – multiple JSON records
  POST /api/ingest/csv      – CSV file upload; returns JSON or downloadable CSV
"""

import io

from flask import Blueprint, current_app, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models.model_version import ModelVersion
from models.prediction import Prediction
from utils.responses import error_response, success_response

ingest_bp = Blueprint("ingest_bp", __name__)

_PARAM_COUNT = 10


def _validate_record(record: list) -> list[float] | None:
    if not isinstance(record, list) or len(record) != _PARAM_COUNT:
        return None
    try:
        return [float(v) for v in record]
    except (TypeError, ValueError):
        return None


def _save_predictions(
    records: list[list[float]],
    results: list[int],
    user_id: int | None,
    source: str,
    active_model: ModelVersion | None,
) -> list[Prediction]:
    preds: list[Prediction] = []
    for params, result in zip(records, results):
        p = Prediction(
            user_id=user_id,
            result=result,
            source=source,
            model_version_id=active_model.id if active_model else None,
        )
        p.set_parameters(params)
        db.session.add(p)
        preds.append(p)
    db.session.commit()
    return preds


# ── Single record ─────────────────────────────────────────────────────────────

@ingest_bp.route("/api/ingest", methods=["POST"])
@jwt_required()
def ingest_single():
    """
    Accepts a single IoT record as JSON.

    Request body:
        {"parameters": [f0, f1, ..., f9]}

    Response:
        {"prediction": 0|1, "label": "valid"|"spam", "prediction_id": int}
    """
    body = request.get_json(silent=True) or {}
    record = _validate_record(body.get("parameters"))
    if record is None:
        return error_response(
            f"'parameters' must be an array of exactly {_PARAM_COUNT} numeric values",
            "INVALID_PARAMETERS", 422,
        )

    ml_service = current_app.extensions["ml_service"]
    try:
        result = ml_service.predict(record)
    except RuntimeError as exc:
        return error_response(str(exc), "MODEL_NOT_READY", 503)

    user_id = get_jwt_identity()
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    preds = _save_predictions([record], [result], int(user_id) if user_id else None, "api", active_model)

    return success_response({
        "prediction": result,
        "label": "spam" if result == 1 else "valid",
        "prediction_id": preds[0].id,
    })


# ── Batch records ─────────────────────────────────────────────────────────────

@ingest_bp.route("/api/ingest/batch", methods=["POST"])
@jwt_required()
def ingest_batch():
    """
    Accepts multiple IoT records as JSON.

    Request body:
        {"records": [[f0..f9], [f0..f9], ...]}

    Response:
        {"results": [{"index": 0, "prediction": 0, "label": "valid", "prediction_id": int}, ...]}
    """
    body = request.get_json(silent=True) or {}
    raw_records = body.get("records")

    if not isinstance(raw_records, list) or len(raw_records) == 0:
        return error_response("'records' must be a non-empty array", "INVALID_PARAMETERS", 422)

    if len(raw_records) > 1000:
        return error_response("Batch size limit is 1000 records", "BATCH_TOO_LARGE", 422)

    validated: list[list[float]] = []
    for i, rec in enumerate(raw_records):
        parsed = _validate_record(rec)
        if parsed is None:
            return error_response(
                f"Record at index {i} is invalid. Each record must be {_PARAM_COUNT} numeric values.",
                "INVALID_PARAMETERS", 422,
            )
        validated.append(parsed)

    ml_service = current_app.extensions["ml_service"]
    try:
        results = ml_service.predict_batch(validated)
    except RuntimeError as exc:
        return error_response(str(exc), "MODEL_NOT_READY", 503)

    user_id = get_jwt_identity()
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    preds = _save_predictions(
        validated, results, int(user_id) if user_id else None, "api", active_model
    )

    return success_response({
        "results": [
            {
                "index": i,
                "prediction": r,
                "label": "spam" if r == 1 else "valid",
                "prediction_id": preds[i].id,
            }
            for i, r in enumerate(results)
        ],
        "total": len(results),
        "spam_count": sum(results),
        "valid_count": len(results) - sum(results),
    })


# ── CSV file ──────────────────────────────────────────────────────────────────

@ingest_bp.route("/api/ingest/csv", methods=["POST"])
@jwt_required()
def ingest_csv():
    """
    Accepts a CSV file where each row contains 10 PCA component columns
    (p0, p1, ..., p9) or unnamed columns in that order.

    Query params:
        format=json   → returns JSON (default)
        format=csv    → returns the CSV with a 'prediction' column appended

    Request: multipart/form-data with field 'file' (.csv)
    """
    if "file" not in request.files:
        return error_response("No file part in request", "NO_FILE")

    f = request.files["file"]
    if not f.filename or not f.filename.lower().endswith(".csv"):
        return error_response("Only .csv files are accepted", "INVALID_FILE")

    import pandas as pd

    try:
        df = pd.read_csv(f)
    except Exception as exc:
        return error_response(f"Could not parse CSV: {exc}", "PARSE_ERROR", 422)

    # Accept either named columns (p0..p9) or positional (first 10 cols)
    param_cols = [f"p{i}" for i in range(_PARAM_COUNT)]
    if all(col in df.columns for col in param_cols):
        feature_df = df[param_cols]
    elif len(df.columns) >= _PARAM_COUNT:
        feature_df = df.iloc[:, :_PARAM_COUNT]
    else:
        return error_response(
            f"CSV must have at least {_PARAM_COUNT} columns or columns named p0–p9",
            "INVALID_COLUMNS", 422,
        )

    if len(feature_df) == 0:
        return error_response("CSV has no data rows", "EMPTY_FILE", 422)

    if len(feature_df) > 5000:
        return error_response("CSV row limit is 5000", "FILE_TOO_LARGE", 422)

    try:
        records = feature_df.astype(float).values.tolist()
    except ValueError:
        return error_response("All feature columns must be numeric", "INVALID_DATA", 422)

    ml_service = current_app.extensions["ml_service"]
    try:
        results = ml_service.predict_batch(records)
    except RuntimeError as exc:
        return error_response(str(exc), "MODEL_NOT_READY", 503)

    user_id = get_jwt_identity()
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    preds = _save_predictions(
        records, results, int(user_id) if user_id else None, "csv", active_model
    )

    fmt = request.args.get("format", "json").lower()

    if fmt == "csv":
        df["prediction"] = results
        df["label"] = ["spam" if r == 1 else "valid" for r in results]
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        response = make_response(csv_buf.getvalue())
        response.headers["Content-Type"] = "text/csv"
        response.headers["Content-Disposition"] = "attachment; filename=predictions.csv"
        return response

    return success_response({
        "results": [
            {
                "row": i,
                "prediction": r,
                "label": "spam" if r == 1 else "valid",
                "prediction_id": preds[i].id,
            }
            for i, r in enumerate(results)
        ],
        "total": len(results),
        "spam_count": sum(results),
        "valid_count": len(results) - sum(results),
    })
