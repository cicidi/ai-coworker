---
name: init
description: Initialize the AI coworker for a new project — 5-step interactive setup
license: MIT
compatibility: claude-code,opencode,gemini
metadata:
  triggers:
    - init
    - setup coworker
    - initialize ai coworker
    - coworker init
  when_to_use: When setting up ai-coworker for a new project
  audience: ai-coworker
---

# init

Initialize the AI coworker for a new project. Interactive 5-step setup.

## Usage

```bash
coworker init
```

Interactive prompts will guide you through:
1. Scan project directory
2. Generate CLAUDE.md with project-specific rules
3. Detect identity (username, team)
4. Create local config (coworker.yaml)
5. Install hooks and sync to IDEs
