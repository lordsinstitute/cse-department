from __future__ import annotations

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # 1 hour

    UPLOAD_FOLDER: str = os.path.join(BASE_DIR, "uploads")
    STATIC_PIMG: str = os.path.join(BASE_DIR, "static", "pimg")
    DATASET_PATH: str = os.path.join(BASE_DIR, "Dataset.csv")
    MODEL_PATH: str = os.path.join(BASE_DIR, "iot_spam_model.h5")

    ADMIN_USER: str = os.environ.get("ADMIN_USER", "admin")
    ADMIN_PASS: str = os.environ.get("ADMIN_PASS", "admin")
    USER_USER: str = os.environ.get("USER_USER", "user")
    USER_PASS: str = os.environ.get("USER_PASS", "user")

    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    SENTRY_DSN: str = os.environ.get("SENTRY_DSN", "")


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'dev.db')}"
    )
    LOG_LEVEL: str = "DEBUG"


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    TESTING: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'prod.db')}"
    )


config_map: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
