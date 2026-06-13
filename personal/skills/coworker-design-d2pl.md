---
name: coworker-design-d2pl
triggers:
  - d2pl
  - design to plan
  - create plan from design
  - break design into tasks
description: |
  Break DESIGN.md features into tasks grouped in waves with MAC (Minimum
  Acceptance Criteria). Produces a structured plan file ready for execution.
services:
  category: coworker-design
when_to_use: |
  When DESIGN.md is ready and needs to be turned into an executable plan.
  When user says "d2pl", "create a plan", or "break this into tasks".
when_not_to_use: |
  Do not use without a DESIGN.md. Use coworker-do-quick-task for small changes.
dependencies:
  - coworker-design-f2d
version: 1.0.0
---

# Design → Plan (d2pl)

Stage 3 of the 8-stage pipeline. Converts DESIGN.md into an executable plan file with waves and MAC.

## Process

### 1. Read Inputs
```
→ Read DESIGN.md — identify all features to implement
→ Read existing code structure — understand file locations
→ Check FEATURE.md for feature IDs
```

### 2. Decompose into Tasks
Each task must be:
- **Atomic** — one clear output (one file, one function, one endpoint)
- **Independent within its wave** — no file conflicts with sibling tasks
- **Completable in one subagent session**
- **Verifiable** — has a clear done condition

### 3. Group into Waves
```
Wave 1 (parallel): tasks with no dependencies
Wave 2 (parallel): tasks depending only on Wave 1
Wave 3 (sequential): tasks depending on Wave 2
...
```

**Key rule:** Tasks in the same wave must NOT modify the same file.

### 4. Define MAC
MAC = Minimum Acceptance Criteria: the smallest proof that the feature works.
- Not comprehensive tests
- Not full coverage
- Just: "if this passes, the feature basically works"

Example:
```
MAC:
- [ ] `POST /users` returns 201 with user object
- [ ] `GET /users/{id}` returns 200 or 404
- [ ] Unit test for UserService.create() passes
```

### 5. Output File
Create `docs/planning/plan_{feature_id}.md`:

```markdown
# Plan: {feature name}
**Feature ID:** {id}
**Created:** {date}
**Status:** PENDING

## MAC (Minimum Acceptance Criteria)
- [ ] {criterion}

## Wave 1 (parallel)
### Task 1.1 — {name}
- **File:** {path}
- **What:** {description}
- **Done when:** {criterion}

### Task 1.2 — {name}
...

## Wave 2 (sequential)
...
```
