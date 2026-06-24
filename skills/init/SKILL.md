---
name: init
description: Auto-scan project and generate config — detects language, dependencies, IDEs
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

Auto-scan project and generate configuration.

## Usage

```bash
coworker init
```

CLI will:
1. Scan the project for language, framework, dependencies
2. Detect installed IDEs
3. Show findings for confirmation
4. Generate `coworker.yaml`
5. Generate/update `CLAUDE.md` with Project Context

After init, run `coworker sync` to apply.
