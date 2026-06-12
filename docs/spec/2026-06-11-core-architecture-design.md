# Core Architecture Design

<!-- PROTECTED -->
Project: ai-coworker
Last Updated: 2026-06-11
<!-- END PROTECTED -->

## Architecture Overview

```
[coworker CLI] → [Config Manager] → [IDE Adapters]
                      ↓
              [coworker.yaml / .mcp.json]
                      ↓
              [Claude Code / OpenCode / Gemini / Cursor]
```

Single Python CLI that reads YAML config and propagates skills, MCP servers, and permissions to target IDEs.

## Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| CLI framework | Click | Rich terminal UI, composable commands |
| Data models | Pydantic 2 | Strict schema validation for YAML config |
| Config format | YAML | Human-readable, existing ecosystem |
| Output formatting | Rich | Tables, panels, progress bars |
| Package manager | setuptools/pyproject.toml | Python standard |

## Data Model

**coworker.yaml** — source of truth for:
- MCP servers (name, command, args, env)
- Skills (name, source path, triggers)
- Permissions (tool allow/deny rules)
- Tool overrides (custom configurations per IDE)

**Project Catalog** (`~/.coworker/project.yaml`):
- List of all projects with paths, upstream/downstream relationships, knowledge pools

**Initiatives** (`~/.coworker/initiatives/<name>.yaml`):
- Per-workstream config: branches, decisions, links, reference docs

## IDE Adapters

| Adapter | Targets | Key Behavior |
|---------|---------|-------------|
| `adapters/claude.py` | `~/.claude/commands/`, `settings.local.json` | Context injection via HTML comments in CLAUDE.md |
| `adapters/opencode.py` | `~/.opencode/instructions/` | Context injection in instructions.md |
| `adapters/gemini.py` | `~/.gemini/` | Config sync |
| `adapters/cursor.py` | `.cursor/rules/` | Symlinks from Claude |

## Security Design

- No auth — single developer, local machine
- Secrets in env vars only (`coworker.yaml` references `$ENV_VAR`)
- `.local_config.yaml` gitignored (identity, project name)
- `.env` gitignored
- No network calls in core sync (all local file operations)

## Open Questions

- [ ] Docker/devcontainer support for portable setup
