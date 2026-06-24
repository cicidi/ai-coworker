# AI Coworker System — Blueprint

> **Purpose:** Complete specification of the AI Coworker system. Give this to any LLM to recreate the entire system.

> **What is AI Coworker?** A Python CLI tool that adds skills, guardrails, and project context to your AI coding assistant (Claude Code, OpenCode, Gemini, Cursor). It auto-scans your project, generates config, and provides a structured 5-stage development workflow.

---

## Table of Contents

1. [Core Philosophy](#1-core-philosophy)
2. [Directory Structure](#2-directory-structure)
3. [5-Stage Workflow](#3-5-stage-workflow)
4. [Skill Catalog](#4-skill-catalog)
5. [CLI Commands](#5-cli-commands)
6. [Configuration Layer](#6-configuration-layer)
7. [Guardrails](#7-guardrails)
8. [Self-Healing](#8-self-healing)
9. [Installer Specification](#9-installer-specification)
10. [Example Configurations](#10-example-configurations)

---

## 1. Core Philosophy

> **"Human decides, AI executes."**

1. **Human-centric** — When uncertain, ask. Never assume.
2. **Rapid execution** — Once confirmed, move fast.
3. **Self-healing** — Log every correction. Patterns become rules.
4. **No documents** — All understanding lives in the conversation, not in PRD/FEATURE/DESIGN files.

---

## 2. Directory Structure

```
ai-coworker/
├── CLAUDE.md              # AI rules: pipeline, guardrails, conventions
├── README.md              # Install and usage guide
├── TODO.md                # Development roadmap
├── pyproject.toml         # Python package config
├── src/coworker/          # CLI tool source
│   ├── cli.py             # All CLI commands
│   ├── config.py          # Config loading/merging
│   ├── models.py          # Pydantic data models
│   ├── adapters/          # IDE adapters (claude, opencode, gemini)
│   ├── initiatives/       # Initiative manager
│   ├── analytics/         # SQLite analytics DB + knowledge extraction
│   └── dashboard/         # Analytics web dashboard
├── skills/                # CLI command skills (SKILL.md format)
│   ├── init/              # → coworker init
│   ├── analytics-*/       # → coworker analytics create-db / import / dashboard
│   ├── initiative-*/      # → initiative activate / deactivate / list / show / remove
│   ├── project-*/         # → project add / edit / list / remove / show / sync
│   ├── skill-list/        # → coworker skill list
│   └── status/            # → coworker status
├── .cursor/rules/         # Cursor IDE instruction files (27 .md files)
├── .opencode/instructions/ # OpenCode IDE instruction files
├── .gemini/               # Gemini CLI instruction files
├── .claude/commands/      # Claude Code instruction files
└── tests/python/          # Python tests
```

**Key design decisions:**
- `personal/` — gitignored, for per-developer local data
- `docs/` — gitignored, not published
- `global/` — deleted, config templates live in `cli.py` as Python strings
- Skills live in TWO places: IDE directories (runtime) + skill-factory repo (source)

---

## 3. 5-Stage Workflow

For any coding task, AI follows this pipeline:

```
Stage 1: flow-understand  → Clarify requirements, confirm with user
Stage 2: flow-split       → Break into parallel tasks, group in waves
Stage 3: flow-build       → Implement via parallel subagents (one commit per task)
Stage 4: flow-check       → Run tests + lint + guardrails in fresh session
Stage 5: flow-ship        → Create PR with summary, request review
```

### Wave-based parallelism

```
Wave 1 (parallel)           Wave 2 (depends on Wave 1)
├── Task 1.1: model.py      ├── Task 2.1: service.py
├── Task 1.2: types.ts      └── Task 2.2: api.ts
└── Task 1.3: config.py
```

**Rule:** No two tasks in the same wave modify the same file.

### Subagent model (Stage 3)

Each task spawns an isolated subagent:
```
Context: file to modify, what to implement, done condition
Rules: implement ONLY this task, write tests, commit atomically
Output: DONE with commit hash, or FAILED with reason
```

---

## 4. Skill Catalog

28 skills organized by function:

### flow-* — Development Pipeline
| Skill | Stage | Description |
|-------|-------|-------------|
| `flow-understand` | 1 | Parse requirements, ask clarifying questions |
| `flow-split` | 2 | Break into parallel tasks, group in waves |
| `flow-build` | 3 | Execute via parallel subagents |
| `flow-check` | 4 | Run tests, lint, guardrails |
| `flow-ship` | 5 | Create PR, request review |

### gate-* — Quality Gates
| Skill | Checks |
|-------|--------|
| `gate-guardrails` | OWASP Top 10: no secrets, injection, hardcoded creds |
| `gate-conventions` | Code style, naming, formatting |
| `gate-review` | Anti-pattern detection |
| `gate-tests` | Test coverage verification |
| `gate-ship` | Review checkpoint enforcement |

### self-* — Self-Management
| Skill | Purpose |
|-------|---------|
| `self-init` | Auto-scan project and generate config |
| `self-heal` | Log correction traces for pattern analysis |
| `self-analyze` | Analyze mistakes to generate rules |
| `self-patch` | Auto-generate patches |
| `self-strain` | Analyze strain sites (pain points) |

### bug-* — Debug & Issues
| Skill | Purpose |
|-------|---------|
| `bug-report` | Report coworker bugs to GitHub |
| `bug-create` | Create a GitHub issue |
| `bug-hunt` | Debug an issue |
| `bug-sleuth` | Investigate root cause |

### doc-* — Document Operations
| Skill | Purpose |
|-------|---------|
| `doc-merge` | Merge markdown docs preserving PROTECTED blocks |
| `doc-protect` | Manage PROTECTED blocks |
| `doc-review` | Request document review |

### connect-* — Integrations
| Skill | Service |
|-------|---------|
| `connect-github` | GitHub MCP |
| `connect-slack` | Slack MCP |
| `connect-discord` | Discord MCP |
| `connect-telegram` | Telegram MCP |
| `connect-gdrive` | Google Drive MCP |

---

## 5. CLI Commands

```
coworker init                     # Auto-scan project, generate config + CLAUDE.md
coworker sync                     # Sync skills to detected IDEs
coworker status                   # Show global + project config status

coworker analytics create-db      # Initialize ~/.coworker/analytics/analytics.db
coworker analytics import         # Import session JSONL into SQLite
coworker analytics dashboard      # Start analytics web dashboard

coworker project add/edit/list/remove/show   # Manage project catalog
coworker project sync                        # Inject catalog into IDE configs

coworker initiative start         # Quick-start: create + activate
coworker initiative create/edit   # Create or edit an initiative
coworker initiative activate      # Activate (inject into IDE configs)
coworker initiative deactivate    # Deactivate (remove from IDE configs)
coworker initiative list/show     # List or view initiatives
coworker initiative remove        # Permanently delete

coworker skill list/new           # Manage skills
```

### init behavior

`coworker init` auto-scans the project:

1. Reads `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml`
2. Detects: language, framework, dependencies, test/lint commands
3. Detects installed IDEs (Claude Code, OpenCode, Gemini, Cursor)
4. Shows summary → user confirms
5. Generates `coworker.yaml` + `CLAUDE.md` Project Context section

---

## 6. Configuration Layer

Two config files merged at runtime:

### Global config — `~/.coworker/coworker.yaml`
```yaml
version: "1"
scope: global
mcp: []
skills: []
permissions:
  allow:
    - Bash(git *)
    - Read(*)
    - Write(*)
claude:
  effortLevel: medium
```

### Project config — `./coworker.yaml`
```yaml
version: "1"
scope: project
mcp: []
skills: []
permissions:
  allow: []
  deny: []
```

Project permissions override global. Skills/MCP are merged.

### CLAUDE.md Context Injection

Two types of blocks are injected into `CLAUDE.md`:

```
<!-- COWORKER:STATIC START -->
## Project Catalog         ← from project.yaml
## Docs Directory Structure  ← auto-generated
## Coworker Skills           ← usage guidance
## Additional Behavioral Guidelines ← Karpathy rules (attributed)
<!-- COWORKER:STATIC END -->
```

```
<!-- INITIATIVE:{name} START -->
## Active Initiative: {name}    ← from initiative YAML
<!-- INITIATIVE:{name} END -->
```

---

## 7. Guardrails

Auto-applied before every commit (OWASP Top 10):

- **A01** Broken Access Control — no auth bypass, all endpoints protected
- **A02** Cryptographic Failures — no hardcoded secrets, use env vars
- **A03** Injection — parameterized queries, no user input in shell/HTML
- **A04** Insecure Design — validate inputs at boundaries
- **A05** Security Misconfiguration — no .env in git, no debug in prod
- **A06** Vulnerable Components — flag outdated deps
- **A07** Authentication Failures — tokens in env vars only
- **A08** Software Integrity — review dependency changes
- **A09** Logging Failures — no PII/tokens in logs
- **A10** SSRF — no server-side requests to user-provided URLs

Git conventions enforced:
- Branch naming: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`
- Commits: Conventional Commits format
- Never push to main/master — all changes through PR
- Every PR references a GitHub Issue

---

## 8. Self-Healing

Three-phase feedback loop:

1. **Trace** (`self-heal`) — On every user correction, log: what went wrong, what was fixed
2. **Analyze** (`self-analyze`) — Periodically scan traces for patterns
3. **Rule** — Convert patterns into new guardrails or skills

Example:
```
Trace: AI used `git add .` and committed secrets
→ Pattern: 3 occurrences in 2 weeks
→ Rule: Add "never use git add ." to commit conventions skill
```

---

## 9. Installer Specification

### Dependencies
- Python 3.10+
- `click`, `rich`, `pyyaml`, `pydantic`
- Optional: `uvicorn` (for analytics dashboard)

### Install
```bash
git clone https://github.com/cicidi/ai-coworker.git ~/ai-coworker
cd ~/ai-coworker
pip install --break-system-packages -e .
```

### What install does
1. Registers `coworker` CLI command
2. No automatic DB setup (run `coworker analytics create-db` manually)

### What init does
1. Scans project for language, framework, dependencies
2. Detects installed IDEs
3. Shows findings → user confirms
4. Creates `coworker.yaml` and updates `CLAUDE.md`

### What sync does
1. Reads global + project `coworker.yaml`
2. Copies skill files to each IDE's directory
3. Syncs permissions and settings
4. Injects project catalog into `CLAUDE.md`

---

## 10. Example Configurations

### Minimal project
```yaml
version: "1"
scope: project
permissions:
  allow:
    - Bash(git *)
    - Read(*)
    - Write(*)
```

### Full project with skills
```yaml
version: "1"
scope: project
skills:
  - name: flow-understand
    path: ~/ai-coworker/.cursor/rules/flow-understand.md
    enabled: true
  - name: gate-guardrails
    path: ~/ai-coworker/.cursor/rules/gate-guardrails.md
    enabled: true
permissions:
  allow:
    - Bash(git *)
    - Bash(npm *)
    - Bash(pytest *)
    - Read(*)
    - Write(*)
```
