# Atlas Weekly Plan — Execution Prompt

> Run every Sunday or Monday morning. Reviews the past week and plans the next.

## Inputs

- All 3 repos + GitHub Issues/Projects
- Last week's morning reports (if saved as issues)
- atlas.config.json

## Steps

### Step 1: Weekly retrospective

```
FOR EACH product:
  1. Count PRs merged this week
  2. Count issues closed this week
  3. List features shipped (merged to main)
  4. List bugs fixed
  5. CI/E2E health: % green this week vs last week
  6. Note any incidents or rollbacks
```

### Step 2: Review open backlog

```
FOR EACH product:
  1. List all open issues by priority
  2. Identify stale issues (no activity > 7 days)
  3. Check if any milestones are overdue
  4. Identify dependencies between products
```

### Step 3: Plan next week

```
Select 5–10 tasks per product for the coming week:
  - Must include all P0 and P1 bugs
  - Must include milestone-critical features
  - Balance between: bugs, features, growth tasks, tech debt
  - Assign each to: Product Agent / Distribution Agent / Founder

Create/update GitHub Issues with:
  - Labels from atlas.config.json taxonomy
  - Milestone assignment
  - Due dates (within the week)
```

### Step 4: Distribution planning

```
Delegate to Distribution Agent (distribution.weekly.gtm.md):
  - Content calendar for the week
  - Any launches or announcements
  - Growth experiments to run
  - Copy/content deliverables
```

### Step 5: Automation review

```
Review Automation-cowork:
  - What was automated this week? Time saved?
  - Top 3 candidates for next week
  - Create tasks/issues for top automation
```

## Output

```markdown
# Atlas Weekly Plan — Week of YYYY-MM-DD

## 📊 Last Week Summary
| Product | PRs Merged | Issues Closed | Features Shipped | Bugs Fixed | CI Health |
|---------|-----------|--------------|-----------------|-----------|-----------|
| Resume Builder | X | Y | [list] | [list] | XX% |
| RunSmart | X | Y | [list] | [list] | XX% |

## 🎯 This Week's Goals
### Resume Builder
1. [Goal] — Owner — Priority — Due
2. [Goal] — Owner — Priority — Due

### RunSmart
1. [Goal] — Owner — Priority — Due
2. [Goal] — Owner — Priority — Due

## 🚀 Distribution Plan
- [Content/growth items for the week]

## 🤖 Automation Targets
1. [Automation] — Est. ROI: Xh/week — Effort: Yh
2. [Automation] — Est. ROI: Xh/week — Effort: Yh

## ❓ Founder Decisions Needed
[Decision format from atlas.system.md]
```

## Acceptance Criteria

- [ ] Last week fully summarized with metrics
- [ ] 5–10 tasks per product assigned and prioritized
- [ ] Distribution plan delegated
- [ ] Automation opportunities identified
- [ ] GitHub Issues created/updated for all tasks
