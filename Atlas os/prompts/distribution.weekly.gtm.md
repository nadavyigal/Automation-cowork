# Distribution Agent — Weekly GTM Plan

> Run weekly (delegated by Atlas during weekly planning).

## Inputs

- Atlas Weekly Plan priorities
- Product roadmap / shipped features this week
- Previous week's distribution metrics (if available)
- Content calendar from last week
- atlas.config.json for product list

## Steps

### Step 1: Audit existing assets

```
FOR EACH product:
  1. Check /GTM, /launch-assets, /docs, /marketing folders
  2. Identify reusable content
  3. Note what's outdated or missing
```

### Step 2: Align with product milestones

```
FROM Atlas Weekly Plan:
  - What features shipped or shipping this week?
  - Any launches or announcements?
  - Create content hooks around new features
```

### Step 3: Build content calendar

```
FOR EACH product, plan 3-5 content pieces:
  - Platform (LinkedIn, Twitter, Reddit, Blog, Email, Community)
  - Topic aligned to: feature launch, user pain point, educational content
  - Draft headline and 2-line brief
  - Assign status: Idea → Draft → Review → Ready → Published
```

### Step 4: Define growth experiments

```
Propose 1-2 experiments per product:
  - Hypothesis: "If we [do X], then [metric Y] will [increase/decrease] by [Z%]"
  - Implementation: what needs to change (copy, CTA, channel)
  - Duration: 1 week minimum
  - Measurement: exact metric and how to measure
```

### Step 5: Create action items

```
FOR EACH deliverable:
  - Create GitHub Issue with label: distribution-agent, content/growth
  - Assign due date within the week
  - Include acceptance criteria
```

## Output

Produce the Weekly GTM Brief per the template in `distribution.system.md`.

## Acceptance Criteria

- [ ] Content calendar for the week (3-5 items per product)
- [ ] At least 1 growth experiment defined per product
- [ ] GitHub Issues created for each deliverable
- [ ] All copy marked for founder review before external publish
