# Playbook 00 — Bootstrap Atlas OS (Same Day)

## Goal
Get Atlas OS installed across all repos with CI + Playwright running.

## Prerequisites
- GitHub account with push access to all 3 repos
- GitHub CLI (`gh`) installed and authenticated
- Node.js 18+ and npm

## Checklist

### 1. Set up Automation-cowork as Atlas home

```bash
cd Automation-cowork

# Create atlas-os directory (copy this entire atlas-os folder)
git add atlas-os/
git commit -m "chore: add Atlas OS orchestration system"
git push
```

### 2. Symlink into each product repo

```bash
# Resume Builder
cd new-ResumeBuilder-ai-
ln -s ../Automation-cowork/atlas-os atlas
# OR copy if symlinks don't work in your setup:
# cp -r ../Automation-cowork/atlas-os atlas
git add atlas
git commit -m "chore: add Atlas OS symlink"
git push

# RunSmart
cd Running-coach-
ln -s ../Automation-cowork/atlas-os atlas
git add atlas
git commit -m "chore: add Atlas OS symlink"
git push
```

### 3. Add GitHub Actions workflows

For **Resume Builder** (`new-ResumeBuilder-ai-`):
```bash
# Already has .github/workflows — add/update:
cp atlas-os/workflows/ci.yml .github/workflows/ci.yml
cp atlas-os/workflows/playwright.yml .github/workflows/playwright.yml
cp atlas-os/workflows/atlas-morning-report.yml .github/workflows/atlas-morning-report.yml
git add .github/workflows/
git commit -m "ci: add Atlas OS workflows (CI + Playwright + morning report)"
git push
```

For **RunSmart** (`Running-coach-`):
```bash
cp atlas-os/workflows/ci.yml .github/workflows/ci.yml
cp atlas-os/workflows/playwright.yml .github/workflows/playwright.yml
cp atlas-os/workflows/atlas-morning-report.yml .github/workflows/atlas-morning-report.yml
git add .github/workflows/
git commit -m "ci: add Atlas OS workflows (CI + Playwright + morning report)"
git push
```

### 4. Add issue and PR templates

```bash
# For each repo:
mkdir -p .github/ISSUE_TEMPLATE
cp atlas-os/templates/github_issue_template.md .github/ISSUE_TEMPLATE/atlas-task.md
cp atlas-os/templates/pr_template.md .github/pull_request_template.md
git add .github/
git commit -m "chore: add Atlas issue and PR templates"
git push
```

### 5. Add GitHub secrets

Go to each repo → Settings → Secrets and variables → Actions:

| Secret | Value | Repos |
|--------|-------|-------|
| `ATLAS_GITHUB_TOKEN` | PAT with `repo` + `workflow` scopes | All 3 |

### 6. Set up branch protection (CRITICAL)

For each product repo → Settings → Branches → Add rule for `main`:

- ✅ Require a pull request before merging
- ✅ Require approvals (1)
- ✅ Require status checks to pass before merging
  - Select: `ci` workflow
  - Select: `playwright` workflow (when available)
- ✅ Require branches to be up to date before merging
- ❌ Allow force pushes: OFF
- ❌ Allow deletions: OFF

### 7. Add labels to each repo

```bash
# Run for each repo:
gh label create p0-critical --color B60205 --description "Severity: critical"
gh label create p1-high --color D93F0B --description "Severity: high"
gh label create p2-medium --color FBCA04 --description "Severity: medium"
gh label create p3-low --color 0E8A16 --description "Severity: low"
gh label create atlas --color 5319E7 --description "Owner: Atlas orchestrator"
gh label create product-agent --color 0075CA --description "Owner: Product Agent"
gh label create distribution-agent --color E4E669 --description "Owner: Distribution Agent"
gh label create founder-required --color B60205 --description "Needs founder decision"
gh label create bug --color D73A4A
gh label create feature --color A2EEEF
gh label create chore --color FEF2C0
gh label create test --color BFD4F2
gh label create e2e --color C5DEF5 --description "E2E test related"
gh label create automation --color 7057FF --description "Automation-cowork"
gh label create blocked --color B60205 --description "Blocked, needs intervention"
```

### 8. Install Playwright (if not already present)

For **Resume Builder** (already has Playwright):
```bash
cd new-ResumeBuilder-ai-
npx playwright install --with-deps
npx playwright test --list  # verify tests exist
```

For **RunSmart** (needs Playwright setup):
```bash
cd Running-coach-
npm init playwright@latest
# Accept defaults, TypeScript, tests/ folder
npx playwright install --with-deps
```

### 9. Verify setup

```bash
# For each repo, check:
gh workflow list                    # Workflows visible
gh run list --limit 3              # Recent runs
gh issue list                      # Issues accessible
gh pr list                         # PRs accessible
```

## Success Criteria

- [ ] Atlas OS files committed to Automation-cowork
- [ ] Symlinked/copied to Resume Builder and RunSmart
- [ ] CI workflow runs on push/PR for both products
- [ ] Playwright workflow runs on push/PR for Resume Builder
- [ ] Playwright installed on RunSmart (at least skeleton test)
- [ ] Branch protection enabled on main for both products
- [ ] Labels added to all repos
- [ ] Morning Report prompt can be run manually in Cursor/Claude
- [ ] Atlas can read: commits, PRs, issues, CI status for all repos
