from __future__ import annotations

from typing import Any

from loguru import logger
from sqlalchemy import create_engine, text

from src.core.config import settings


def _ensure_table(engine) -> None:
    create_sql = """
    CREATE TABLE IF NOT EXISTS analytics_customers (
        id BIGINT PRIMARY KEY,
        email TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        updated_at TIMESTAMP
    )
    """
    with engine.begin() as conn:
        conn.execute(text(create_sql))


def load_customers(rows: list[dict[str, Any]]) -> int:
    if not settings.target_database_url:
        raise ValueError("TARGET_DATABASE_URL is not configured")

    if not rows:
        return 0

    engine = create_engine(settings.target_database_url, future=True)
    _ensure_table(engine)

    insert_sql = """
    INSERT INTO analytics_customers (id, email, first_name, last_name, updated_at)
    VALUES (:id, :email, :first_name, :last_name, :updated_at)
    ON CONFLICT (id) DO UPDATE SET
        email = EXCLUDED.email,
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        updated_at = EXCLUDED.updated_at
    """

    with engine.begin() as conn:
        conn.execute(text(insert_sql), rows)

    logger.info(f"Loaded {len(rows)} rows into analytics_customers")
    return len(rows)