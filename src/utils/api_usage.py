from __future__ import annotations

from datetime import datetime, timedelta
from sqlalchemy import select

from src.core.database import get_session
from src.core.models import ApiUsage


def check_and_increment(
    provider: str,
    endpoint: str,
    limit: int | None,
    period_days: int = 30,
) -> tuple[bool, int, datetime | None]:
    if limit is None or limit <= 0:
        return True, 0, None

    now = datetime.utcnow()
    period_end = now + timedelta(days=period_days)

    with get_session() as session:
        stmt = select(ApiUsage).where(
            ApiUsage.provider == provider,
            ApiUsage.endpoint == endpoint,
        )
        usage = session.execute(stmt).scalars().first()

        if not usage:
            usage = ApiUsage(
                provider=provider,
                endpoint=endpoint,
                request_count=0,
                period_start=now,
                period_end=period_end,
            )
            session.add(usage)
            session.flush()

        if not usage.period_end or now > usage.period_end:
            usage.request_count = 0
            usage.period_start = now
            usage.period_end = period_end

        if usage.request_count >= limit:
            return False, usage.request_count, usage.period_end

        usage.request_count += 1
        session.add(usage)
        return True, usage.request_count, usage.period_end