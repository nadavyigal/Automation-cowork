# Architecture

## Overview
Three-layer agentic stack:
1. Directive: human instructions
2. Orchestration: BMAD agents and workflows
3. Execution: Python automations + PostgreSQL

## Database Schema
Core tables:
- automation_runs
- lead_enrichment_jobs
- pipeline_executions
- social_media_posts
- api_usage

Mermaid ERD to be added in `visualizations/system-architecture.mmd`.

## Python Package Structure
- src/core: config, database, models, logger, scheduler, executor
- src/utils: http client, error handling, self-healing
- src/automations/lead_enrichment: webhook, enrichment, storage, notifications
- src/automations/data_pipelines: extractor, transformers, loader, etl_job, scheduler

## API Integrations
- Lead enrichment: Hunter, Clearbit, Apollo, Snov (fallback chain)
- Email: SMTP or SendGrid
- AI: OpenAI for self-healing

## Error Handling
- Retry decorator with exponential backoff
- Status updates stored in DB

## Logging & Monitoring
- Loguru to stdout + rolling file

## Deployment
- Local Docker for PostgreSQL + pgAdmin
- Python runtime via Poetry

## Secrets
- Environment variables in `.env`