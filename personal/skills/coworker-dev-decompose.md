---
name: coworker-dev-decompose
triggers:
  - decompose
  - break down
  - plan tasks
  - split the work
description: |
  Break confirmed requirements into parallel-executable tasks grouped in waves.
  No file conflicts within a wave. Produces a task plan for user approval.
services:
  category: coworker-dev
when_to_use: |
  After understanding the requirements and getting user confirmation. When there
  are multiple files or components to change and parallelism would help.
when_not_to_use: |
  Skip for single-file, single-commit changes — go directly to execute.
dependencies:
  - coworker-dev-understand
version: 1.0.0
---

# Decompose → Tasks

Stage 2 of the workflow. Break the confirmed requirements into independent, parallelizable tasks.

## Goal
Produce a task breakdown with waves (parallel groups) that the user approves.

## Process

### 1. Explore the Codebase
```
→ Search for relevant files and systems
→ Read key files to understand existing patterns
→ Identify what needs to be created/modified/deleted
```

### 2. Define Tasks
Each task must be:
- **Atomic**: One file or one cohesive unit of work
- **Testable**: Has a clear done condition
- **Independent**: Can be implemented in isolation within its wave

Format:
```
### Task {id}: {name}
- **File(s)**: {paths}
- **What**: {1-line description}
- **Done when**: {verifiable condition}
```

### 3. Group into Waves
Waves determine execution order:
- **Wave 1**: Tasks with no dependencies (infrastructure, models, utilities)
- **Wave 2**: Tasks that depend on Wave 1
- **Wave N**: Tasks that depend on prior waves

Rule: **No two tasks in the same wave may modify the same file.**

### 4. Confirm with User
Show the wave structure and ask for confirmation:
```
## Task Plan

### Wave 1 (parallel)
- Task 1.1: {name} → {file}
- Task 1.2: {name} → {file}

### Wave 2 (parallel)
- Task 2.1: {name} → {file}

Continue with execute? (y/n)
```

## Rules
- Tasks within a wave MUST NOT share files
- Each wave should have 1-5 tasks for manageable parallelism
- If a task is unclear after codebase exploration, ask the user
- Keep task descriptions short — the subagent will figure out details
