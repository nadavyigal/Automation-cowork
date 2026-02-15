from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import requests
from loguru import logger

from src.core.config import settings
from src.core.models import SocialMediaPost


@dataclass(frozen=True)
class PublishResult:
    success: bool
    provider: str
    external_id: str | None = None
    error_message: str | None = None


def _resolve_webhook(platform: str) -> str | None:
    mapping = {
        "linkedin": settings.linkedin_publisher_webhook_url,
        "x": settings.x_publisher_webhook_url,
        "reddit": settings.reddit_publisher_webhook_url,
        "community": settings.community_publisher_webhook_url,
        "newsletter": settings.newsletter_publisher_webhook_url,
    }
    return mapping.get(platform)


def _publish_via_webhook(post: SocialMediaPost) -> PublishResult:
    webhook = _resolve_webhook(post.platform)
    if not webhook:
        return PublishResult(
            success=False,
            provider="webhook",
            error_message=f"No webhook configured for platform '{post.platform}'",
        )

    payload = {
        "platform": post.platform,
        "content": post.content,
        "url": post.media_url,
        "scheduled_at": post.scheduled_at.isoformat() if post.scheduled_at else None,
        "post_id": post.id,
    }

    try:
        response = requests.post(webhook, json=payload, timeout=(5, 30))
        response.raise_for_status()
        external_id: str | None = None
        try:
            body = response.json()
            external_id = str(body.get("id") or body.get("job_id") or body.get("post_id") or "")
        except ValueError:
            external_id = None
        return PublishResult(success=True, provider="webhook", external_id=external_id)
    except Exception as exc:  # noqa: BLE001
        return PublishResult(success=False, provider="webhook", error_message=str(exc))


def _publish_dry_run(post: SocialMediaPost) -> PublishResult:
    logger.info(
        f"[DRY RUN] publish platform={post.platform} id={post.id} url={post.media_url}"
    )
    external_id = f"dryrun-{post.id}-{int(datetime.utcnow().timestamp())}"
    return PublishResult(success=True, provider="dry-run", external_id=external_id)


def publish_post(post: SocialMediaPost) -> PublishResult:
    mode = settings.marketing_execution_mode.strip().lower()
    if mode == "dry-run":
        return _publish_dry_run(post)

    if mode == "live":
        return _publish_via_webhook(post)

    return PublishResult(
        success=False,
        provider="config",
        error_message=f"Unsupported marketing_execution_mode: {settings.marketing_execution_mode}",
    )
