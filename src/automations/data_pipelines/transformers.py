from __future__ import annotations

from typing import Any
from loguru import logger


def transform_customers(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []

    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        if not email:
            continue

        row["email"] = email
        key = email
        if key not in deduped:
            deduped[key] = row
            continue

        existing = deduped[key]
        if row.get("updated_at") and existing.get("updated_at"):
            if row["updated_at"] > existing["updated_at"]:
                deduped[key] = row

    normalized = list(deduped.values())
    logger.info(f"Transformed {len(rows)} rows into {len(normalized)} deduped rows")
    return normalized