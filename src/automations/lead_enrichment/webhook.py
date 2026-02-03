from __future__ import annotations

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, EmailStr
from loguru import logger

from src.automations.lead_enrichment import enrichment, notifications, storage
from src.core.models import RunStatus


class LeadInput(BaseModel):
    email: EmailStr
    name: str | None = None
    company: str | None = None


app = FastAPI(title="Automation Cowork Lead Enrichment")


def process_lead(job_id: int, payload: dict) -> None:
    cached = storage.get_cached_enrichment(payload["email"])
    if cached and cached.enriched_data:
        logger.info("Using cached enrichment data")
        storage.update_lead_job(job_id, status=RunStatus.completed, enriched_data=cached.enriched_data)
        try:
            notifications.send_lead_notification(
                job_id=job_id,
                email=payload["email"],
                provider="cache",
                status="completed",
            )
        except Exception as exc:
            logger.warning(f"Notification failed: {exc}")
        return

    run = storage.create_automation_run("lead_enrichment")
    try:
        result = enrichment.enrich_lead(payload)
        status = RunStatus.completed if result.data else RunStatus.failed
        error_message = None if result.data else "All providers failed"
        storage.update_lead_job(
            job_id,
            status=status,
            enriched_data=result.data,
            error_message=error_message,
            automation_run_id=run.id,
        )

        try:
            notifications.send_lead_notification(
                job_id=job_id,
                email=payload["email"],
                provider=result.provider if result.data else None,
                status=status.value,
                error_message=error_message,
            )
        except Exception as exc:
            logger.warning(f"Notification failed: {exc}")

        storage.finalize_automation_run(run.id, status)
    except Exception as exc:
        logger.exception(f"Lead enrichment failed: {exc}")
        storage.update_lead_job(job_id, status=RunStatus.failed, error_message=str(exc), automation_run_id=run.id)
        storage.finalize_automation_run(run.id, RunStatus.failed, str(exc))
        try:
            notifications.send_lead_notification(
                job_id=job_id,
                email=payload["email"],
                provider=None,
                status="failed",
                error_message=str(exc),
            )
        except Exception as notify_exc:
            logger.warning(f"Notification failed: {notify_exc}")


@app.post("/api/webhook/lead", status_code=202)
async def receive_lead(lead: LeadInput, background_tasks: BackgroundTasks):
    payload = lead.model_dump()
    job = storage.create_lead_job(payload)
    background_tasks.add_task(process_lead, job.id, payload)
    return {"job_id": job.id, "status": "accepted"}
