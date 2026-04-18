from web import create_app, socketio
from config import Config

Config.ensure_dirs()

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("  Prompt-Driven AI Web Automation")
    print("  http://localhost:5050")
    print("=" * 50)
    if not Config.has_api_key():
        print("  WARNING: ANTHROPIC_API_KEY not set!")
        print("  Copy .env.example to .env and add your key")
    print("=" * 50)
    socketio.run(app, host="0.0.0.0", port=5050, debug=True, allow_unsafe_werkzeug=True)
