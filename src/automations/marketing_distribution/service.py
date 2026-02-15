from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from loguru import logger

from src.automations.marketing_distribution import ingest_assets, publishers, storage
from src.automations.marketing_distribution.notifications import send_marketing_summary
from src.core.config import settings
from src.core.models import RunStatus


def run_marketing_distribution(
    *,
    trigger: str = "manual",
    target_date: date | None = None,
    force_sync: bool = False,
) -> dict:
    timezone = ZoneInfo(settings.scheduler_timezone)
    now_local = datetime.now(tz=timezone)
    effective_date = target_date or now_local.date()

    run = storage.create_marketing_run(trigger)
    summary: dict = {
        "run_id": run.id,
        "trigger": trigger,
        "target_date": effective_date.isoformat(),
        "queued": 0,
        "existing": 0,
        "published": 0,
        "failed": 0,
        "status": "running",
        "error": None,
    }

    try:
        posts = ingest_assets.load_social_posts(for_date=effective_date, force_sync=force_sync)
        logger.info(f"Loaded {len(posts)} marketing posts from assets")

        for draft in posts:
            _, created = storage.queue_social_post(run.id, draft)
            if created:
                summary["queued"] += 1
            else:
                summary["existing"] += 1

        due_posts = storage.list_due_posts(now=now_local)
        logger.info(f"Found {len(due_posts)} due marketing posts")

        for queued_post in due_posts:
            storage.mark_post_running(queued_post.id)
            result = publishers.publish_post(queued_post)
            if result.success:
                storage.mark_post_completed(queued_post.id)
                summary["published"] += 1
            else:
                storage.mark_post_failed(queued_post.id, result.error_message or "Unknown publish error")
                summary["failed"] += 1

        if summary["failed"] > 0:
            summary["status"] = RunStatus.failed.value
            storage.finalize_marketing_run(
                run.id,
                status=RunStatus.failed,
                error_message=f"{summary['failed']} posts failed",
            )
        else:
            summary["status"] = RunStatus.completed.value
            storage.finalize_marketing_run(run.id, status=RunStatus.completed)

        send_marketing_summary(summary)
        return summary
    except Exception as exc:  # noqa: BLE001
        summary["status"] = RunStatus.failed.value
        summary["error"] = str(exc)
        storage.finalize_marketing_run(run.id, status=RunStatus.failed, error_message=str(exc))
        send_marketing_summary(summary)
        logger.exception(f"Marketing distribution run failed: {exc}")
        raise
