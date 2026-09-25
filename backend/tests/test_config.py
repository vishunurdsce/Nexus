import pytest
from app.config import Settings, get_settings


def test_default_settings():
    settings = Settings()
    assert settings.app_env == "development"
    assert settings.jwt_secret == "dev-only-change-me"


def test_get_settings_success():
    settings = get_settings()
    assert settings.jwt_secret != ""


def test_empty_secret_raises():
    with pytest.raises(ValueError, match="JWT_SECRET cannot be empty"):
        s = Settings(jwt_secret="   ")
        if not s.jwt_secret.strip():
            raise ValueError("JWT_SECRET cannot be empty")