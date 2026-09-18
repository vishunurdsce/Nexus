import pytest
from app.config import Settings


def test_development_allows_default_fallback_values():
    """Verify that in development mode, default fallback credentials pass validation."""
    settings = Settings(app_env="development")
    assert settings.app_env == "development"
    assert settings.database_url == "postgresql+asyncpg://postgres:password@localhost:5432/nexus"
    assert settings.jwt_secret == "dev-only-change-me"
    assert settings.admin_bootstrap_password == "ChangeMeNow!"


def test_default_app_env_is_production():
    """Verify default app_env is production and fails closed without configuration."""
    with pytest.raises(ValueError) as exc_info:
        # Default app_env is production, which detects default insecure credentials
        Settings()
    assert "detected in non-development mode" in str(exc_info.value)


@pytest.mark.parametrize(
    "insecure_pattern",
    [
        "dev-only-change-me",
        "ChangeMeNow!",
        "change-this-db-password",
        "replace-with-64-char-random-string",
        "your_long_random_secret",
        "password",
        "secret",
        "admin",
        "change_me",
    ],
)
def test_production_rejects_insecure_jwt_secret_patterns(insecure_pattern):
    with pytest.raises(ValueError, match="Insecure or default jwt_secret detected in non-development mode!"):
        Settings(
            app_env="production",
            database_url="postgresql+asyncpg://secure_user:complex_pass_123@prod-db:5432/nexus",
            jwt_secret=f"pre_{insecure_pattern}_post",
            admin_bootstrap_password="ValidStrongProdPassword!987",
        )


@pytest.mark.parametrize(
    "insecure_pattern",
    [
        "dev-only-change-me",
        "ChangeMeNow!",
        "change-this-db-password",
        "replace-with-64-char-random-string",
        "your_long_random_secret",
        "password",
        "secret",
        "admin",
        "change_me",
    ],
)
def test_production_rejects_insecure_admin_password_patterns(insecure_pattern):
    with pytest.raises(ValueError, match="Insecure or default admin_bootstrap_password detected in non-development mode!"):
        Settings(
            app_env="production",
            database_url="postgresql+asyncpg://secure_user:complex_pass_123@prod-db:5432/nexus",
            jwt_secret="valid_secure_jwt_token_prod_9999",
            admin_bootstrap_password=f"pre_{insecure_pattern}_post",
        )


@pytest.mark.parametrize(
    "insecure_pattern",
    [
        "dev-only-change-me",
        "ChangeMeNow!",
        "change-this-db-password",
        "replace-with-64-char-random-string",
        "your_long_random_secret",
        "password",
        "secret",
        "admin",
        "change_me",
    ],
)
def test_production_rejects_insecure_database_url_patterns(insecure_pattern):
    with pytest.raises(ValueError, match="Default database password detected in non-development mode!"):
        Settings(
            app_env="production",
            database_url=f"postgresql+asyncpg://secure_user:{insecure_pattern}@prod-db:5432/nexus",
            jwt_secret="valid_secure_jwt_token_prod_9999",
            admin_bootstrap_password="ValidStrongProdPassword!987",
        )


def test_production_accepts_valid_credentials():
    """Verify that production mode succeeds when all credentials are secure."""
    settings = Settings(
        app_env="production",
        database_url="postgresql+asyncpg://nexus_db_usr:k8x9Wz7qL2mP@prod-db.internal:5432/nexus_db",
        jwt_secret="k8x9Wz7qL2mPk8x9Wz7qL2mPk8x9Wz7qL2mP",
        admin_bootstrap_password="StrongPr0dCredentials!2026",
    )
    assert settings.app_env == "production"
    assert "k8x9Wz7qL2mP" in settings.jwt_secret
    assert settings.admin_bootstrap_password == "StrongPr0dCredentials!2026"
