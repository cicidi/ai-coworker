---
name: analytics-import
description: Import session JSONL files into the analytics SQLite database
license: MIT
compatibility: claude-code,opencode,gemini
metadata:
  triggers:
    - analytics-import
    - import analytics data
    - import sessions to db
  when_to_use: When user needs to import session data into analytics
  audience: ai-coworker
---

# analytics-import

Import raw session JSONL files into the analytics SQLite database.

## Usage

```bash
coworker analytics import
```
