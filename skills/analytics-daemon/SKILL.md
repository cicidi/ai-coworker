---
name: analytics-daemon
description: Auto-import daemon — scans projects every 30 minutes, imports new sessions into SQLite
license: MIT
compatibility: claude-code,opencode,gemini
metadata:
  triggers:
    - analytics-daemon
    - start analytics daemon
    - auto import sessions
  when_to_use: When user wants continuous auto-import of sessions
  audience: ai-coworker
---

# analytics-daemon

Run the auto-import daemon to continuously import new sessions.

## Usage

```bash
coworker analytics daemon
```

The daemon polls every 30 minutes:
- Scans Claude Code hooks sessions from `~/.coworker/analytics/sessions/`
- Scans OpenCode sessions from `~/.local/share/opencode/opencode.db`
- Only imports sessions not yet in analytics.db
- Writes checkpoint to `~/.coworker/analytics/checkpoint.json`
