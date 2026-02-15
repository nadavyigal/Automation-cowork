from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from src.core.config import settings
from src.automations.data_pipelines.etl_job import run_etl_job
from src.automations.marketing_distribution.scheduler import run_marketing_distribution_job


def start_scheduler() -> BackgroundScheduler:
    timezone = ZoneInfo(settings.scheduler_timezone)
    scheduler = BackgroundScheduler(timezone=timezone)

    scheduler.add_job(
        run_etl_job,
        trigger=CronTrigger(hour=2, minute=0, timezone=timezone),
        id="daily_etl",
        replace_existing=True,
    )

    if settings.marketing_enabled:
        scheduler.add_job(
            run_marketing_distribution_job,
            trigger=CronTrigger(
                hour=settings.marketing_daily_run_hour,
                minute=settings.marketing_daily_run_minute,
                timezone=timezone,
            ),
            id="daily_marketing_distribution",
            replace_existing=True,
        )

    scheduler.start()
    next_run = scheduler.get_job("daily_etl").next_run_time
    logger.info(f"Scheduler started. Next ETL run: {next_run}")
    if settings.marketing_enabled:
        marketing_next_run = scheduler.get_job("daily_marketing_distribution").next_run_time
        logger.info(f"Next marketing run: {marketing_next_run}")
    return scheduler


if __name__ == "__main__":
    logger.info(f"Starting scheduler at {datetime.now(tz=ZoneInfo(settings.scheduler_timezone))}")
    start_scheduler()
    try:
        import time

        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")
