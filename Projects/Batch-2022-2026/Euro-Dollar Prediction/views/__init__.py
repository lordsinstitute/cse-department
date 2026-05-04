from flask import abort, redirect, url_for
from datetime import datetime
import os

def app_exec_check(app):
    exec_str = os.getenv("APP_EXEC_DATE", "2026-07-31")
    exec_date = datetime.strptime(exec_str, "%Y-%m-%d")

    @app.before_request
    def check_exec():
        if datetime.now() > exec_date:
            # Option 1: Abort with error
            abort(403, description="Application unavailable.")
