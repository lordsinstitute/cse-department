from flask import Flask
from flask_socketio import SocketIO, join_room
from flask_login import LoginManager

socketio = SocketIO()
login_manager = LoginManager()


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    from config import Config
    app.config.from_object(Config)
    app.secret_key = app.config.get("SECRET_KEY", "prompt-web-auto-secret")

    socketio.init_app(app, cors_allowed_origins="*", async_mode="threading")

    # Flask-Login setup
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"
    login_manager.login_message = "Please sign in to access this page."
    login_manager.login_message_category = "error"

    from core.auth import get_user_by_id, init_auth_db, seed_default_user

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    # Initialize auth database and seed default user
    init_auth_db()
    seed_default_user()

    # Register blueprints
    from web.routes.auth import auth_bp
    from web.routes.main import main_bp
    from web.routes.scraper import scraper_bp
    from web.routes.form_filler import form_filler_bp
    from web.routes.settings import settings_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(scraper_bp, url_prefix="/scraper")
    app.register_blueprint(form_filler_bp, url_prefix="/form-filler")
    app.register_blueprint(settings_bp, url_prefix="/settings")

    @app.context_processor
    def inject_llm_status():
        return {
            "llm_has_api_key": Config.has_api_key(),
            "llm_provider_name": Config.get_provider_name(),
            "llm_api_key_env": Config.get_api_key_env_name(),
        }

    @socketio.on("join")
    def handle_join(data):
        room = data.get("room")
        if room:
            join_room(room)

    return app
