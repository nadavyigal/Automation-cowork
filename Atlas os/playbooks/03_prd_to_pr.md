# Playbook 03 — PRD to PR Pipeline

## When
A new feature needs to be implemented from a product requirement.

## Inputs
- Feature description or PRD
- Product (Resume Builder / RunSmart)
- Priority and deadline

## Steps

### Step 1: Break down into tasks
```
1. Read the feature requirement
2. Identify: frontend changes, backend changes, database changes, test needs
3. Create sub-tasks (each should be < 4 hours of work)
4. Create GitHub Issues for each sub-task
5. Link to parent feature issue
```

### Step 2: Technical design (if complex)
```
IF feature touches > 5 files OR requires new API:
  1. Write brief tech design in issue comment
  2. List files to create/modify
  3. Define API contracts (if any)
  4. Note database changes (if any) → flag for founder
  5. Wait for founder approval if architectural
```

### Step 3: Implement in small PRs
```
FOR EACH sub-task:
  1. Create branch: feature/[feature-name]-[subtask]
  2. Implement changes
  3. Add tests (unit + E2E if user-facing)
  4. Open PR using templates/pr_template.md
  5. Link PR to issue
  6. Request review
```

### Step 4: Verify and ship
```
1. All PRs pass CI + E2E
2. All acceptance criteria met
3. Founder reviews and approves merge to main
4. Monitor post-merge for issues
```

## Acceptance Criteria
- [ ] Feature broken into < 4h sub-tasks
- [ ] Each sub-task has a GitHub Issue
- [ ] Each PR is small and reviewable
- [ ] Tests cover the new functionality
- [ ] No production deploy without founder approval
