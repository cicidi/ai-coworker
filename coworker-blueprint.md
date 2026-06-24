# AI Coworker System — Blueprint

> **Purpose:** Complete specification of the AI Coworker context management system. Give this to any LLM to recreate it.

> **What is AI Coworker?** A Python CLI tool that keeps your AI coding assistants aware of your projects, initiatives, and available skills. It auto-scans projects, injects managed context blocks into IDE configs, syncs skills from [skill-factory](https://github.com/cicidi/skill-factory), and tracks session analytics. It's the data foundation for building an autonomous coding agent.

> **What it is NOT:** A development workflow tool. Skills for coding, testing, reviewing, debugging — those come from skill-factory, not ai-coworker. AI Coworker provides the context, memory, and data layer that makes those skills effective.

---

## Table of Contents

1. [Core Purpose](#1-core-purpose)
2. [Directory Structure](#2-directory-structure)
3. [Context Injection System](#3-context-injection-system)
4. [Project Catalog](#4-project-catalog)
5. [Initiative Management](#5-initiative-management)
6. [CLI Commands](#6-cli-commands)
7. [Skill Management](#7-skill-management)
8. [Analytics](#8-analytics)
9. [Configuration Layer](#9-configuration-layer)
10. [IDE Adapters](#10-ide-adapters)
11. [Installer Specification](#11-installer-specification)

---

## 1. Core Purpose

AI Coworker solves three problems:

### Problem 1: Your AI doesn't know your project

AI assistants start with zero context. They don't know what language, framework, or dependencies you use. They don't know your team's projects or how they relate.

**Solution:** `coworker init` auto-scans → generates config → `coworker sync` injects context into IDE config files.

### Problem 2: Context drifts across sessions

You're working on initiative "skill-migration" across 3 projects. Your AI knows about project A but not B or C.

**Solution:** `coworker initiative activate` injects the current initiative into your IDE config. Deactivate when done. Context follows you.

### Problem 3: Skills are scattered

Team skills live in skill-factory, personal tweaks in random folders, nothing is synced.

**Solution:** `coworker sync` reads `coworker.yaml` → copies configured skills to all installed IDEs.

### Problem 4: No memory across sessions

Every AI session starts from zero. Past learnings, effective workflows, and mistakes are lost.

**Solution:** Analytics pipeline imports Claude Code and OpenCode session data into SQLite. Knowledge extraction identifies repeatable patterns. This data powers a future autonomous coding agent that remembers what works.

---

## 2. Directory Structure

```
ai-coworker/
├── CLAUDE.md              # AI rules: conventions, guardrails
├── README.md              # Install and usage guide
├── TODO.md                # Development roadmap
├── coworker-blueprint.md  # This document
├── pyproject.toml         # Python package config
├── src/coworker/          # CLI tool
│   ├── cli.py             # All CLI commands
│   ├── config.py          # Config loading/merging
│   ├── models.py          # Pydantic data models
│   ├── adapters/          # IDE adapters
│   │   ├── claude.py      # Claude Code: settings, skills, context injection
│   │   ├── opencode.py    # OpenCode: same
│   │   └── gemini.py      # Gemini CLI: settings, skills
│   ├── initiatives/       # Initiative lifecycle
│   │   └── manager.py     # Create, activate, deactivate, inject context
│   ├── analytics/         # Session tracking
│   │   ├── db.py          # SQLite schema (sessions, messages, tool_calls)
│   │   ├── import_data.py # Import JSONL → SQLite
│   │   └── knowledge.py   # Knowledge extraction
│   └── dashboard/         # Web dashboard
├── skills/                # CLI command skills (SKILL.md format)
├── .cursor/rules/         # IDE instruction files (synced to IDEs)
├── .opencode/instructions/
├── .gemini/
├── .claude/commands/
└── tests/python/          # Python tests
```

---

## 3. Context Injection System

The heart of AI Coworker. Writes managed blocks into IDE config files without touching user content.

### Block types

**Static block** — always present, injected by `coworker project sync`:

```markdown
<!-- COWORKER:STATIC START -->
## Project Catalog
| Project | Path | Upstream | Downstream |
|---------|------|----------|------------|

## Docs Directory Structure
Standard directory layout for docs/

## Coworker Skills
Usage guidance for coworker skills

## Additional Behavioral Guidelines
(From andrej-karpathy-skills, with attribution)
<!-- COWORKER:STATIC END -->
```

**Initiative block** — injected only when an initiative is active:

```markdown
<!-- INITIATIVE:skill-migration START -->
## Active Initiative: skill-migration
> Migrate all skills from ai-coworker to skill-factory

### Projects in scope
| Project | Role | Branches |
|---------|------|----------|

### Key Decisions
- 2026-06-23: Migrate personal-skills first (by cicidi)

### Reference Docs
- `docs/spec/skill-migration.md` — Migration plan

### Links
- [skill-factory](https://github.com/cicidi/skill-factory)
<!-- INITIATIVE:skill-migration END -->
```

### Injection logic

```
coworker project sync
  → reads project.yaml catalog
  → builds static block
  → if CLAUDE.md has COWORKER:STATIC markers: replace between them
  → if not: append at end
  → writes CLAUDE.md

coworker initiative activate
  → removes any existing INITIATIVE blocks
  → appends new initiative block
  → writes CLAUDE.md

coworker initiative deactivate
  → removes INITIATIVE blocks
  → writes CLAUDE.md
```

### Supported IDEs

| IDE | File modified | Adapter |
|-----|--------------|---------|
| Claude Code | `CLAUDE.md` | `claude.py` |
| OpenCode | `.opencode/instructions.md` | `opencode.py` |
| Gemini CLI | (not yet) | `gemini.py` |
| Cursor | (not yet) | — |

Static and initiative blocks are injected into both Claude Code and OpenCode configs.

---

## 4. Project Catalog

Tracks all projects you work on and their relationships.

### Data model

```yaml
# project.yaml
projects:
  - name: ai-coworker
    local_path: ~/ai-coworker
    upstream: []
    downstream:
      - name: skill-factory
    knowledge_pool:
      - type: github
        url: https://github.com/cicidi/ai-coworker
    refs:
      github:
        - owner: cicidi
          repo: ai-coworker
```

### Commands

```
coworker project add     → Interactive add with upstream/downstream
coworker project edit    → Modify an entry
coworker project list    → Show all tracked projects
coworker project show    → Detail view of one project
coworker project remove  → Delete from catalog
coworker project sync    → Inject catalog into IDE configs
```

---

## 5. Initiative Management

Initiatives are cross-project pieces of work — features, migrations, refactors that span multiple repos.

### Data model

```yaml
# .coworker/initiatives/skill-migration.yaml
name: skill-migration
description: Migrate all skills from ai-coworker to skill-factory
status: active
projects:
  - name: ai-coworker
    role: source
    branches: [main]
  - name: skill-factory
    role: target
    branches: [master]
decisions:
  - date: "2026-06-23"
    decision: "Migrate personal-skills first"
    rationale: "They're simpler"
    by: cicidi
links:
  - url: https://github.com/cicidi/skill-factory
    title: skill-factory repo
reference_docs:
  - path: docs/spec/skill-migration.md
    title: Migration plan
```

### Lifecycle

```
coworker initiative start    → create + add projects + activate (one step)
coworker initiative create   → just create the YAML
coworker initiative activate → inject into IDE configs, mark ~/.coworker/initiatives/.active
coworker initiative deactivate → remove from IDE configs
coworker initiative edit     → modify YAML
coworker initiative list     → show all
coworker initiative show     → full detail
coworker initiative remove   → delete YAML + deactivate
```

Active initiative is tracked in `~/.coworker/initiatives/.active`.

---

## 6. CLI Commands

```
coworker init              # Auto-scan project, generate config + CLAUDE.md context
coworker sync              # Sync config to all detected IDEs
coworker status            # Show global + project config status

coworker analytics create-db    # Initialize ~/.coworker/analytics/analytics.db
coworker analytics import       # Import session JSONL → SQLite
coworker analytics dashboard    # Web dashboard on localhost

coworker project add/edit/list/remove/show   # Project catalog
coworker project sync                        # Inject catalog into IDE configs

coworker initiative start      # Create + activate in one step
coworker initiative create     # Create initiative YAML
coworker initiative edit       # Edit initiative YAML
coworker initiative activate   # Inject into IDE configs
coworker initiative deactivate # Remove from IDE configs
coworker initiative list       # List all
coworker initiative show       # Show detail
coworker initiative remove     # Delete permanently

coworker skill list            # List configured skills
coworker skill new             # Scaffold new skill
```

### init behavior

`coworker init` auto-scans the current directory:

1. Reads `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml`
2. Detects: language, framework, dependencies, test/lint commands
3. Detects: installed IDEs (Claude Code, OpenCode, Gemini, Cursor)
4. Shows summary → user confirms
5. Creates `coworker.yaml`
6. Adds/updates `CLAUDE.md` with `## Project Context` section

Example output:
```
Project Scan: my-app
  Language:      Node.js
  Framework:     React, Express
  Dependencies:  next, typescript, prisma...
  Detected IDEs: claude, opencode
  Test command:  npm test

Create project config with these settings? [Y/n]:
```

---

## 7. Skill Management

AI Coworker manages skill **distribution**, not skill **creation**. Skills are created and maintained in [skill-factory](https://github.com/cicidi/skill-factory).

### Skill lifecycle

```
skill-factory          ai-coworker               IDE
─────────────          ─────────────              ───
skill-create  ──→  listed in coworker.yaml  ──→  .claude/commands/
skill-edit    ──→  coworker sync           ──→  .cursor/rules/
skill-import  ──→                          ──→  .opencode/instructions/
                                              ──→  .gemini/
```

### Config example

```yaml
# coworker.yaml
skills:
  - name: flow-understand
    path: ~/skill-factory/ai-coworker-skills/flow-understand/SKILL.md
    enabled: true
  - name: gate-guardrails
    path: ~/skill-factory/ai-coworker-skills/gate-guardrails/SKILL.md
    enabled: true
```

`coworker sync` copies each enabled skill to all detected IDE directories. The skill content (how to understand requirements, how to run guardrails) is defined in skill-factory — ai-coworker just distributes it.

---

## 8. Analytics & Memory Management

Tracks AI session activity across Claude Code and OpenCode. Records skill usage, tool calls, token costs, and extracts reusable knowledge. This data is the foundation for building an autonomous coding agent.

### Database schema

```sql
-- ~/.coworker/analytics/analytics.db
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    title TEXT,
    model TEXT,
    cost REAL,
    tokens_input INTEGER,
    tokens_output INTEGER
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id),
    role TEXT,
    content TEXT,
    timestamp TEXT
);

CREATE TABLE tool_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id),
    tool_name TEXT,
    input TEXT,
    output TEXT,
    duration_ms INTEGER
);

CREATE TABLE knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    type TEXT,
    session_id TEXT,
    project TEXT,
    skills TEXT,
    summary TEXT,
    evidence TEXT
);
```

### Data pipeline

```
Claude Code sessions  ──→  JSONL files  ──→  SQLite
OpenCode sessions     ──→  opencode.db  ──→  SQLite
                                              │
                                              ├── session_summaries
                                              ├── knowledge cards
                                              └── dashboard
                                              │
                                              ▼
                                         Obsidian vault
                                      (searchable memory)
```

### Commands

```
coworker analytics create-db   → Initialize the SQLite database
coworker analytics import      → Import OpenCode JSONL sessions
coworker analytics dashboard   → Start web UI at http://localhost:8080
```

### Road to Autonomy

The analytics data enables:

1. **Skill effectiveness** — Which skills are used most? Which fail often?
2. **Pattern detection** — What workflows repeat across sessions?
3. **Knowledge extraction** — What got learned and should persist?
4. **Auto-coding agent** — Given session history + skill catalog + project context,
   the agent can autonomously pick the right skill, apply the right guardrails,
   and learn from past mistakes.

### Commands

```
coworker analytics create-db   → Initialize the SQLite database
coworker analytics import      → Import OpenCode JSONL sessions
coworker analytics dashboard   → Start web UI at http://localhost:8080
```

---

## 9. Configuration Layer

### Global config — `~/.coworker/coworker.yaml`

```yaml
version: "1"
scope: global
mcp: []
skills:
  - name: flow-understand
    path: ~/skill-factory/ai-coworker-skills/flow-understand/SKILL.md
    enabled: true
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
skills: []
permissions:
  allow: []
  deny: []
```

### Merge logic

1. Start with global config
2. Project `permissions.allow` extends global `allow`
3. Project `permissions.deny` overrides
4. Project `skills` merged with global `skills`
5. Project `claude`/`gemini`/`opencode` settings override global

---

## 10. IDE Adapters

Each adapter handles two things:
1. **Sync**: copy skills, write settings.json, configure permissions
2. **Context injection**: write managed blocks into IDE config files

| Adapter | Sync target | Context injection target |
|---------|------------|-------------------------|
| `claude.py` | `~/.claude/skills/`, `settings.json` | `CLAUDE.md` |
| `opencode.py` | `.opencode/`, `config.json` | `.opencode/instructions.md` |
| `gemini.py` | `.gemini/`, `settings.json` | (not yet) |

---

## 11. Installer Specification

### Dependencies
- Python 3.10+
- `click`, `rich`, `pyyaml`, `pydantic`
- Optional: `uvicorn` (analytics dashboard)

### Install

```bash
git clone https://github.com/cicidi/ai-coworker.git
cd ai-coworker
pip install --break-system-packages -e .
```

### First run

```bash
coworker init        # Creates global + project config
coworker sync        # Syncs skills to your IDEs
coworker status      # Verify everything is set up
```

### What gets created

| Step | Creates |
|------|---------|
| `coworker init --global` | `~/.coworker/coworker.yaml`, `~/.coworker/skills/` |
| `coworker init` (project) | `./coworker.yaml`, updates `CLAUDE.md` |
| `coworker sync` | Copies skills to IDE dirs, writes settings |
| `coworker analytics create-db` | `~/.coworker/analytics/analytics.db` |
