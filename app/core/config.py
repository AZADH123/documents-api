from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """12-factor config: real env vars override .env, which overrides defaults."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # app
    app_name: str = "Documents API"
    app_version: str = "0.1.0"
    environment: str = "development"      # development | staging | production
    debug: bool = False

    # server
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"

    # api
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = []          # JSON list in env, e.g. CORS_ORIGINS='["http://localhost:3000"]'


@lru_cache
def get_settings() -> Settings:
    return Settings()