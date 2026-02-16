# Playbook 04 — Bug to Fix PR Pipeline

## When
A bug is reported, discovered in CI, or found during testing.

## Flow

```
Bug Reported
  ↓
product.bug-triage.md → Confirm + Classify (P0–P3)
  ↓
IF P0/P1: Fix immediately
  ↓ Create branch: fix/[description]
  ↓ Implement minimal fix
  ↓ Add regression test
  ↓ Open PR → CI runs
  ↓ Founder reviews + approves merge
  ↓
IF P2/P3: Add to backlog
  ↓ Create GitHub Issue with labels
  ↓ Assign to next sprint/week
```

## Key Rules

1. **Fix the bug, not the symptom** — find root cause
2. **Minimal change** — smallest diff that fixes the issue
3. **Regression test** — always add a test that would have caught this
4. **Rollback plan** — every fix PR must describe how to revert
5. **No hotfixes to main** — always go through PR + review

## Acceptance Criteria
- [ ] Bug confirmed and root cause identified
- [ ] Fix is minimal and reversible
- [ ] Regression test added
- [ ] PR open with clear description
- [ ] CI passes
- [ ] Founder approves merge
