from __future__ import annotations

from functools import lru_cache
from typing import List, Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings and environment configuration loader.

    Reads variables from environment or .env file and validates credentials
    to prevent insecure deployment defaults outside of development mode.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Environment mode
    app_env: str = "development"

    # Database & Services
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    ollama_url: str = "http://localhost:11434"

    # Security & Authentication
    jwt_secret: str
    cookie_secure: bool = False
    chat_cookie: str = "nexus_chat"
    admin_cookie: str = "nexus_admin"
    csrf_cookie: str = "nexus_csrf"

    # Admin Bootstrap
    admin_bootstrap_email: str = "admin@nexus.local"
    admin_bootstrap_password: str

    # CORS & Origins
    chat_origin: str = "http://localhost:8080"
    admin_origin: str = "http://localhost:8081"
    api_cors_origins: str = "http://localhost:8080,http://localhost:8081"

    # LLM & Embeddings
    llm_provider: str = "ollama"
    groq_api_key: Optional[str] = None
    groq_llm_model: str = "llama-3.1-70b-versatile"
    gemini_api_key: Optional[str] = None

    ollama_llm_model: str = "qwen2.5:7b-instruct-q4_K_M"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_vision_model: str = "llava:7b"
    enable_vision: bool = False
    embed_dim: int = 768
    qdrant_collection: str = "nexus_chunks"
    upload_dir: str = "/data/uploads"
    max_upload_mb: int = 50

    @model_validator(mode="after")
    def validate_production_credentials(self) -> Settings:
        """Validate that non-development environments do not use default or insecure secrets.

        Raises:
            ValueError: If insecure or default secrets are detected when APP_ENV is not 'development'.
        """
        insecure_patterns = {
            "dev-only-change-me",
            "ChangeMeNow!",
            "change-this-db-password",
            "replace-with-64-char-random-string",
        }

        if self.app_env.lower() != "development":
            if any(p in self.jwt_secret for p in insecure_patterns):
                raise ValueError("Insecure or default jwt_secret detected in non-development mode!")
            if any(p in self.admin_bootstrap_password for p in insecure_patterns):
                raise ValueError("Insecure or default admin_bootstrap_password detected in non-development mode!")
            if any(p in self.database_url for p in insecure_patterns):
                raise ValueError("Default database password detected in non-development mode!")

        return self

    @property
    def cors_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list.

        Returns:
            List[str]: Cleaned list of allowed origin strings.
        """
        return [o.strip() for o in self.api_cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Retrieve and cache application settings instance.

    Returns:
        Settings: Singleton configuration object.
    """
    return Settings()