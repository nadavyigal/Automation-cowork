from __future__ import annotations

import os
import sys
from loguru import logger

from src.core.config import settings


def setup_logger() -> None:
    log_level = settings.log_level.upper()
    log_file = settings.log_file

    logger.remove()
    logger.add(sys.stdout, level=log_level, enqueue=True, backtrace=False, diagnose=False)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logger.add(log_file, level=log_level, enqueue=True, rotation="10 MB", retention="7 days")


setup_logger()