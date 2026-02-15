from __future__ import annotations

from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel

from src.automations.marketing_distribution import storage
from src.automations.marketing_distribution.service import run_marketing_distribution


class MarketingRunInput(BaseModel):
    week_id: str | None = None
    run_date: date | None = None
    force_sync: bool = False


app = FastAPI(title="Automation Cowork Marketing Distribution")


@app.post("/api/webhook/marketing/run-week")
async def trigger_marketing_run(payload: MarketingRunInput):
    summary = run_marketing_distribution(
        trigger="webhook",
        target_date=payload.run_date,
        force_sync=payload.force_sync,
    )
    return summary


@app.post("/api/webhook/marketing/rerun-failed")
async def rerun_failed_posts():
    summary = run_marketing_distribution(trigger="rerun_failed", force_sync=False)
    return summary


@app.get("/api/marketing/status")
async def marketing_status(limit: int = 20):
    runs = storage.list_recent_marketing_runs(limit=limit)
    return {
        "runs": [
            {
                "id": run.id,
                "automation_name": run.automation_name,
                "status": run.status.value if hasattr(run.status, "value") else str(run.status),
                "started_at": run.started_at.isoformat() if run.started_at else None,
                "finished_at": run.finished_at.isoformat() if run.finished_at else None,
                "error_message": run.error_message,
                "created_at": run.created_at.isoformat() if run.created_at else None,
            }
            for run in runs
        ]
    }
