from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger


def run_automations_parallel(automation_configs: list[dict]):
    if not automation_configs:
        logger.warning("No automations provided")
        return []

    results = []
    with ThreadPoolExecutor(max_workers=len(automation_configs)) as executor:
        futures = {
            executor.submit(config["function"]): config["name"] for config in automation_configs
        }

        for future in as_completed(futures):
            automation_name = futures[future]
            try:
                result = future.result()
                logger.info(f"? {automation_name} completed: {result}")
                results.append((automation_name, result, None))
            except Exception as exc:
                logger.error(f"? {automation_name} failed: {exc}")
                results.append((automation_name, None, exc))

    return results