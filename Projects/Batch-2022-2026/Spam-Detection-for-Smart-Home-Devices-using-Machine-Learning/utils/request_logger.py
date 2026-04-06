from __future__ import annotations

import time

from flask import Flask, g, request


def register_request_logger(app: Flask) -> None:
    @app.before_request
    def before_request() -> None:
        g.start_time = time.monotonic()

    @app.after_request
    def after_request(response):
        duration_ms = round((time.monotonic() - g.start_time) * 1000, 2)
        app.logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
                "remote_addr": request.remote_addr,
            },
        )
        return response
