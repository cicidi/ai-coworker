# AI Coworker

**Project context manager for AI coding assistants.**

AI Coworker keeps your IDE (Claude Code, OpenCode, Gemini, Cursor) aware of your project structure, active initiatives, and available skills. It auto-scans projects, injects context into your AI's config, and connects to [skill-factory](https://github.com/cicidi/skill-factory) for skill lifecycle management.

## What It Does

- **Auto-scan** projects — detect language, framework, dependencies, IDEs
- **Inject context** into CLAUDE.md — project catalog, initiative status, docs structure
- **Manage initiatives** — cross-project work with decisions, links, project scope
- **Track projects** — catalog with upstream/downstream relationships, knowledge pools
- **Sync skills** from config to all installed IDEs
- **Analytics** — session tracking with SQLite DB and web dashboard

## What It Doesn't Do

- Write code or follow a development pipeline
- Create or edit skills (that's [skill-factory](https://github.com/cicidi/skill-factory))
- Implement OWASP guardrails or code review (those are skills you get from skill-factory)

## Install

```bash
git clone https://github.com/cicidi/ai-coworker.git ~/ai-coworker
cd ~/ai-coworker
pip install --break-system-packages -e .
```

## Usage

```bash
coworker init              # Auto-scan project, generate config + CLAUDE.md context
coworker sync              # Sync config to all detected IDEs
coworker status            # Show current config status

# Project catalog
coworker project add       # Add a project to the catalog
coworker project list      # List all tracked projects
coworker project sync      # Inject catalog into IDE configs

# Initiatives (cross-project work)
coworker initiative start  # Create, add project, activate in one step
coworker initiative list   # List all initiatives

# Analytics
coworker analytics create-db   # Initialize session tracking database
coworker analytics dashboard   # View session stats
```

## How Context Injection Works

AI Coworker writes managed sections into your `CLAUDE.md` (or `instructions.md` for OpenCode):

```markdown
# Your CLAUDE.md — user-written content stays untouched

<!-- COWORKER:STATIC START -->
## Project Catalog
| Project | Path | Upstream | Downstream |
|---------|------|----------|------------|
| ai-coworker | ~/ai-coworker | - | skill-factory |

## Docs Directory Structure
...

## Coworker Skills
Prefer coworker skills for repeatable workflows...
<!-- COWORKER:STATIC END -->
```

When you activate an initiative:
```markdown
<!-- INITIATIVE:skill-migration START -->
## Active Initiative: skill-migration
> Migrate all skills from ai-coworker to skill-factory
...
<!-- INITIATIVE:skill-migration END -->
```

Your content outside these comment blocks is never modified.

## Skill Management

AI Coworker connects to [skill-factory](https://github.com/cicidi/skill-factory) for the full skill lifecycle:

| Task | Tool |
|------|------|
| Create a skill | skill-factory `skill-create` |
| Edit a skill | skill-factory `skill-edit` |
| Import external skill | skill-factory `skill-import` |
| List/install skills | `coworker sync` |

Skills live in skill-factory. AI Coworker syncs them to your IDE.
