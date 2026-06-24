---
name: dev-feat-plan-to-code
description: Execute a plan file via orchestrator + subagent model. One task = one subagent = one commit.
aliases: [pl2c, execute-plan]
---

# Plan → Code (pl2c)

Stage 4 of the 8-stage pipeline. Executes a plan file using orchestrator + subagents.

## Orchestrator Behavior

### 1. Load Plan
```
→ Read docs/planning/plan_{feature_id}.md
→ Verify plan status is PENDING or IN_PROGRESS
→ Show wave structure to user, confirm before starting
```

### 2. Execute Wave by Wave

For each wave:
```
→ Identify all tasks in this wave
→ Tasks in same wave: run in parallel (spawn subagents)
→ Wait for all tasks in wave to complete before next wave
→ Verify no file conflicts within wave before spawning
```

### 3. Subagent Instructions (per task)
Each subagent receives:
```
You are implementing Task {id}: {name}

Context:
- File to create/modify: {path}
- What to implement: {description}
- Done when: {criterion}

Rules:
1. Implement ONLY this task — nothing else
2. Write tests alongside code
3. After implementation: git add {file} && git commit -m "{conventional commit}"
4. Do NOT modify any other files
5. Report: DONE or FAILED with reason
```

### 4. Track Progress
Update plan file after each task:
```markdown
### Task 1.1 — {name}
**Status:** ✅ COMPLETE
**Commit:** abc1234
```

### 5. Trigger Verify
After all waves complete:
```
→ Spawn fresh session
→ Run verify (MAC check)
→ Report results
```

## Quick Mode (< 100 lines)
For small changes, skip orchestrator:
```
→ Single task
→ Current session (no subagent)
→ Implement → test → commit → verify
```
