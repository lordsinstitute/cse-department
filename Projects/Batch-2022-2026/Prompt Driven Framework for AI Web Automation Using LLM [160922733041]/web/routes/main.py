"""Main routes: dashboard and history."""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from config import Config
from core.history import get_history, clear_history

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    recent = get_history(limit=5)
    return render_template("index.html", has_api_key=Config.has_api_key(),
                           recent_runs=recent, provider_name=Config.get_provider_name(),
                           api_key_env=Config.get_api_key_env_name())


@main_bp.route("/history")
@login_required
def history_page():
    return render_template("history.html")


@main_bp.route("/api/history")
@login_required
def api_history():
    runs = get_history(limit=100)
    return jsonify(runs)


@main_bp.route("/api/history/clear", methods=["POST"])
@login_required
def api_clear_history():
    clear_history()
    return jsonify({"status": "cleared"})
