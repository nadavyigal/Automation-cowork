from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class RunStatus(enum.StrEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )


class AutomationRun(Base, TimestampMixin):
    __tablename__ = "automation_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    automation_name: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.pending, index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    lead_jobs: Mapped[list[LeadEnrichmentJob]] = relationship(
        "LeadEnrichmentJob", back_populates="automation_run", cascade="all, delete-orphan"
    )
    pipeline_executions: Mapped[list[PipelineExecution]] = relationship(
        "PipelineExecution", back_populates="automation_run", cascade="all, delete-orphan"
    )
    social_media_posts: Mapped[list[SocialMediaPost]] = relationship(
        "SocialMediaPost", back_populates="automation_run", cascade="all, delete-orphan"
    )


class LeadEnrichmentJob(Base, TimestampMixin):
    __tablename__ = "lead_enrichment_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    automation_run_id: Mapped[int | None] = mapped_column(ForeignKey("automation_runs.id"), nullable=True)

    email: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)

    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    enriched_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.pending, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    automation_run: Mapped[AutomationRun | None] = relationship("AutomationRun", back_populates="lead_jobs")

    __table_args__ = (
        Index("ix_lead_enrichment_jobs_email_status", "email", "status"),
    )


class PipelineExecution(Base, TimestampMixin):
    __tablename__ = "pipeline_executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    automation_run_id: Mapped[int | None] = mapped_column(ForeignKey("automation_runs.id"), nullable=True)

    source: Mapped[str] = mapped_column(String(255))
    target: Mapped[str] = mapped_column(String(255))
    rows_extracted: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rows_loaded: Mapped[int | None] = mapped_column(Integer, nullable=True)

    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.pending, index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    automation_run: Mapped[AutomationRun | None] = relationship(
        "AutomationRun", back_populates="pipeline_executions"
    )


class SocialMediaPost(Base, TimestampMixin):
    __tablename__ = "social_media_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    automation_run_id: Mapped[int | None] = mapped_column(ForeignKey("automation_runs.id"), nullable=True)

    platform: Mapped[str] = mapped_column(String(100))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    media_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.pending, index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    automation_run: Mapped[AutomationRun | None] = relationship(
        "AutomationRun", back_populates="social_media_posts"
    )


class ApiUsage(Base, TimestampMixin):
    __tablename__ = "api_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(120), index=True)
    endpoint: Mapped[str] = mapped_column(String(255))
    request_count: Mapped[int] = mapped_column(Integer, default=0)
    period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


__all__ = [
    "AutomationRun",
    "LeadEnrichmentJob",
    "PipelineExecution",
    "SocialMediaPost",
    "ApiUsage",
    "RunStatus",
]