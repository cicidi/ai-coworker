---
name: bug-create
description: Doc-driven change request via GitHub Issue — 6-step structured discussion before any code
aliases: [new-issue, create-issue]
---

# Issue Create

All non-trivial changes start with a GitHub Issue. Code comes after discussion, not before.

## 6-Step Process

### Step 1 — Detect Signal
Triggers:
- User reports a bug
- User wants a new feature
- AI detects inconsistency in code/docs
- AI detects a potential OWASP violation

### Step 2 — Classify
```
Type: bug | feature | refactor | docs | security | chore
Urgency: critical | high | medium | low
Size estimate: XS (<1h) | S (<4h) | M (<1d) | L (<3d) | XL (>3d)
```

### Step 3 — Discussion
Ask structured questions based on type:

**For bugs:**
- What is the expected behavior?
- What is the actual behavior?
- Can you reproduce it? Steps?
- What's the impact?

**For features:**
- What problem does this solve?
- Who benefits?
- Any alternative approaches considered?
- Dependencies on other features?

### Step 4 — Draft Issue
```markdown
## Summary
{1-2 sentence description}

## Context
{background, why this matters}

## Proposed Solution
{approach, not implementation details}

## Acceptance Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}

## Out of Scope
- {what this issue does NOT cover}
```

### Step 5 — Create via GitHub MCP
```
→ Create issue in repo from .local_config.yaml
→ Add appropriate labels
→ Assign to cicidi
→ Return issue URL
```

### Step 6 — Proceed
```
→ "Issue #{number} created: {url}"
→ "Ready to start implementation? (y/n)"
→ If yes: use quick-task or full pipeline based on size
```
