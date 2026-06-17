---
name: coworker-dev-verify
triggers:
  - verify
  - check
  - validate
  - run tests
  - quality check
description: |
  Run verification checks — tests, lint, guardrails — before creating a PR.
  Runs in a fresh session for objective assessment.
services:
  category: coworker-dev
when_to_use: |
  After all tasks are implemented and committed. Before creating a PR. Must run
  in a fresh session to avoid context contamination from the coding session.
when_not_to_use: |
  false
dependencies:
  - coworker-do-guardrails
  - coworker-do-code-review
  - coworker-do-code-conventions
  - coworker-do-unit-tests
version: 1.0.0
---

# Verify

Stage 4 of the workflow. Verify all changes work correctly before PR.

## Why Fresh Session?
Context contamination from the coding session can make the AI think things work when they don't. A fresh session objectively checks the code.

## Process

### 1. Understand What Changed
```
→ git log main..HEAD --oneline
→ git diff main..HEAD --stat
→ Read the PR description or task summary from the user
```

### 2. Run Verification Checks

**Tests:**
```bash
→ Run the project's test suite
→ Ensure all new and existing tests pass
→ If no test command found, ask user
```

**Lint & Format:**
```bash
→ Run linter if configured
→ Run formatter if configured
→ Fix any issues
```

**Guardrails:**
```
→ Load commit-guardrails skill
→ Run OWASP Top 10 checks on all changed files
→ Run code conventions check
→ Run code review (anti-pattern check)
```

### 3. Manual Verification
```
→ Check that every task's "done when" condition is met
→ Verify the feature/fix actually works end-to-end
→ Check for any TODO or unfinished code
```

### 4. Report

```
## Verification Report

**Branch:** {branch}
**Commits:** {N} commits

| Check | Status | Notes |
|-------|--------|-------|
| Tests | ✅ / ❌ | |
| Lint | ✅ / ❌ | |
| Guardrails | ✅ / ❌ | |
| Done conditions | ✅ / ❌ | |

**Overall:** PASS / FAIL
```

### 5. On Failure
```
→ Fix the issue in this session
→ Re-run verification
→ Loop until all checks pass
```

### 6. On Pass
```
→ Proceed to PR stage
```
