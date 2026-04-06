from __future__ import annotations

import os

from flask import Blueprint, current_app, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from extensions import db
from models.dataset import Dataset
from models.model_version import ModelVersion
from utils.responses import error_response, success_response

admin_bp = Blueprint("admin_bp", __name__)


def _admin_required():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return error_response("Admin access required", "FORBIDDEN", 403)
    return None


# ── Auth ──────────────────────────────────────────────────────────────────────

@admin_bp.route("/api/admin/login", methods=["POST"])
def admin_login():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "")
    password = body.get("password", "")

    if not username or not password:
        return error_response("Username and password required", "MISSING_FIELDS")

    auth_service = current_app.extensions["auth_service"]
    user = auth_service.authenticate_admin(username, password)
    if not user:
        return error_response("Invalid credentials", "INVALID_CREDENTIALS", 401)

    token = create_access_token(identity=str(user.id), additional_claims={"role": "admin"})
    return success_response({"access_token": token, "role": "admin"})


@admin_bp.route("/api/admin/logout", methods=["POST"])
@jwt_required()
def admin_logout():
    denied = _admin_required()
    if denied:
        return denied
    return success_response({"message": "Logged out"})


# ── Dataset ───────────────────────────────────────────────────────────────────

ALLOWED_EXTENSIONS = {"csv"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route("/api/admin/upload", methods=["POST"])
@jwt_required()
def admin_upload():
    denied = _admin_required()
    if denied:
        return denied

    if "file" not in request.files:
        return error_response("No file part in request", "NO_FILE")

    f = request.files["file"]
    if not f.filename or not _allowed_file(f.filename):
        return error_response("Invalid file. Only .csv files are accepted.", "INVALID_FILE")

    from werkzeug.utils import secure_filename
    filename = secure_filename(f.filename)
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)
    f.save(file_path)

    # Copy as active dataset
    import shutil
    shutil.copy(file_path, current_app.config["DATASET_PATH"])

    # Count rows
    import pandas as pd
    try:
        row_count = len(pd.read_csv(file_path))
    except Exception:
        row_count = None

    # Deactivate previous datasets
    Dataset.query.update({"is_active": False})

    dataset = Dataset(
        filename=filename,
        file_path=file_path,
        row_count=row_count,
        is_active=True,
    )
    db.session.add(dataset)
    db.session.commit()
    current_app.logger.info("Dataset uploaded: %s (%s rows)", filename, row_count)

    return success_response({"dataset": dataset.to_dict()}, 201)


# ── ML ────────────────────────────────────────────────────────────────────────

@admin_bp.route("/api/admin/compare-algorithms", methods=["GET"])
@jwt_required()
def compare_algorithms():
    denied = _admin_required()
    if denied:
        return denied

    ml_service = current_app.extensions["ml_service"]
    try:
        results = ml_service.compare_algorithms()
    except Exception as exc:
        current_app.logger.error("Algorithm comparison failed: %s", exc)
        return error_response(str(exc), "COMPARISON_ERROR", 500)

    return success_response({"algorithms": results})


@admin_bp.route("/api/admin/create-model", methods=["POST"])
@jwt_required()
def create_model():
    denied = _admin_required()
    if denied:
        return denied

    ml_service = current_app.extensions["ml_service"]
    try:
        result = ml_service.create_model()
    except Exception as exc:
        current_app.logger.error("Model training failed: %s", exc)
        return error_response(str(exc), "TRAINING_ERROR", 500)

    # Count existing versions for versioning
    version_count = ModelVersion.query.count() + 1
    version_str = f"1.{version_count}.0"

    # Deactivate old models
    ModelVersion.query.update({"is_active": False})

    active_dataset = Dataset.query.filter_by(is_active=True).first()
    mv = ModelVersion(
        version=version_str,
        file_path=result["model_path"],
        accuracy=result["accuracy"],
        dataset_id=active_dataset.id if active_dataset else None,
        is_active=True,
    )
    db.session.add(mv)
    db.session.commit()

    return success_response({"accuracy": result["accuracy"], "model_version": mv.to_dict()})


@admin_bp.route("/api/admin/models", methods=["GET"])
@jwt_required()
def list_models():
    denied = _admin_required()
    if denied:
        return denied

    models = ModelVersion.query.order_by(ModelVersion.trained_at.desc()).all()
    return success_response({"models": [m.to_dict() for m in models]})


@admin_bp.route("/api/admin/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    denied = _admin_required()
    if denied:
        return denied

    from models.prediction import Prediction
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    active_dataset = Dataset.query.filter_by(is_active=True).first()
    total_predictions = Prediction.query.count()

    return success_response({
        "total_predictions": total_predictions,
        "active_model": active_model.to_dict() if active_model else None,
        "active_dataset": active_dataset.to_dict() if active_dataset else None,
    })
