from __future__ import annotations

from typing import Any

from flask import Response, jsonify


def success_response(data: dict[str, Any], status_code: int = 200) -> tuple[Response, int]:
    return jsonify({"status": "success", "data": data}), status_code


def error_response(
    message: str, code: str = "ERROR", status_code: int = 400
) -> tuple[Response, int]:
    return jsonify({"status": "error", "message": message, "code": code}), status_code
