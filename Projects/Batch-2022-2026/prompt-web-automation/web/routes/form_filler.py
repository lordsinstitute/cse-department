"""Form filler module routes."""

import os
import time
from flask import Blueprint, render_template, request, jsonify, send_from_directory, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
from config import Config
from core.security import validate_url, agent_rate_limiter
from web import socketio

form_filler_bp = Blueprint("form_filler", __name__)

active_agents = {}


@form_filler_bp.route("/")
@login_required
def form_filler_page():
    if not Config.has_api_key():
        flash(f"Please set your {Config.get_api_key_env_name()} in the .env file.", "error")
    return render_template("form_filler.html")


@form_filler_bp.route("/demo-form")
def demo_form():
    """Serve the built-in demo job application form."""
    demo_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "demo")
    return send_from_directory(demo_dir, "sample_form.html")


@form_filler_bp.route("/upload-resume", methods=["POST"])
@login_required
def upload_resume():
    """Upload and parse a PDF resume."""
    if not Config.has_api_key():
        return jsonify({"error": f"{Config.get_api_key_env_name()} not configured."}), 400

    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files["resume"]
    if not file.filename:
        return jsonify({"error": "No file selected."}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported."}), 400

    # Security: check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > Config.MAX_UPLOAD_SIZE:
        max_mb = Config.MAX_UPLOAD_SIZE // (1024 * 1024)
        return jsonify({"error": f"File too large. Maximum size is {max_mb}MB."}), 400

    # Save file
    filename = secure_filename(file.filename)
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(Config.UPLOAD_DIR, filename)
    file.save(filepath)

    try:
        from core.parsers.pdf_parser import parse_resume
        resume_data = parse_resume(filepath)
        return jsonify({"success": True, "data": resume_data})
    except Exception as e:
        return jsonify({"error": f"Failed to parse resume: {str(e)}"}), 500
    finally:
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except OSError:
            pass


@form_filler_bp.route("/start", methods=["POST"])
@login_required
def start_filling():
    """Start the form filler agent."""
    data = request.get_json()
    url = data.get("url", "").strip()
    resume_data = data.get("resume_data", {})
    room = data.get("room", "")

    if not Config.has_api_key():
        return jsonify({"error": f"{Config.get_api_key_env_name()} not configured."}), 400

    if not url:
        return jsonify({"error": "Please enter a form URL."}), 400

    if not resume_data:
        return jsonify({"error": "No resume data provided. Upload a resume first."}), 400

    if not url.startswith("http"):
        url = "https://" + url

    # Security: validate URL (allow localhost for demo form)
    is_valid, error = validate_url(url, allow_localhost=True)
    if not is_valid:
        return jsonify({"error": error}), 400

    # Security: rate limiting
    client_ip = request.remote_addr or "unknown"
    allowed, retry_after = agent_rate_limiter.is_allowed(client_ip)
    if not allowed:
        return jsonify({"error": f"Too many requests. Please wait {retry_after} seconds."}), 429

    socketio.start_background_task(
        target=_run_form_filler_agent, url=url, resume_data=resume_data, room=room
    )

    return jsonify({"status": "started"})


@form_filler_bp.route("/stop", methods=["POST"])
@login_required
def stop_filling():
    data = request.get_json()
    room = data.get("room", "")
    agent = active_agents.get(room)
    if agent:
        agent.stop()
        return jsonify({"status": "stopping"})
    return jsonify({"status": "no active agent"})


def _run_form_filler_agent(url, resume_data, room):
    """Background task to run the form filler agent."""
    from core.agents.form_filler_agent import FormFillerAgent
    from core.history import save_run

    agent = FormFillerAgent(resume_data=resume_data, socketio=socketio, room=room)
    active_agents[room] = agent
    start_time = time.time()
    task_desc = "Fill out the web form with the provided resume data. Match each form field to the appropriate data and fill it in. Then submit the form."

    try:
        result = agent.run(start_url=url, task_description=task_desc)
        duration = time.time() - start_time

        # Determine status
        if agent._stopped:
            status = "stopped"
        elif result["success"]:
            status = "success"
        else:
            status = "failed"

        # Save to history
        save_run(
            module="form_filler",
            url=url,
            task_description="Form fill with resume data",
            status=status,
            summary=result["summary"],
            steps=result["steps"],
            duration_seconds=duration,
        )

        socketio.emit(
            "agent_complete",
            {
                "success": result["success"],
                "summary": result["summary"],
                "steps": result["steps"],
            },
            room=room,
        )
    except Exception as e:
        duration = time.time() - start_time
        save_run(
            module="form_filler",
            url=url,
            task_description="Form fill with resume data",
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
