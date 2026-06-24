---
name: self-analyze
description: Scan .self-healing/traces/, find patterns, inject summary into CLAUDE.md
license: MIT
compatibility: claude-code,opencode,gemini
metadata:
  triggers:
    - self-analyze
    - analyze traces
    - find patterns
    - self improve
  when_to_use: Periodically to find recurring AI mistakes and generate rules
  audience: ai-coworker
---

# self-analyze

Scan project correction traces, find patterns, inject rules into CLAUDE.md.

## Usage

```bash
coworker self-analyze
```

## What it does

1. Reads all `.self-healing/traces/*.yaml`
2. Groups corrections by pattern, counts frequency
3. Generates summary in `<!-- SELF-ANALYZE -->` block
4. Injects into project's CLAUDE.md
