---
name: verify-plan
description: Post-execution MAC verification in a fresh session — confirms feature works before PR
aliases: [verify, mac-check, qp]
---

# Verify Plan (MAC Check)

Stage 7 of the 8-stage pipeline. Runs in a FRESH session (no context from coding session).

## Why Fresh Session?
Context contamination from the coding session can make AI think things work when they don't.
A fresh session has no assumptions — it objectively checks the code.

## Process

### 1. Load Plan
```
→ Read docs/planning/plan_{feature_id}.md
→ Extract MAC (Minimum Acceptance Criteria) section
→ List all criteria to verify
```

### 2. For Each MAC Criterion

**If criterion is testable via command:**
```bash
→ Run the verification command
→ Check output matches expected result
→ Mark: ✅ PASS or ❌ FAIL
```

**If criterion is structural:**
```
→ Read the relevant file
→ Check criterion is satisfied by code
→ Mark: ✅ PASS or ❌ FAIL
```

**If criterion requires running the app:**
```
→ Start app if possible
→ Make the required request/action
→ Verify response
→ Mark: ✅ PASS or ❌ FAIL
```

### 3. Report

```markdown
## MAC Verification Report

**Plan:** {feature_id}
**Verified:** {date}
**Session:** Fresh (no prior context)

| Criterion | Status | Notes |
|-----------|--------|-------|
| {criterion} | ✅ | |
| {criterion} | ❌ | {what failed} |

**Overall:** PASS ({N}/{total}) / FAIL ({N}/{total})
```

### 4. On Failure
```
→ Identify root cause of each failing criterion
→ Generate fix instructions (do NOT fix in this session — creates new plan task)
→ Update plan with FAILED status
→ Return to pl2c to fix
```

### 5. On Full Pass
```
→ Mark plan status: VERIFIED
→ Proceed to review-checkpoint (Stage 8)
```
