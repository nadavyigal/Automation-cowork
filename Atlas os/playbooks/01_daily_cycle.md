# Playbook 01 — Daily Cycle

## When
Every workday morning (Sun–Thu for Israel timezone).

## Flow

```
07:00  atlas-morning-report.yml runs (GitHub Actions, scheduled)
         ↓ Collects CI/PR/Issue signals → outputs Markdown artifact
         ↓ Optionally creates/updates "Daily Report" issue

08:00  Founder opens Cursor/Claude
         ↓ Pastes atlas.daily.morning.md prompt
         ↓ Atlas scans all repos, generates Morning Report
         ↓ Creates GitHub Issues for new tasks
         ↓ Assigns to Product Agent / Distribution Agent

08:30  Founder reviews report
         ↓ Answers decision questions
         ↓ Approves/rejects pending PRs
         ↓ Adjusts priorities if needed

09:00+ Atlas executes
         ↓ Product Agent works on P0/P1 tasks
         ↓ Distribution Agent works on content/growth
         ↓ Atlas monitors CI/E2E, triggers fix loops as needed

End of day: Quick check
         ↓ What got done? Any new blockers?
         ↓ Update issues, close completed
```

## Daily Standup Format (if you want a quicker version)

Instead of the full Morning Report, you can ask Atlas:

```
Quick standup for today:
- What shipped yesterday?
- What's blocked?
- What are the top 3 tasks for today?
```

## Success Criteria

- [ ] Morning Report generated before 9 AM
- [ ] All P0 items addressed same day
- [ ] Founder decisions made within 4 hours
- [ ] GitHub Issues reflect current state
