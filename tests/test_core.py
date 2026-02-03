from src.core.config import settings


def test_settings_loads():
    assert settings.database_url
    assert settings.scheduler_timezone == "Asia/Jerusalem"