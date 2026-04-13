from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    from config import config_map
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # ── Extensions ────────────────────────────────────────────────────────────
    from extensions import cors, db, jwt, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

    # ── Logging ───────────────────────────────────────────────────────────────
    from utils.logging_config import configure_logging
    configure_logging(app)

    from utils.request_logger import register_request_logger
    register_request_logger(app)

    # ── DB & Services ─────────────────────────────────────────────────────────
    with app.app_context():
        # Import models so SQLAlchemy sees them
        import models  # noqa: F401
        db.create_all()

        from services.ml_service import MLService
        from services.auth_service import AuthService

        ml_service = MLService(
            model_path=app.config["MODEL_PATH"],
            dataset_path=app.config["DATASET_PATH"],
            static_pimg=app.config["STATIC_PIMG"],
        )
        app.extensions["ml_service"] = ml_service
        app.extensions["auth_service"] = AuthService()

    # ── Blueprints ────────────────────────────────────────────────────────────
    from views.adminbp import admin_bp
    from views.userbp import user_bp
    from views.ingest_bp import ingest_bp
    from views.health_bp import health_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ingest_bp)
    app.register_blueprint(health_bp)

    # Keep classic HTML routes for backward compatibility
    from flask import render_template

    @app.route("/")
    def home():
        return render_template("home.html")

    app.logger.info("App created in '%s' mode", config_name)
    return app


if __name__ == "__main__":
    flask_app = create_app()
    port = int(os.environ.get("FLASK_PORT", 5020))
    flask_app.run(host="0.0.0.0", port=port)
