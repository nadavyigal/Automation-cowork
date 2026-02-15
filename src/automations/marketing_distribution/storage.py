from __future__ import annotations

from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from sqlalchemy import select

from src.automations.marketing_distribution.schema import SocialPostDraft
from src.core.config import settings
from src.core.database import get_session
from src.core.models import AutomationRun, RunStatus, SocialMediaPost


def create_marketing_run(trigger_source: str) -> AutomationRun:
    with get_session() as session:
        run = AutomationRun(
            automation_name="marketing_distribution",
            status=RunStatus.running,
            started_at=datetime.utcnow(),
            error_message=f"trigger={trigger_source}",
        )
        session.add(run)
        session.flush()
        session.refresh(run)
        return run


def finalize_marketing_run(run_id: int, status: RunStatus, error_message: str | None = None) -> None:
    with get_session() as session:
        run = session.get(AutomationRun, run_id)
        if not run:
            return
        run.status = status
        run.finished_at = datetime.utcnow()
        run.error_message = error_message
        session.add(run)


def _scheduled_datetime_from_date(publish_date: date) -> datetime:
    timezone = ZoneInfo(settings.scheduler_timezone)
    return datetime.combine(
        publish_date,
        time(hour=settings.marketing_daily_run_hour, minute=settings.marketing_daily_run_minute),
        tzinfo=timezone,
    )


def queue_social_post(run_id: int, post: SocialPostDraft) -> tuple[SocialMediaPost, bool]:
    scheduled_at = _scheduled_datetime_from_date(post.publish_date)

    with get_session() as session:
        existing_stmt = (
            select(SocialMediaPost)
            .where(SocialMediaPost.platform == post.normalized_platform)
            .where(SocialMediaPost.media_url == post.utm_url)
            .where(SocialMediaPost.scheduled_at == scheduled_at)
            .order_by(SocialMediaPost.id.desc())
            .limit(1)
        )
        existing = session.execute(existing_stmt).scalars().first()
        if existing:
            return existing, False

        queued = SocialMediaPost(
            automation_run_id=run_id,
            platform=post.normalized_platform,
            content=post.rendered_content,
            media_url=post.utm_url,
            scheduled_at=scheduled_at,
            status=RunStatus.pending,
        )
        session.add(queued)
        session.flush()
        session.refresh(queued)
        return queued, True


def list_due_posts(now: datetime) -> list[SocialMediaPost]:
    with get_session() as session:
        stmt = (
            select(SocialMediaPost)
            .where(SocialMediaPost.status == RunStatus.pending)
            .where(SocialMediaPost.scheduled_at.is_not(None))
            .where(SocialMediaPost.scheduled_at <= now)
            .order_by(SocialMediaPost.scheduled_at.asc(), SocialMediaPost.id.asc())
        )
        return list(session.execute(stmt).scalars().all())


def mark_post_running(post_id: int) -> None:
    with get_session() as session:
        post = session.get(SocialMediaPost, post_id)
        if not post:
            return
        post.status = RunStatus.running
        session.add(post)


def mark_post_completed(post_id: int) -> None:
    with get_session() as session:
        post = session.get(SocialMediaPost, post_id)
        if not post:
            return
        post.status = RunStatus.completed
        post.posted_at = datetime.utcnow()
        post.error_message = None
        session.add(post)


def mark_post_failed(post_id: int, error_message: str) -> None:
    with get_session() as session:
        post = session.get(SocialMediaPost, post_id)
        if not post:
            return
        post.status = RunStatus.failed
        post.error_message = error_message[:1000]
        session.add(post)


def list_recent_marketing_runs(limit: int = 20) -> list[AutomationRun]:
    with get_session() as session:
        stmt = (
            select(AutomationRun)
            .where(AutomationRun.automation_name == "marketing_distribution")
            .order_by(AutomationRun.created_at.desc())
            .limit(limit)
        )
        return list(session.execute(stmt).scalars().all())
