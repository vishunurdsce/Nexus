from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"

    # Core Security
    jwt_secret: str = "dev-only-change-me"
    cookie_secure: bool = False
    chat_cookie: str = "nexus_chat"
    admin_cookie: str = "nexus_admin"
    csrf_cookie: str = "nexus_csrf"

    # Admin Bootstrap
    admin_bootstrap_email: str = "admin@nexus.local"
    admin_bootstrap_password: str = "ChangeMeNow!"

    # CORS & Origins
    chat_origin: str = "http://localhost:8080"
    admin_origin: str = "http://localhost:8081"
    api_cors_origins: str = "http://localhost:8080,http://localhost:8081"

    # Database & Storage
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/nexus"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "nexus_documents"

    # Ollama Models
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "llama3.2"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_vision_model: str = "llava:7b"
    enable_vision: bool = False
    embed_dim: int = 768

    # Uploads
    upload_dir: str = "./uploads"
    max_upload_mb: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    settings = Settings()
    if not settings.jwt_secret.strip():
        raise ValueError("JWT_SECRET cannot be empty")
    if not settings.admin_bootstrap_password.strip():
        raise ValueError("ADMIN_BOOTSTRAP_PASSWORD cannot be empty")
    if not settings.database_url.strip():
        raise ValueError("DATABASE_URL cannot be empty")
    return settings