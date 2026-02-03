from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any
from loguru import logger

from src.core.config import settings
from src.utils.api_usage import check_and_increment
from src.utils.http_client import HttpClient


@dataclass
class ProviderResult:
    provider: str
    data: dict | None


@dataclass
class Provider:
    name: str
    func: Callable[[dict], dict | None]


client = HttpClient()


PROVIDER_LIMITS: dict[str, dict] = {
    "hunter": {"limit": 100, "period_days": 30},
    "clearbit": {"limit": 50, "period_days": 30},
    "apollo": {"limit": 10, "period_days": 30},
    "snov": {"limit": 50, "period_days": 30},
}


def _within_quota(provider: str, endpoint: str) -> bool:
    config = PROVIDER_LIMITS.get(provider, {})
    limit = config.get("limit")
    period_days = config.get("period_days", 30)

    allowed, count, period_end = check_and_increment(provider, endpoint, limit, period_days)
    if not allowed:
        logger.warning(
            f"Provider {provider} over quota ({count}/{limit}). Next reset: {period_end}"
        )
        return False
    return True


def _call_hunter(payload: dict) -> dict | None:
    if not settings.hunter_api_key:
        return None

    email = payload.get("email")
    domain = payload.get("domain") or (email.split("@")[-1] if email and "@" in email else None)
    if not domain:
        return None

    url = "https://api.hunter.io/v2/email-finder"
    if not _within_quota("hunter", url):
        return None
    params = {
        "domain": domain,
        "first_name": payload.get("first_name") or payload.get("name", "").split(" ")[0],
        "last_name": payload.get("last_name") or " ".join(payload.get("name", "").split(" ")[1:]),
        "api_key": settings.hunter_api_key,
    }
    return client.get(url, params=params)


def _call_clearbit(payload: dict) -> dict | None:
    if not settings.clearbit_api_key:
        return None

    email = payload.get("email")
    if not email:
        return None

    url = "https://person.clearbit.com/v2/people/find"
    if not _within_quota("clearbit", url):
        return None
    headers = {"Authorization": f"Bearer {settings.clearbit_api_key}"}
    return client.get(url, headers=headers, params={"email": email})


def _call_apollo(payload: dict) -> dict | None:
    if not settings.apollo_api_key:
        return None

    email = payload.get("email")
    if not email:
        return None

    url = "https://api.apollo.io/v1/people/match"
    if not _within_quota("apollo", url):
        return None
    headers = {"Content-Type": "application/json"}
    body = {"api_key": settings.apollo_api_key, "email": email}
    return client.post(url, headers=headers, json=body)


def _call_snov(payload: dict) -> dict | None:
    if not settings.snov_api_key:
        return None

    email = payload.get("email")
    if not email:
        return None

    url = "https://api.snov.io/v1/get-emails-from-names"
    if not _within_quota("snov", url):
        return None
    body = {
        "api_key": settings.snov_api_key,
        "email": email,
    }
    return client.post(url, json=body)


PROVIDERS: list[Provider] = [
    Provider("hunter", _call_hunter),
    Provider("clearbit", _call_clearbit),
    Provider("apollo", _call_apollo),
    Provider("snov", _call_snov),
]


def enrich_lead(payload: dict) -> ProviderResult:
    for provider in PROVIDERS:
        try:
            logger.info(f"Trying enrichment provider: {provider.name}")
            data = provider.func(payload)
            if data:
                logger.info(f"Enrichment success: {provider.name}")
                return ProviderResult(provider=provider.name, data=data)
        except Exception as exc:
            logger.warning(f"Provider {provider.name} failed: {exc}")
            continue

    logger.warning("All enrichment providers failed")
    return ProviderResult(provider="none", data=None)
