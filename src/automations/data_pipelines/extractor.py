from __future__ import annotations

import argparse
from datetime import datetime
from typing import Any

from loguru import logger
from sqlalchemy import create_engine, text

from src.core.config import settings


def extract_customers(since: datetime | None = None) -> list[dict[str, Any]]:
    if not settings.source_database_url:
        raise ValueError("SOURCE_DATABASE_URL is not configured")

    engine = create_engine(settings.source_database_url, future=True)
    query = "SELECT id, email, first_name, last_name, updated_at FROM customers"
    params: dict[str, Any] = {}
    if since:
        query += " WHERE updated_at > :since"
        params["since"] = since

    with engine.connect() as conn:
        rows = conn.execute(text(query), params).mappings().all()
        logger.info(f"Extracted {len(rows)} customer rows")
        return [dict(row) for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract customer data")
    parser.add_argument("--since", type=str, default=None, help="ISO datetime for incremental load")
    parser.add_argument("--dry-run", action="store_true", help="Only log row count")
    args = parser.parse_args()

    since = datetime.fromisoformat(args.since) if args.since else None
    rows = extract_customers(since)

    if args.dry_run:
        logger.info("Dry run complete")
        return

    logger.info(f"Sample row: {rows[0] if rows else 'n/a'}")


if __name__ == "__main__":
    main()