from __future__ import annotations

from loguru import logger

from src.automations.marketing_distribution.service import run_marketing_distribution


def run_marketing_distribution_job() -> dict:
    logger.info("Running scheduled marketing distribution job")
    return run_marketing_distribution(trigger="scheduler", force_sync=True)
