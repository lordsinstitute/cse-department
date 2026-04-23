"""Scraper module routes."""

import os
import time
from flask import Blueprint, render_template, request, jsonify, send_file, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
from config import Config
from core.security import validate_url, agent_rate_limiter
from web import socketio

scraper_bp = Blueprint("scraper", __name__)

# Store active agents per room for stop functionality
active_agents = {}


@scraper_bp.route("/")
@login_required
def scraper_page():
    if not Config.has_api_key():
        flash(f"Please set your {Config.get_api_key_env_name()} in the .env file.", "error")
    return render_template("scraper.html")


@scraper_bp.route("/start", methods=["POST"])
@login_required
def start_scraping():
    data = request.get_json()
    url = data.get("url", "").strip()
    task = data.get("task", "").strip()
    room = data.get("room", "")

    if not Config.has_api_key():
        return jsonify({"error": f"{Config.get_api_key_env_name()} not configured."}), 400

    if not url:
        return jsonify({"error": "Please enter a URL."}), 400

    if not task:
        return jsonify({"error": "Please describe what data to extract."}), 400

    if not url.startswith("http"):
        url = "https://" + url

    # Security: validate URL
    is_valid, error = validate_url(url)
    if not is_valid:
        return jsonify({"error": error}), 400

    # Security: rate limiting
    client_ip = request.remote_addr or "unknown"
    allowed, retry_after = agent_rate_limiter.is_allowed(client_ip)
    if not allowed:
        return jsonify({"error": f"Too many requests. Please wait {retry_after} seconds."}), 429

    # Run agent in background via SocketIO
    socketio.start_background_task(
        target=_run_scraper_agent, url=url, task=task, room=room
    )

    return jsonify({"status": "started"})


@scraper_bp.route("/stop", methods=["POST"])
@login_required
def stop_scraping():
    data = request.get_json()
    room = data.get("room", "")
    agent = active_agents.get(room)
    if agent:
        agent.stop()
        return jsonify({"status": "stopping"})
    return jsonify({"status": "no active agent"})


@scraper_bp.route("/download/<filename>")
@login_required
def download_file(filename):
    # Security: sanitize filename and verify path
    filename = secure_filename(filename)
    if not filename:
        flash("Invalid filename.", "error")
        return redirect(url_for("scraper.scraper_page"))

    filepath = os.path.realpath(os.path.join(Config.EXPORT_DIR, filename))
    export_dir = os.path.realpath(Config.EXPORT_DIR)

    # Prevent path traversal
    if not filepath.startswith(export_dir):
        flash("Access denied.", "error")
        return redirect(url_for("scraper.scraper_page"))

    if not os.path.exists(filepath):
        flash("File not found.", "error")
        return redirect(url_for("scraper.scraper_page"))

    return send_file(filepath, as_attachment=True)


def _run_scraper_agent(url, task, room):
    """Background task to run the scraper agent."""
    from core.agents.scraper_agent import ScraperAgent
    from core.exporters.excel_exporter import export_to_excel
    from core.history import save_run

    agent = ScraperAgent(socketio=socketio, room=room)
    active_agents[room] = agent
    start_time = time.time()

    try:
        result = agent.run(start_url=url, task_description=task)
        duration = time.time() - start_time

        # Export collected data
        filename = None
        if agent.collected_data:
            try:
                filepath = export_to_excel(agent.collected_data)
                filename = os.path.basename(filepath)
                agent.emit_log(f"Exported {len(agent.collected_data)} items to {filename}", "success")
            except Exception as e:
                agent.emit_log(f"Export error: {str(e)}", "error")

        # Determine status
        if agent._stopped:
            status = "stopped"
        elif result["success"]:
            status = "success"
        else:
            status = "failed"

        # Save to history
        save_run(
            module="scraper",
            url=url,
            task_description=task,
            status=status,
            summary=result["summary"],
            steps=result["steps"],
            items_collected=len(agent.collected_data),
            download_filename=filename,
            duration_seconds=duration,
        )

        socketio.emit(
            "agent_complete",
            {
                "success": result["success"],
                "summary": result["summary"],
                "steps": result["steps"],
                "items_collected": len(agent.collected_data),
                "download_filename": filename,
            },
            room=room,
        )
    except Exception as e:
        duration = time.time() - start_time
        save_run(
            module="scraper",
            url=url,
            task_description=task,
            status="failed",
            summary=f"Error: {str(e)}",
            steps=0,
            duration_seconds=duration,
        )
        socketio.emit(
            "agent_complete",
            {"success": False, "summary": f"Error: {str(e)}", "steps": 0},
            room=room,
        )
    finally:
        active_agents.pop(room, None)
