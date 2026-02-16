# Product Agent — Bug Triage Prompt

> Use when a bug is reported or discovered.

## Inputs

- Bug description (issue, user report, or CI failure)
- Product name and repo
- Steps to reproduce (if available)
- Error logs / screenshots (if available)

## Steps

### Step 1: Reproduce and confirm
```
1. Read the bug description
2. Scan relevant code files
3. Check recent commits — was this introduced recently?
4. Check if there's an existing issue for this
5. Classify: confirmed bug / cannot reproduce / by design / duplicate
```

### Step 2: Assess severity
```
P0-critical: App crashes, data loss, auth broken, payment broken
P1-high: Feature broken, major UX issue, performance degradation
P2-medium: Minor UX issue, edge case, cosmetic
P3-low: Typo, minor polish, nice-to-have
```

### Step 3: Identify root cause
```
1. Trace the code path from user action to failure
2. Identify the exact file(s) and line(s)
3. Determine: code bug / config issue / missing env var / data issue
4. Check: is this a regression? Was there a recent change that caused it?
```

### Step 4: Plan fix
```
1. Describe the minimal fix
2. List files to change
3. Identify what tests to add/update
4. Estimate effort: <1h / 1-4h / 4h+
5. Flag if fix requires: schema change / breaking change / founder review
```

### Step 5: Create issue and/or PR
```
IF no existing issue:
  → Create GitHub Issue using templates/github_issue_template.md
  → Apply labels: bug, [priority], [area], product-agent

IF fix is clear and effort < 4h:
  → Create fix branch: fix/[short-description]
  → Implement fix
  → Add test
  → Open PR using templates/pr_template.md
  → Trigger CI
```

## Output

```markdown
## Bug Triage: [Title]

**Product:** [name]
**Severity:** P0/P1/P2/P3
**Status:** Confirmed / Cannot Reproduce / Duplicate of #[X]

**Root Cause:** [1-2 sentences]
**Affected Files:** [list]
**Regression:** Yes (introduced in commit [hash]) / No

**Fix Plan:**
- [Change 1]
- [Change 2]
- [Test to add]

**Effort:** <1h / 1-4h / 4h+
**Requires Founder:** Yes / No
**Issue:** #[number] (created/updated)
**PR:** #[number] (if fix submitted)
```

## Acceptance Criteria

- [ ] Bug confirmed or classified
- [ ] Priority assigned with justification
- [ ] Root cause identified
- [ ] Fix plan documented
- [ ] GitHub Issue exists with proper labels
- [ ] If fixable < 4h, PR opened

## Escalation

Escalate if:
- Cannot reproduce but user reports persist
- Fix requires schema/auth/payment changes
- Root cause is in a third-party dependency
- Multiple bugs suggest a systemic issue
