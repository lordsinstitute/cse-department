"""Settings routes: LLM provider and API key configuration."""

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from config import Config

settings_bp = Blueprint("settings", __name__)

ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")


def _read_env():
    """Read .env file as a dict."""
    env = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    env[key.strip()] = value.strip()
    return env


def _write_env(env):
    """Write dict back to .env file."""
    lines = []
    for key, value in env.items():
        lines.append(f"{key}={value}")
    with open(ENV_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")


def _mask_key(key):
    """Mask API key for display: show first 8 and last 4 chars."""
    if not key or len(key) < 16:
        return key or ""
    return key[:8] + "•" * (len(key) - 12) + key[-4:]


@settings_bp.route("/")
@login_required
def settings_page():
    return render_template(
        "settings.html",
        provider=Config.LLM_PROVIDER,
        provider_name=Config.get_provider_name(),
        has_claude_key=bool(Config.ANTHROPIC_API_KEY),
        has_gemini_key=bool(Config.GEMINI_API_KEY),
        claude_key_masked=_mask_key(Config.ANTHROPIC_API_KEY),
        gemini_key_masked=_mask_key(Config.GEMINI_API_KEY),
        claude_model=Config.CLAUDE_MODEL,
        gemini_model=Config.GEMINI_MODEL,
    )


@settings_bp.route("/save", methods=["POST"])
@login_required
def save_settings():
    provider = request.form.get("llm_provider", "claude").strip().lower()
    claude_key = request.form.get("anthropic_api_key", "").strip()
    gemini_key = request.form.get("gemini_api_key", "").strip()
    claude_model = request.form.get("claude_model", "").strip()
    gemini_model = request.form.get("gemini_model", "").strip()

    # Read existing .env
    env = _read_env()

    # Update provider
    env["LLM_PROVIDER"] = provider
    Config.LLM_PROVIDER = provider

    # Update Claude key (only if not the masked placeholder)
    if claude_key and "•" not in claude_key:
        env["ANTHROPIC_API_KEY"] = claude_key
        Config.ANTHROPIC_API_KEY = claude_key
    elif not claude_key:
        env.pop("ANTHROPIC_API_KEY", None)
        Config.ANTHROPIC_API_KEY = ""

    # Update Gemini key
    if gemini_key and "•" not in gemini_key:
        env["GEMINI_API_KEY"] = gemini_key
        Config.GEMINI_API_KEY = gemini_key
    elif not gemini_key:
        env.pop("GEMINI_API_KEY", None)
        Config.GEMINI_API_KEY = ""

    # Update models
    if claude_model:
        env["CLAUDE_MODEL"] = claude_model
        Config.CLAUDE_MODEL = claude_model
    if gemini_model:
        env["GEMINI_MODEL"] = gemini_model
        Config.GEMINI_MODEL = gemini_model

    # Write to .env
    _write_env(env)

    # Validate active provider has a key
    if not Config.has_api_key():
        flash(f"Warning: {Config.get_provider_name()} is selected but no API key is set.", "warning")
    else:
        flash(f"Settings saved. Using {Config.get_provider_name()} as LLM provider.", "success")

    return redirect(url_for("settings.settings_page"))


@settings_bp.route("/api/status")
@login_required
def api_status():
    """Return current LLM configuration status."""
    return jsonify({
        "has_api_key": Config.has_api_key(),
        "provider": Config.LLM_PROVIDER,
        "provider_name": Config.get_provider_name(),
        "api_key_env": Config.get_api_key_env_name(),
    })
