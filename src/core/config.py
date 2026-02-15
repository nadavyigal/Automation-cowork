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
    marketing_enabled: bool = True
    marketing_daily_run_hour: int = 8
    marketing_daily_run_minute: int = 5

    marketing_assets_repo_url: str | None = None
    marketing_assets_branch: str = "version-2-marketing"
    marketing_assets_local_dir: str = "runtime/marketing-assets"
    marketing_csv_relative_path: str = "docs/gtm/week-1-social-publishing-sheet.csv"
    marketing_execution_mode: str = "dry-run"

    linkedin_publisher_webhook_url: str | None = None
    x_publisher_webhook_url: str | None = None
    reddit_publisher_webhook_url: str | None = None
    community_publisher_webhook_url: str | None = None
    newsletter_publisher_webhook_url: str | None = None

    log_level: str = "INFO"
    log_file: str = "logs/automation.log"

    environment: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
