---
name: coworker-flow-ship
triggers:
  - create pr
  - submit pr
  - pull request
  - open pr
  - raise pr
description: |
  Create a pull request with a clear summary of all changes. Applies review
  checkpoint to find appropriate reviewer and notify them.
services:
  category: coworker-dev
when_to_use: |
  After verification passes. When all tasks are committed and verified, create
  the PR to merge the changes.
when_not_to_use: |
  Do not create PR if verification failed — fix issues first.
dependencies:
  - coworker-dev-verify
  - coworker-do-review-checkpoint
version: 1.0.0
---

# Create PR

Stage 5 of the workflow. Create a pull request with a clear summary.

## Process

### 1. Gather Context
```
→ git log main..HEAD --oneline
→ git diff main..HEAD --stat
→ Review all commit messages
```

### 2. Generate PR Summary
```
## Summary
{what was done, why, key decisions}

## Changes
- {bullet list of key changes, one per commit or file group}

## Testing
- {tests run, results}

## Verification
- ✅ Tests passing
- ✅ Lint clean
- ✅ Guardrails passed
```

### 3. Create PR
```bash
gh pr create \
  --title "{conventional type}: {short description}" \
  --body "{PR summary}" \
  --base main
```

### 4. Request Review
```
→ Find appropriate reviewer from team context
→ Add reviewer to PR
→ Send notification (Slack/Telegram per team config)
→ Return PR URL to user
```

## Rules
- PR title must follow Conventional Commits
- Every PR references a GitHub Issue (create one if missing)
- PR body must include verification results
- Never merge without human approval
- Branch naming: `{type}/{issue-id}-{short-description}`
