from __future__ import annotations

from datetime import datetime
from loguru import logger

from src.automations.data_pipelines.extractor import extract_customers
from src.automations.data_pipelines.transformers import transform_customers
from src.automations.data_pipelines.loader import load_customers
from sqlalchemy import select

from src.core.database import get_session
from src.core.models import AutomationRun, PipelineExecution, RunStatus


def _create_run() -> AutomationRun:
    with get_session() as session:
        run = AutomationRun(automation_name="data_pipeline", status=RunStatus.running, started_at=datetime.utcnow())
        session.add(run)
        session.flush()
        session.refresh(run)
        return run


def _create_execution(run_id: int) -> PipelineExecution:
    with get_session() as session:
        execution = PipelineExecution(
            automation_run_id=run_id,
            source="source_db",
            target="warehouse_db",
            status=RunStatus.running,
            started_at=datetime.utcnow(),
        )
        session.add(execution)
        session.flush()
        session.refresh(execution)
        return execution


def _finalize_execution(execution_id: int, status: RunStatus, rows_extracted: int, rows_loaded: int, error: str | None = None) -> None:
    with get_session() as session:
        execution = session.get(PipelineExecution, execution_id)
        if not execution:
            return
        execution.status = status
        execution.rows_extracted = rows_extracted
        execution.rows_loaded = rows_loaded
        execution.finished_at = datetime.utcnow()
        execution.error_message = error
        session.add(execution)


def _finalize_run(run_id: int, status: RunStatus, error: str | None = None) -> None:
    with get_session() as session:
        run = session.get(AutomationRun, run_id)
        if not run:
            return
        run.status = status
        run.finished_at = datetime.utcnow()
        run.error_message = error
        session.add(run)


def _get_last_successful_run_time() -> datetime | None:
    with get_session() as session:
        stmt = (
            select(PipelineExecution.finished_at)
            .where(PipelineExecution.status == RunStatus.completed)
            .order_by(PipelineExecution.finished_at.desc())
            .limit(1)
        )
        return session.execute(stmt).scalar_one_or_none()


def run_etl_job() -> dict:
    run = _create_run()
    execution = _create_execution(run.id)

    try:
        last_run = _get_last_successful_run_time()
        rows = extract_customers(last_run)
        transformed = transform_customers(rows)
        loaded = load_customers(transformed)

        _finalize_execution(execution.id, RunStatus.completed, len(rows), loaded)
        _finalize_run(run.id, RunStatus.completed)

        result = {"rows_extracted": len(rows), "rows_loaded": loaded}
        logger.info(f"ETL job completed: {result}")
        return result
    except Exception as exc:
        logger.exception(f"ETL job failed: {exc}")
        _finalize_execution(execution.id, RunStatus.failed, 0, 0, str(exc))
        _finalize_run(run.id, RunStatus.failed, str(exc))
        raise


if __name__ == "__main__":
    run_etl_job()
