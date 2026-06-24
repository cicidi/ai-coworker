---
name: analytics-once
description: Import new sessions once — scans for unimported Claude Code and OpenCode sessions
license: MIT
compatibility: claude-code,opencode,gemini
metadata:
  triggers:
    - analytics-once
    - import sessions once
    - check for new sessions
  when_to_use: When user wants to import sessions without running the daemon
  audience: ai-coworker
---

# analytics-once

Import new sessions from Claude Code and OpenCode into the analytics database.

## Usage

```bash
coworker analytics once
```

Scan for new sessions and import only those not yet in analytics.db.
Write checkpoint so the same sessions are not imported again.
