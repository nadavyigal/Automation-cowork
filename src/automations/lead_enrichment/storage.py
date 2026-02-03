from __future__ import annotations

from datetime import datetime
from sqlalchemy import select

from src.core.database import get_session
from src.core.models import AutomationRun, LeadEnrichmentJob, RunStatus


def create_automation_run(name: str) -> AutomationRun:
    with get_session() as session:
        run = AutomationRun(automation_name=name, status=RunStatus.running, started_at=datetime.utcnow())
        session.add(run)
        session.flush()
        session.refresh(run)
        return run


def finalize_automation_run(run_id: int, status: RunStatus, error_message: str | None = None) -> None:
    with get_session() as session:
        run = session.get(AutomationRun, run_id)
        if not run:
            return
        run.status = status
        run.finished_at = datetime.utcnow()
        run.error_message = error_message
        session.add(run)


def create_lead_job(payload: dict) -> LeadEnrichmentJob:
    with get_session() as session:
        job = LeadEnrichmentJob(
            email=payload.get("email", ""),
            name=payload.get("name"),
            company=payload.get("company"),
            payload=payload,
            status=RunStatus.pending,
        )
        session.add(job)
        session.flush()
        session.refresh(job)
        return job


def update_lead_job(job_id: int, **updates) -> None:
    with get_session() as session:
        job = session.get(LeadEnrichmentJob, job_id)
        if not job:
            return
        for key, value in updates.items():
            setattr(job, key, value)
        session.add(job)


def get_cached_enrichment(email: str) -> LeadEnrichmentJob | None:
    with get_session() as session:
        stmt = (
            select(LeadEnrichmentJob)
            .where(LeadEnrichmentJob.email == email)
            .where(LeadEnrichmentJob.status == RunStatus.completed)
            .order_by(LeadEnrichmentJob.updated_at.desc())
        )
        result = session.execute(stmt).scalars().first()
        return result