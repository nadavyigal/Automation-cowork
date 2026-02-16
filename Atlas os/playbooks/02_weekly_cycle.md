# Playbook 02 — Weekly Cycle

## When
Every Sunday (or start of work week).

## Flow

```
Sunday AM:
  1. Run atlas.weekly.plan.md prompt
  2. Atlas generates weekly retrospective + plan
  3. Atlas delegates to Distribution Agent (distribution.weekly.gtm.md)
  4. Founder reviews and adjusts priorities
  5. GitHub Issues created/updated with week's milestones

Mid-week (Wednesday):
  1. Quick progress check via atlas.daily.morning.md
  2. Atlas flags anything behind schedule
  3. Re-prioritize if needed

End of week (Thursday/Friday):
  1. Atlas summarizes what shipped
  2. Updates metrics
  3. Carries over incomplete tasks
```

## Weekly Metrics to Track

| Metric | How to measure |
|--------|---------------|
| PRs merged | `gh pr list --state merged --search "merged:>YYYY-MM-DD"` |
| Issues closed | `gh issue list --state closed --search "closed:>YYYY-MM-DD"` |
| CI health | % of green workflow runs this week |
| E2E coverage | # passing / # total tests |
| Response time | Time from issue creation to first commit |

## Success Criteria

- [ ] Weekly plan created with 5–10 tasks per product
- [ ] Distribution plan for the week
- [ ] All tasks have owners and due dates
- [ ] GitHub Issues and milestones updated
