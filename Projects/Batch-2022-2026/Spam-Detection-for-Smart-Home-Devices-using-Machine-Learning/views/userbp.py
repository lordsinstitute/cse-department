from __future__ import annotations

from flask import Blueprint, current_app, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from extensions import db
from models.model_version import ModelVersion
from models.prediction import Prediction
from utils.responses import error_response, success_response

user_bp = Blueprint("user_bp", __name__)

# ── Auth ──────────────────────────────────────────────────────────────────────

@user_bp.route("/api/user/login", methods=["POST"])
def user_login():
    body = request.get_json(silent=True) or {}
    username = body.get("username", "")
    password = body.get("password", "")

    if not username or not password:
        return error_response("Username and password required", "MISSING_FIELDS")

    auth_service = current_app.extensions["auth_service"]
    user = auth_service.authenticate_user(username, password)
    if not user:
        return error_response("Invalid credentials", "INVALID_CREDENTIALS", 401)

    token = create_access_token(
        identity=str(user.id), additional_claims={"role": user.role}
    )
    return success_response({"access_token": token, "role": user.role})


@user_bp.route("/api/user/logout", methods=["POST"])
@jwt_required()
def user_logout():
    return success_response({"message": "Logged out"})


# ── Predict ───────────────────────────────────────────────────────────────────

@user_bp.route("/api/user/predict", methods=["POST"])
@jwt_required()
def predict():
    body = request.get_json(silent=True) or {}
    parameters = body.get("parameters")

    if not parameters or not isinstance(parameters, list) or len(parameters) != 10:
        return error_response(
            "Must provide 'parameters': array of exactly 10 numeric values",
            "INVALID_PARAMETERS", 422,
        )

    try:
        params = [float(v) for v in parameters]
    except (TypeError, ValueError):
        return error_response("All parameter values must be numeric", "INVALID_PARAMETERS", 422)

    ml_service = current_app.extensions["ml_service"]
    try:
        result = ml_service.predict(params)
    except RuntimeError as exc:
        return error_response(str(exc), "MODEL_NOT_READY", 503)

    # Persist prediction
    user_id = get_jwt_identity()
    active_model = ModelVersion.query.filter_by(is_active=True).first()
    pred = Prediction(
        user_id=int(user_id) if user_id else None,
        result=result,
        source="manual",
        model_version_id=active_model.id if active_model else None,
    )
    pred.set_parameters(params)
    db.session.add(pred)
    db.session.commit()

    return success_response({
        "prediction": result,
        "label": "spam" if result == 1 else "valid",
        "prediction_id": pred.id,
    })


@user_bp.route("/api/user/predictions", methods=["GET"])
@jwt_required()
def prediction_history():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    paginated = (
        Prediction.query.filter_by(user_id=int(user_id))
        .order_by(Prediction.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return success_response({
        "predictions": [p.to_dict() for p in paginated.items],
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages,
    })
