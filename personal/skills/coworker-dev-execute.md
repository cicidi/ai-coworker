---
name: coworker-dev-execute
triggers:
  - execute
  - implement
  - build
  - run the tasks
  - code it
description: |
  Execute tasks wave by wave using parallel subagents. One task = one subagent
  = one atomic commit. Orchestrator manages the waves and reviews results.
services:
  category: coworker-dev
when_to_use: |
  After tasks have been decomposed and user approved the plan. Spawns parallel
  subagents to implement each task concurrently within a wave.
when_not_to_use: |
  Do not use without a confirmed task plan. For single-file changes, skip
  decompose and go directly to execute with a single task.
dependencies:
  - coworker-dev-decompose
  - coworker-do-guardrails
  - coworker-do-code-review
version: 1.0.0
---

# Execute

Stage 3 of the workflow. Implement the task plan wave by wave using parallel subagents.

## Orchestrator Behavior

### 1. Execute Wave by Wave
```
For each wave (sequentially):
  → Spawn subagents for all tasks in this wave (in parallel)
  → Wait for all subagents to complete
  → Review results before moving to next wave
```

### 2. Subagent Per Task
Each subagent receives:
```
You are implementing Task {id}: {name}

Context:
- File(s) to create/modify: {paths}
- What to implement: {description}
- Done when: {criterion}

Rules:
1. Implement ONLY this task — nothing else
2. Write tests alongside code
3. Follow existing code patterns and conventions
4. After done: git add {files} && git commit -m "{conventional commit}"
5. Report: DONE or FAILED with reason
```

### 3. Review Between Waves
After each wave:
```
→ Check all subagent results
→ If any FAILED: pause, diagnose with user, fix or re-plan
→ If all DONE: proceed to next wave
```

### 4. On Failure
```
→ Show the failed task and error
→ Ask user: retry / skip / replan?
→ Do NOT silently retry — user decides
```

## Rules
- One task = one subagent = one atomic commit
- Subagents must follow: `feat:` / `fix:` / `chore:` etc.
- No subagent modifies files outside its assigned task
- All wave tasks must complete before proceeding
- After all waves: auto-trigger verify stage
