# Product Requirements Document (PRD)

## Vision
Build a standalone, code-first automation system to replace n8n visual workflows with a Python + BMAD agentic stack.

## Goals
- Replace two core n8n workflows: lead enrichment and daily data pipelines
- Run locally on Windows with a dedicated PostgreSQL instance
- Enable self-correction for API changes
- Produce Mermaid diagrams for each workflow
- Make it easy to add new automations

## Personas
- Developer/Operator (single user): designs, runs, and maintains the automations

## Functional Requirements
### Lead Enrichment
- Accept webhook payloads
- Enrich lead data using multiple API providers with fallback chain
- Cache results to avoid duplicate API calls
- Store results and status in PostgreSQL
- Send email notifications on completion/failure

### Data Pipelines
- Extract from a source PostgreSQL database
- Transform: dedupe, normalize, validate
- Load into a target/warehouse database
- Schedule nightly runs at 2 AM Asia/Jerusalem
- Log metrics and store execution status

## Non-Functional Requirements
- Reliability: retries with exponential backoff
- Maintainability: modular Python packages, clear logs
- Performance: batch DB operations, caching
- Observability: structured logging, status tables

## Success Metrics
- Both automations run end-to-end locally
- Lead enrichment completes within 2 minutes per lead
- Data pipeline runs daily without manual intervention
- Docs and diagrams reflect actual workflows

## Out of Scope
- Social media automation (Phase 2)
- Cloud deployment
- Slack notifications

## Epics
1. Foundation
2. Lead Enrichment Automation
3. Data Pipelines