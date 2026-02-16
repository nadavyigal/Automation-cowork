# Playbook 06 — Automation-cowork Integration

## Purpose

Automation-cowork is the automation foundation. Atlas discovers available workflows, proposes new automations, and tracks ROI.

## Registry Format

Create `/automation-cowork/registry.json` as the source of truth:

```json
{
  "version": "1.0.0",
  "workflows": [
    {
      "id": "lead-enrichment",
      "name": "Lead Enrichment Pipeline",
      "trigger": "webhook",
      "endpoint": "/api/webhook/lead",
      "description": "Enrich leads with Hunter.io, Clearbit, Apollo, Snov",
      "inputs": ["email", "company"],
      "outputs": ["enriched_lead_record"],
      "products": ["resume-builder", "runsmart"],
      "status": "active",
      "roi": {
        "time_saved_minutes_per_run": 15,
        "runs_per_week": 10,
        "weekly_savings_hours": 2.5
      }
    },
    {
      "id": "data-pipeline-nightly",
      "name": "Nightly Data Pipeline",
      "trigger": "cron",
      "schedule": "0 2 * * * Asia/Jerusalem",
      "description": "Extract, transform, load from source to warehouse",
      "inputs": ["source_db_connection"],
      "outputs": ["warehouse_updated"],
      "products": ["automation-cowork"],
      "status": "active",
      "roi": {
        "time_saved_minutes_per_run": 30,
        "runs_per_week": 7,
        "weekly_savings_hours": 3.5
      }
    },
    {
      "id": "marketing-distribution",
      "name": "Marketing Distribution",
      "trigger": "cron_or_webhook",
      "endpoint": "/api/webhook/marketing/run-week",
      "description": "Pull GTM assets, ingest CSV queue, publish posts",
      "inputs": ["csv_queue", "marketing_assets"],
      "outputs": ["published_posts", "run_summary"],
      "products": ["resume-builder", "runsmart"],
      "status": "active",
      "roi": {
        "time_saved_minutes_per_run": 45,
        "runs_per_week": 1,
        "weekly_savings_hours": 0.75
      }
    }
  ],
  "proposed": []
}
```

## Weekly Automation Review (Atlas task)

Every week, Atlas should:

### Step 1: Review existing automations
```
1. Read registry.json
2. Check status of each workflow (running? errors?)
3. Calculate actual vs. estimated ROI
4. Flag any broken or underperforming automations
```

### Step 2: Identify new automation candidates
```
Look for patterns:
  - Tasks repeated > 3x/week across products
  - Manual steps in CI/CD that could be automated
  - Data collection that could be scheduled
  - Report generation that follows a template
  - Notifications that should be automatic
```

### Step 3: Propose 1–3 new automations
```
FOR EACH proposal:
  - Name and description
  - What manual task it replaces
  - Estimated time saved per week
  - Implementation effort (hours)
  - ROI score: time_saved_per_week / implementation_hours
  - Priority: ROI > 2.0 = high, 1.0-2.0 = medium, < 1.0 = low
```

### Step 4: Convert to tasks
```
FOR highest-ROI proposal:
  1. Create GitHub Issue in Automation-cowork repo
  2. Label: automation, [priority]
  3. Break down into sub-tasks
  4. Assign to Product Agent for implementation
  5. Add to registry.json with status: "proposed"
```

## Integration Patterns

### Pattern 1: Webhook trigger from product
```
Product event (signup, export, etc.)
  → POST to Automation-cowork webhook
  → Workflow processes
  → Result stored/notified
```

### Pattern 2: Scheduled data sync
```
Cron job in Automation-cowork
  → Reads from product databases
  → Transforms and aggregates
  → Updates dashboards/reports
```

### Pattern 3: CI/CD automation
```
GitHub Actions in product repo
  → Triggers Automation-cowork workflow
  → Results posted back as PR comment/issue
```

## Success Criteria

- [ ] registry.json exists and is current
- [ ] All active workflows documented
- [ ] At least 1 new automation proposed per week
- [ ] ROI tracked for each automation
- [ ] Broken automations flagged and fixed within 48h
