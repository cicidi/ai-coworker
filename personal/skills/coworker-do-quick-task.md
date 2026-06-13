---
name: coworker-do-quick-task
triggers:
  - quick fix
  - small change
  - hotfix
  - minor tweak
  - bug fix under 100 lines
description: |
  Small change (under 100 lines) without the full PRD/Design/Plan pipeline.
  For bug fixes, config tweaks, and simple one-off tasks.
services:
  category: coworker-do
when_to_use: |
  When the change is under 100 lines, well-understood, and does not require
  design discussion. Bug fixes, typos, config changes, minor refactors.
when_not_to_use: |
  Do not use for new features, architectural changes, or anything needing
  design review. Use the full 8-stage pipeline instead.
version: 1.0.0
---

# Quick Task

For changes under 100 lines that don't need the full 8-stage pipeline.

## When to Use
- Bug fixes
- Config changes
- Typo/documentation fixes
- Small refactors (renaming, moving)
- Dependency updates
- Single-file changes

## When NOT to Use (use full pipeline instead)
- New features with API changes
- Database schema changes
- Changes to auth/security logic
- Changes affecting multiple services
- Anything requiring design review

## Process

### 1. Confirm Scope
```
→ Estimate lines of change
→ If > 100 lines: "This seems larger than quick-task scope. Use full pipeline? (y/n)"
→ If touches auth/security/DB: warn and confirm
```

### 2. Create GitHub Issue (if bug)
```
→ Title: "fix: {short description}"
→ Body: what's broken, what the fix is
→ Label: bug
```

### 3. Implement
```
→ git checkout -b fix/{issue-id}-{description} (or chore/, docs/)
→ Make changes
→ Run tests / linter
```

### 4. Guardrails Check (auto)
Runs automatically:
- OWASP checks (no secrets, no injection, no hardcoded creds)
- Conventional commit format
- No TODO without issue reference

### 5. Commit & PR
```
git add {specific files}
git commit -m "fix: {description} (closes #{issue})"
gh pr create --title "fix: {description}" --body "Closes #{issue}"
```

### 6. Verify
Quick MAC check — run relevant tests, confirm fix works.
