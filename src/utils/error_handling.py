from __future__ import annotations

import time
from collections.abc import Callable
from functools import wraps
from loguru import logger


class AutomationError(Exception):
    pass


class RetryableError(AutomationError):
    pass


def retry(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    exceptions: tuple[type[Exception], ...] = (RetryableError, Exception),
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(f"Retry exhausted for {func.__name__}: {exc}")
                        raise

                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    logger.warning(
                        f"Retrying {func.__name__} after error: {exc} (attempt {attempt}/{max_attempts})"
                    )
                    time.sleep(delay)

        return wrapper

    return decorator