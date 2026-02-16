# Product Agent — PR Review Prompt

> Use when reviewing an open PR on any product repo.

## Inputs

- PR number and repo
- PR diff (files changed)
- PR description
- Linked issue (if any)
- CI status

## Steps

### Step 1: Read PR context
```
1. Read PR title, description, and linked issue
2. Understand the intent — what problem does this solve?
3. Check CI status — is it passing?
```

### Step 2: Code review checklist
```
FOR EACH changed file:
  □ Logic correctness — does the code do what it claims?
  □ Edge cases — null, empty, boundary values handled?
  □ Error handling — try/catch, error states, user feedback?
  □ TypeScript — no `any` types, proper interfaces?
  □ Security — no exposed secrets, SQL injection, XSS?
  □ Performance — no N+1 queries, unnecessary re-renders?
  □ Readability — clear names, no magic numbers?
  □ Tests — new code has tests, existing tests updated?
```

### Step 3: E2E impact
```
IF change touches user-facing UI:
  □ Playwright E2E test covers the flow?
  □ If not, flag: "Needs E2E test before merge"
IF change touches API:
  □ Contract test exists?
  □ Backward compatible?
```

### Step 4: Risk assessment
```
Classify change:
  LOW: Copy changes, CSS, test additions, docs
  MEDIUM: New features with tests, refactors with no behavior change
  HIGH: Auth, payments, database schema, API contracts, data deletion
```

## Output

```markdown
## PR Review: #[number] — [title]

### Summary
[1-2 sentence summary of what the PR does]

### Verdict: ✅ Approve / 🔄 Request Changes / ❌ Block

### Findings
| Severity | File | Line | Issue |
|----------|------|------|-------|
| 🔴 Critical | path/file.ts | 42 | [description] |
| 🟡 Suggestion | path/file.ts | 88 | [description] |
| 🟢 Nit | path/file.ts | 12 | [description] |

### Missing Tests
- [ ] [Test that should be added]

### Risk Level: Low / Medium / High
### Requires Founder Approval: Yes / No
```

## Acceptance Criteria

- [ ] Every changed file reviewed
- [ ] Critical issues flagged
- [ ] Missing tests identified
- [ ] Risk level assessed
- [ ] Clear verdict given
