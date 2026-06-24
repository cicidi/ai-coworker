---
name: self-heal
description: Log user corrections to .self-healing/traces/ for pattern analysis. Auto-installs hook if missing.
license: MIT
compatibility: claude-code,opencode,gemini
metadata:
  triggers:
    - self-heal
    - log correction
    - heal
  when_to_use: After user corrects AI behavior. Auto-detected via hook on keywords (no, don't, stop, wrong).
  audience: ai-coworker
---

# self-heal

Log every user correction to `.self-healing/traces/{date}.yaml`.

## Usage

```bash
# Manual trigger
coworker self-heal

# Or AI auto-triggers via .claude/hooks/on-self-heal.sh
```

## What it does

1. Checks if `.claude/hooks/on-self-heal.sh` exists
2. If not, offers to install the hook
3. Writes correction trace to project's `.self-healing/traces/`
4. Run `self-analyze` later to find patterns across traces
