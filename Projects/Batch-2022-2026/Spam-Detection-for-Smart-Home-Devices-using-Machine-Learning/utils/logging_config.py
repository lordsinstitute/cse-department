from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask


def configure_logging(app: Flask) -> None:
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO").upper(), logging.INFO)

    formatter: logging.Formatter
    if app.debug:
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
    else:
        try:
            from pythonjsonlogger import jsonlogger

            formatter = jsonlogger.JsonFormatter(
                "%(timestamp)s %(level)s %(name)s %(message)s %(module)s %(funcName)s %(lineno)d"
            )
        except ImportError:
            formatter = logging.Formatter(
                '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}'
            )

    # Stream handler (always on)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    handlers: list[logging.Handler] = [stream_handler]

    # Rotating file handler in production
    if not app.debug:
        logs_dir = os.path.join(os.path.dirname(app.root_path), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, "app.log"),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        handlers.append(file_handler)

    app.logger.handlers.clear()
    for handler in handlers:
        app.logger.addHandler(handler)

    app.logger.setLevel(log_level)
    app.logger.propagate = False
    app.logger.info("Logging configured", extra={"log_level": app.config.get("LOG_LEVEL")})
