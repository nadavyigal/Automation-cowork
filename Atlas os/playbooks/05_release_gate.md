# Playbook 05 — Release / Production Deploy Gate

## Hard Rule

> **No code reaches production without explicit founder approval.**

## Recommended Setup: Protected Branches + Required PR Approvals

This is simpler than GitHub Environments and works with Vercel's auto-deploy.

### Configuration (per repo)

**GitHub → Settings → Branches → Branch protection rules → `main`:**

- ✅ Require a pull request before merging
- ✅ Require approvals: **1** (the founder)
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require status checks to pass before merging
  - Required checks: `ci`, `playwright` (if exists)
- ✅ Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ❌ Allow force pushes: **OFF**
- ❌ Allow deletions: **OFF**

### Vercel Integration

Both products deploy via Vercel which auto-deploys on push to `main`:
- **Preview deploys** happen on every PR → safe, no gate needed
- **Production deploy** happens on merge to `main` → gated by PR approval

Flow:
```
Feature branch → PR → CI passes → Founder approves → Merge to main → Vercel auto-deploys
```

### Pre-merge Checklist (for founder review)

Before approving a PR for merge to main:

```markdown
## Release Checklist
- [ ] CI passes (lint + typecheck + unit tests)
- [ ] E2E tests pass (Playwright)
- [ ] PR description explains what and why
- [ ] Changes are reviewed and understood
- [ ] No breaking changes to user-facing flows
- [ ] Database migrations reviewed (if any)
- [ ] Environment variables documented (if new ones needed)
- [ ] Rollback plan described
- [ ] No secrets or credentials in code
```

### Rollback Procedure

If something goes wrong after deploy:

```bash
# Option 1: Revert the PR
gh pr list --state merged --limit 5  # find the PR
git revert -m 1 <merge-commit-hash>
git push origin main  # triggers redeploy

# Option 2: Vercel instant rollback
# Go to Vercel dashboard → Deployments → click previous deploy → Promote to Production

# Option 3: Git reset (last resort)
git reset --hard <known-good-commit>
git push --force origin main  # requires temporarily disabling branch protection
```

## Success Criteria

- [ ] Branch protection configured on all repos
- [ ] No way to push directly to main
- [ ] Every production deploy traceable to an approved PR
- [ ] Rollback tested and documented
