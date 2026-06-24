---
name: bug-hunt
description: Root cause investigation — from quick code bug to multi-service outage. Hypothesis-driven, no guessing.
aliases: [debug, investigate, oncall, deep-dive, sleuth]
---

# Bug Hunt

Find and fix the root cause. Two modes depending on scope.

## Choose Mode

### Mode 1: Quick Debug
Known code bug, single service, stack trace available.

1. **Gather** — error message, stack trace, failing test, git log
2. **Hypothesize** — 3-5 possible causes, ranked by likelihood
3. **Test** — test each hypothesis, stop when confirmed
4. **Fix** — minimal fix + regression test
5. **Document** — commit: "fix: {desc} — root cause: {cause}"

### Mode 2: Deep Investigation
Unknown cause, multi-service, production outage, on-call.

1. **Define** — what's observable? when started? what changed? who affected?
2. **Data sources** — logs, git log, PRs, metrics, deployments
3. **Investigate** — follow each lead autonomously, don't stop at first finding
4. **Timeline** — build event timeline, mark probable root cause
5. **Report** — structured report: problem, root cause, evidence, fix, prevention
6. **Issue** — create GitHub Issue with the report

## Investigation Report Format (Mode 2)

```markdown
## Investigation Report

**Problem:** {description}
**Duration:** {start} → {end or ongoing}
**Impact:** {affected users/systems}

## Root Cause
{precise description}

## Evidence
1. {evidence}
2. {evidence}

## Timeline
| Time | Event |
|------|-------|
| T1   | {event} |
| T2   | {event} ← root cause here |

## Fix
{what to do}

## Prevention
{how to prevent recurrence}
```

## Rules

- Never guess — every fix backed by evidence
- Never fix symptoms instead of root cause
- Never add workarounds for code you don't understand
- Always add a regression test
- If pattern is generalizable → log self-heal trace
- Use strongest model for complex investigations
