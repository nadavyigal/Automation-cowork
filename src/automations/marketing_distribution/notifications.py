from __future__ import annotations

from datetime import datetime

from loguru import logger

from src.automations.lead_enrichment.notifications import send_email
from src.core.config import settings


def send_marketing_summary(summary: dict) -> None:
    if not settings.notify_email:
        return

    subject = (
        f"Marketing Distribution Run {summary.get('status', 'unknown').upper()} "
        f"({summary.get('trigger', 'manual')})"
    )

    body = "\n".join(
        [
            f"Timestamp: {datetime.utcnow().isoformat()}Z",
            f"Run ID: {summary.get('run_id')}",
            f"Trigger: {summary.get('trigger')}",
            f"Target Date: {summary.get('target_date')}",
            f"Queued: {summary.get('queued', 0)}",
            f"Existing: {summary.get('existing', 0)}",
            f"Published: {summary.get('published', 0)}",
            f"Failed: {summary.get('failed', 0)}",
            f"Status: {summary.get('status')}",
            f"Error: {summary.get('error') or 'None'}",
        ]
    )

    try:
        send_email(subject=subject, body=body, to_address=settings.notify_email)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"Failed to send marketing summary notification: {exc}")
