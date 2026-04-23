import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "prompt-web-auto-secret-key")

    # LLM Provider: "claude" or "gemini"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude")

    # Claude (Anthropic)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    # Gemini (Google)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

    MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS", "25"))
    STEP_DELAY = float(os.getenv("STEP_DELAY", "1.0"))

    UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
    EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")

    NAVIGATION_TIMEOUT = 30000  # 30 seconds in ms
    SCREENSHOT_QUALITY = 50
    VISIBLE_TEXT_LIMIT = 2000
    MAX_CONSECUTIVE_ERRORS = 3

    # Rate limit backoff
    RATE_LIMIT_DELAYS = [2, 4, 8]

    # Security
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
        os.makedirs(cls.EXPORT_DIR, exist_ok=True)

    @classmethod
    def has_api_key(cls):
        """Check if the active provider's API key is configured."""
        if cls.LLM_PROVIDER.lower() == "gemini":
            return bool(cls.GEMINI_API_KEY)
        return bool(cls.ANTHROPIC_API_KEY)

    @classmethod
    def get_provider_name(cls):
        """Return display name of the active LLM provider."""
        return "Gemini" if cls.LLM_PROVIDER.lower() == "gemini" else "Claude"

    @classmethod
    def get_api_key_env_name(cls):
        """Return the env variable name for the active provider's API key."""
        if cls.LLM_PROVIDER.lower() == "gemini":
            return "GEMINI_API_KEY"
        return "ANTHROPIC_API_KEY"
