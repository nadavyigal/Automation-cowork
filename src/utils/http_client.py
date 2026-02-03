from __future__ import annotations

from typing import Any
import requests
from loguru import logger

from src.utils.error_handling import retry


class HttpClient:
    def __init__(self, timeout: tuple[int, int] = (5, 30)):
        self.timeout = timeout
        self.session = requests.Session()

    @retry(max_attempts=3)
    def get(self, url: str, headers: dict[str, str] | None = None, params: dict | None = None) -> Any:
        logger.debug(f"HTTP GET {url}")
        response = self.session.get(url, headers=headers, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @retry(max_attempts=3)
    def post(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        json: dict | None = None,
        data: dict | None = None,
    ) -> Any:
        logger.debug(f"HTTP POST {url}")
        response = self.session.post(
            url, headers=headers, json=json, data=data, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()