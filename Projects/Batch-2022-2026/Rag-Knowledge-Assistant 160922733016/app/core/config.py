import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "RAG Knowledge Assistant"
    DATABASE_URL: str = "sqlite:///./data/app.db"
    UPLOAD_DIR: str = "uploads"
    FAISS_INDEX_DIR: str = "data/faiss_indexes"
    SECRET_KEY: str = "change-this-to-a-secure-random-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Default LLM settings (can be overridden by admin via DB)
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    RETRIEVAL_TOP_K: int = 5
    LLM_TEMPERATURE: float = 0.0

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    class Config:
        env_file = ".env"


settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.FAISS_INDEX_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)
