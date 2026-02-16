# Atlas OS — Solo-Founder Multi-Product Orchestration System

Atlas OS is a prompt-playbook system that runs inside **Cursor / Codex / Claude Code** to orchestrate multiple products with maximum automation while keeping a strict human approval gate for production deploys.

## Products Managed

| Product | App URL | Repo | Stack |
|---------|---------|------|-------|
| Resume Builder | https://www.resumelybuilderai.com/he | nadavyigal/new-ResumeBuilder-ai- | Next.js + TS + Supabase + Vercel |
| RunSmart | https://www.runsmart-ai.com | nadavyigal/Running-coach- | Next.js + TS + Python + Supabase + Vercel |
| Automation-cowork | — | nadavyigal/Automation-cowork | Python + FastAPI + PostgreSQL + Docker |

## Agent Hierarchy

```
┌─────────────────────────────────────────────┐
│  FOUNDER (You) — Approves production only   │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│  ATLAS — Orchestrator / Chief of Staff      │
│  Morning report · task creation · delegation│
└──┬──────────────┬──────────────┬────────────┘
   │              │              │
┌──▼───┐    ┌────▼────┐   ┌────▼──────────┐
│Distri│    │ Product │   │ Monetization  │
│bution│    │  Agent  │   │ (future/off)  │
└──────┘    └─────────┘   └───────────────┘
```

## Quick Start (Phase 0 — Same Day)

```bash
# 1. Copy atlas-os/ into Automation-cowork repo
cp -r atlas-os/ /path/to/Automation-cowork/atlas-os/

# 2. Symlink into each product repo
cd /path/to/new-ResumeBuilder-ai-
ln -s ../Automation-cowork/atlas-os atlas

cd /path/to/Running-coach-
ln -s ../Automation-cowork/atlas-os atlas

# 3. Add GitHub secrets to each repo (Settings → Secrets → Actions):
#    ATLAS_GITHUB_TOKEN  (PAT with repo + workflow scopes)
#
# 4. Copy workflow YAMLs into each repo:
cp atlas-os/workflows/ci.yml .github/workflows/ci.yml
cp atlas-os/workflows/playwright.yml .github/workflows/playwright.yml
cp atlas-os/workflows/atlas-morning-report.yml .github/workflows/atlas-morning-report.yml

# 5. Open Cursor/Claude and run the morning prompt:
#    Paste contents of prompts/atlas.daily.morning.md
```

## Daily Workflow

Every morning, open Cursor/Codex/Claude with access to all 3 repos and paste:

```
@atlas.daily.morning.md
```

Atlas generates a Morning Report, creates/updates GitHub Issues, and delegates to agents.

## Hard Rules

1. **No production deploy without founder approval** — protected branches + PR approval required
2. **Prefer small PRs** — reversible changes, clear rollback notes
3. **Always add/maintain tests** when touching critical paths
4. **Playwright E2E** for all user-facing flows
5. **GitHub Actions** for all CI/CD

## File Structure

```
atlas-os/
├── README.md                           ← You are here
├── atlas.config.json                   ← Product registry + settings
├── prompts/
│   ├── atlas.system.md                 ← Atlas orchestrator system prompt
│   ├── atlas.daily.morning.md          ← Daily morning report prompt
│   ├── atlas.weekly.plan.md            ← Weekly planning prompt
│   ├── distribution.system.md          ← Distribution agent system prompt
│   ├── distribution.weekly.gtm.md      ← Weekly GTM planning
│   ├── product.system.md               ← Product agent system prompt
│   ├── product.pr-review.md            ← PR review checklist
│   ├── product.bug-triage.md           ← Bug triage + fix prompt
│   ├── product.e2e-fix-loop.md         ← Auto-fix failing E2E
│   └── monetization.system.future.md   ← Placeholder (disabled)
├── playbooks/
│   ├── 00_bootstrap.md                 ← Day-0 setup
│   ├── 01_daily_cycle.md               ← Daily workflow
│   ├── 02_weekly_cycle.md              ← Weekly workflow
│   ├── 03_prd_to_pr.md                 ← Feature → PR pipeline
│   ├── 04_bug_to_fix_pr.md             ← Bug → Fix PR pipeline
│   ├── 05_release_gate.md              ← Production deploy gate
│   └── 06_automation_cowork_integration.md
├── schemas/
│   ├── task.schema.json                ← Unified task model
│   └── report.schema.json              ← Morning report schema
├── templates/
│   ├── github_issue_template.md
│   ├── pr_template.md
│   └── decision_request_template.md
└── workflows/
    ├── ci.yml                          ← Lint + typecheck + unit
    ├── playwright.yml                  ← E2E with artifacts
    └── atlas-morning-report.yml        ← Scheduled daily report
```

## Build Plan

| Phase | Timeline | Goal | Success Criteria |
|-------|----------|------|-----------------|
| 0 — Bootstrap | Same day | Add /atlas, CI, Playwright | Morning Report runs manually |
| 1 — Cadence | 2–3 days | Daily + Weekly prompts | Atlas creates GitHub Issues |
| 2 — Auto-fix | 3–5 days | Fix loop for failing CI/E2E | Failing test → fix PR → rerun |
| 3 — Deep automation | 1–2 weeks | Automation-cowork integration | 1 new automation/week |
