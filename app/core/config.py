"""
====================================================================
app/core/config.py — environment-driven configuration.
====================================================================

We never hardcode secrets/ports/hosts in source code. Instead we
read them from environment variables (or a .env file) using
pydantic-settings. This makes the same code run anywhere — laptop,
CI, production — just by changing env vars.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All configuration for the app, in one place.

    Each class attribute:
      - is the setting name (APP_NAME -> env var APP_NAME)
      - has a default used if the env var is missing
      - has a type that pydantic enforces (bool, int, str, ...)
    """

    # Look for a .env file in the current directory.
    # `extra="ignore"` lets unknown env vars exist without erroring.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Documents API"
    app_env: str = "development"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000


# A single shared settings instance imported across the app.
settings = Settings()