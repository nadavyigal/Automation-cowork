# Automation Cowork - Agentic Workflow System

Replace n8n visual workflows with code-based, self-correcting automation.

## Architecture

Mermaid diagrams live in `visualizations/` and can be rendered in VS Code Mermaid preview.

## Automations

### 1. Lead Enrichment
- Trigger: Webhook POST to `/api/webhook/lead`
- Process: Enrich with multiple APIs (Hunter.io, Clearbit, Apollo, Snov) -> Store -> Email notification
- Schedule: On-demand (webhook-based)
- API Fallback: Tries multiple providers if one fails

### 2. Data Pipelines
- Trigger: Nightly at 2 AM (Asia/Jerusalem timezone)
- Process: Extract from source DB -> Transform (dedupe, normalize) -> Load to warehouse
- Schedule: APScheduler cron job
- Error Handling: Email alerts on failure, automatic retry

### 3. Marketing Distribution
- Trigger: Daily scheduler or webhook `POST /api/webhook/marketing/run-week`
- Process: Pull GTM assets from marketing repo branch -> ingest CSV queue -> persist posts -> publish (dry-run or webhook live mode)
- Schedule: Configurable via `MARKETING_DAILY_RUN_HOUR/MINUTE`
- Error Handling: Run-level status + email notification summary

## Quick Start

```bash
# 1. Start PostgreSQL
# (requires Docker)
docker-compose up -d

# 2. Create .env from template
copy .env.example .env

# 3. Install dependencies
poetry install

# 4. Run migrations
alembic upgrade head

# 5. Start webhook server
uvicorn src.automations.lead_enrichment.webhook:app --reload

# 5b. Start marketing distribution webhook (optional)
uvicorn src.automations.marketing_distribution.webhook:app --reload --port 8001

# 6. Start scheduler
python src/core/scheduler.py
```

## Development

BMAD Workflow
- Create new story: `/sm` -> `*create-next-story`
- Implement: `/dev` -> Provide story YAML path
- Review: `/qa` -> Provide story YAML path
- Visualize: `/tech-writer` -> Generate diagrams

Testing

```bash
pytest tests/
```

Code Quality

```bash
black src/
ruff check src/
mypy src/
```

## BMAD Installation Note

The upstream BMAD installer uses `npx bmad-method install` to generate `_bmad/` and `.claude/` artifacts.
This repo includes placeholders for `.bmad-core/` and `.claude/commands/BMad/` per the plan, but you should
run the installer if you want the official, up-to-date BMAD assets.
