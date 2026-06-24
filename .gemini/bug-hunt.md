---
name: bug-hunt
description: Scientific debugging — hypothesis → test → confirm → fix. Best with strongest model.
aliases: [debug, investigate-bug]
---

# Issue Debug

Systematic scientific debugging. No guessing — form hypothesis, test it, confirm, then fix.

## Model Recommendation
Use the strongest available model (Opus) for complex debugging.

## Process

### 1. Gather Evidence
```
→ Read error message / stack trace in full
→ Read the failing test or reproduction case
→ Read the code around the failure point
→ Check git log — when did this start failing?
→ Check if tests pass on main branch
```

### 2. Form Hypotheses
List 3-5 possible root causes, ranked by likelihood:
```
H1 (most likely): {hypothesis}
H2: {hypothesis}
H3: {hypothesis}
```

### 3. Test Each Hypothesis
For each hypothesis, define a minimal test:
```
Test H1: {what to check}
→ Run: {command or code change}
→ Expected if H1 is true: {result}
→ Actual: {result}
→ H1: CONFIRMED / REJECTED
```

Test in order — stop when first is confirmed.

### 4. Identify Root Cause
```
Root cause: {precise description}
Evidence: {what confirmed it}
Location: {file:line}
```

### 5. Fix
```
→ Minimal fix that addresses root cause
→ Do NOT over-fix or refactor surrounding code
→ Add regression test that would have caught this
→ Verify fix doesn't break other tests
```

### 6. Document
```
→ Update GitHub Issue with root cause and fix
→ Commit: "fix: {description} — root cause was {brief}"
→ If pattern is generalizable → log self-healing trace
```

## Anti-Patterns to Avoid
- Never "try something and see" without a hypothesis
- Never fix symptoms instead of root cause
- Never add workarounds for code you don't understand
- Never skip the regression test
