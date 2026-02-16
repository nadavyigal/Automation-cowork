# Product Agent — E2E Auto-Fix Loop

> Triggered automatically when Playwright E2E tests fail in CI.
> This is the core automation loop: detect failure → diagnose → fix → rerun.

## Inputs

- Failing workflow run URL or ID
- Repo name and branch
- Playwright HTML report (artifact from CI)
- Test trace files (if available)

## Steps

### Step 1: Read failure details
```
1. Download Playwright HTML report from CI artifacts
2. Identify which test(s) failed
3. For each failed test:
   - Read the test name and file
   - Read the error message
   - Read the trace/screenshot if available
   - Identify: timeout / element not found / assertion failed / network error
```

### Step 2: Classify failure type
```
FLAKY: Test passed in previous run, no code change since
  → Re-run workflow once
  → If passes: mark as flaky, create issue to stabilize
  → If fails again: treat as real failure

SELECTOR_CHANGED: Element not found, but page loads
  → Code change likely moved/renamed the element
  → Fix: update selector in test

FEATURE_BROKEN: Assertion fails on expected behavior
  → The product code has a bug
  → Fix: fix the product code, not the test

ENV_ISSUE: Network error, timeout on external service
  → Missing env var or service down
  → Escalate to founder (credentials needed)

NEW_FLOW: Test references a flow that was redesigned
  → Test needs rewrite to match new UX
  → Update test to match current product behavior
```

### Step 3: Implement fix
```
BASED ON classification:

IF FLAKY:
  1. gh workflow run playwright.yml  (re-run)
  2. If passes: create issue "Stabilize flaky test: [name]"
  3. If fails: continue to FEATURE_BROKEN

IF SELECTOR_CHANGED:
  1. Read current page HTML/component to find correct selector
  2. Update test file with new selector
  3. Use data-testid attributes when possible
  4. Create branch: fix/e2e-[test-name]
  5. Push and open PR

IF FEATURE_BROKEN:
  1. Trigger product.bug-triage.md with the failure context
  2. Fix the product code (not the test)
  3. Create branch: fix/[bug-description]
  4. Push and open PR

IF ENV_ISSUE:
  1. Document what secret/service is needed
  2. Escalate to founder with exact instructions
  3. Create issue with label: blocked, founder-required

IF NEW_FLOW:
  1. Review the current UI/flow
  2. Rewrite the test to match
  3. Create branch: fix/e2e-update-[flow-name]
  4. Push and open PR
```

### Step 4: Verify fix
```
1. Run the specific test locally: npx playwright test [test-file] --headed
2. If passes: push to PR branch
3. CI will auto-trigger on PR
4. Check CI result
5. If still fails: repeat from Step 1 (max 3 attempts)
6. If fails after 3 attempts: escalate to founder
```

### Step 5: Update tracking
```
1. Update or create GitHub Issue with:
   - Test name and failure type
   - Root cause
   - Fix applied
   - CI run results (before and after)
2. Apply labels: e2e, [product], product-agent
3. If multiple tests failing: group into single issue
```

## Output

```markdown
## E2E Fix Report

**Product:** [name]
**Failing Tests:** [count]
**CI Run:** [link]

### Failures
| Test | Type | Fix | Status |
|------|------|-----|--------|
| test-login | SELECTOR_CHANGED | Updated selector | ✅ Fixed |
| test-signup | FEATURE_BROKEN | Fixed validation | ✅ Fixed |
| test-export | ENV_ISSUE | Needs API key | ⏳ Escalated |

**PR:** #[number]
**Re-run CI:** [link]
**Escalated Items:** [list or "None"]
```

## Acceptance Criteria

- [ ] All failing tests diagnosed
- [ ] Fixes attempted (max 3 loops)
- [ ] PR opened with fixes
- [ ] CI re-triggered
- [ ] Unfixable issues escalated with clear reason

## Escalation

Immediately escalate if:
- Credentials/secrets missing
- Breaking change in third-party service
- Auth flow fundamentally changed
- More than 50% of E2E suite failing (likely systemic issue)
- 3 fix attempts failed on same test
