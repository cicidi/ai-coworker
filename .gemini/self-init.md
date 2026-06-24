---
name: self-init
description: Auto-scan project, confirm findings, generate CLAUDE.md and coworker.yaml
aliases: [setup, init]
---

# Init

Run `coworker init` to auto-scan the project and generate configs.

## What it does

1. Scans package.json/pyproject.toml/go.mod/Cargo.toml for language & deps
2. Detects installed IDEs (Claude Code, OpenCode, Gemini, Cursor)
3. Shows findings to user for confirmation
4. Generates coworker.yaml with project settings
5. Generates/updates CLAUDE.md with Project Context section

## Rules

- Run `coworker init` — it handles everything automatically
- User only needs to confirm the scan results
- If CLAUDE.md already has Project Context, skip that section
- After init, remind user to run `coworker sync`
