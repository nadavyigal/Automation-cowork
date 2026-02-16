# Atlas Daily Morning Report — Execution Prompt

> Paste this prompt into Cursor/Codex/Claude at the start of each workday.
> Ensure the tool has access to all 3 repos.

## Inputs

- All 3 repos: `new-ResumeBuilder-ai-`, `Running-coach-`, `Automation-cowork`
- Current date and timezone (Asia/Jerusalem)
- `atlas.config.json` for product registry

## Steps

### Step 1: Scan all repos (DO NOT SKIP)

For each product in atlas.config.json:

```
1. Read repo structure — identify stack, check for package.json / pyproject.toml
2. git log --oneline --since="yesterday" — what shipped
3. List open PRs — title, author, CI status, age
4. List open issues — title, labels, priority, assignee
5. Check latest GitHub Actions runs — pass/fail, which workflow
6. If Playwright exists: check latest E2E run, count pass/fail/skip
7. Check for any Dependabot / security alerts
```

### Step 2: Identify blockers and failures

```
FOR EACH product:
  IF any CI workflow failed in last 24h:
    → Flag as P0, assign to Product Agent
    → Check if it's a flaky test (passed before, no code change)
  IF any E2E test failed:
    → Flag as P0, trigger product.e2e-fix-loop.md
  IF any PR has been open > 3 days:
    → Flag for review
  IF any issue is labeled p0-critical and unassigned:
    → Auto-assign to Product Agent
```

### Step 3: Generate today's task list

Rank by: P0 bugs > failing CI > open P1 issues > weekly milestone tasks > growth tasks

```
Create 3–7 tasks with:
  - Task description (one line)
  - Product
  - Owner: Product Agent / Distribution Agent / Founder / Atlas
  - Priority: P0/P1/P2
  - Link to issue/PR if exists, otherwise create a new GitHub issue
```

### Step 4: Check weekly milestones

```
Read any existing milestone or project board
Compare progress vs. plan
Flag risks: behind schedule, blocked, missing dependency
```

### Step 5: Scan Automation-cowork for opportunities

```
1. Read Automation-cowork/registry.json (if exists)
2. Look at repetitive manual tasks across products
3. Propose 1–3 automations with:
   - What it automates
   - Estimated time saved per week
   - Implementation effort (hours)
   - ROI score (time_saved / effort)
```

### Step 6: Compile founder decisions

```
Collect all items that need founder input:
- Production deploys pending
- Architectural choices
- Priority conflicts
- Budget decisions
Format each as: Question → Options A/B/C → Recommendation
```

## Output

Produce a single Markdown document following the Morning Report template from `atlas.system.md`.

**Title:** `Atlas Morning Report — YYYY-MM-DD`

If creating GitHub issues for new tasks, use the template from `templates/github_issue_template.md` and apply labels from `atlas.config.json`.

## Acceptance Criteria

- [ ] All 3 products scanned (commits, PRs, issues, CI)
- [ ] Failing CI/E2E flagged as P0
- [ ] 3–7 prioritized tasks with owners
- [ ] Weekly progress summary included
- [ ] Founder decisions formatted with options + recommendation
- [ ] No production deploys triggered without founder approval

## Escalation

If you cannot access a repo or API: note it in the report under "⚠️ Access Issues" and continue with available data.
