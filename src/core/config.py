from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    source_database_url: str | None = None
    target_database_url: str | None = None

    hunter_api_key: str | None = None
    clearbit_api_key: str | None = None
    apollo_api_key: str | None = None
    snov_api_key: str | None = None

    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from: str | None = None
    notify_email: str | None = None
    notify_on_success: bool = True
    notify_on_failure: bool = True

    sendgrid_api_key: str | None = None
    openai_api_key: str | None = None

    scheduler_timezone: str = "Asia/Jerusalem"

    log_level: str = "INFO"
    log_file: str = "logs/automation.log"

    environment: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
