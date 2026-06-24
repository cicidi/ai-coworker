# AI Coworker

Your AI-powered development teammate. Scans your project, syncs skills to your IDE, and follows a structured development workflow.

## Install

```bash
git clone https://github.com/cicidi/ai-coworker.git ~/ai-coworker
cd ~/ai-coworker
pip install --break-system-packages -e .
```

## Quick Start

```bash
coworker init         # Auto-scan project, generate config
coworker sync         # Sync skills to your IDE
coworker status       # Check everything is set up
```

## How It Works

AI Coworker adds skills and rules to your IDE (Claude Code, OpenCode, Gemini, Cursor). When you ask your AI to do something, it follows a **5-stage pipeline**:

| Stage | Skill | What happens |
|-------|-------|-------------|
| 1. Understand | `flow-understand` | AI asks clarifying questions, confirms scope |
| 2. Decompose | `flow-split` | Breaks work into parallel tasks, grouped in waves |
| 3. Execute | `flow-build` | Implements tasks via parallel subagents, one commit each |
| 4. Verify | `flow-check` | Runs tests, lint, guardrails in a fresh session |
| 5. Ship | `flow-ship` | Creates PR with summary, requests review |

### Quality Gates

Built-in guardrails run before every commit:

| Gate | Checks |
|------|--------|
| `gate-guardrails` | OWASP Top 10 — no secrets, injection, hardcoded creds |
| `gate-conventions` | Code style, naming, formatting |
| `gate-review` | Anti-pattern detection |
| `gate-tests` | Test coverage verification |

### Self-Management

| Skill | Purpose |
|-------|---------|
| `self-init` | Auto-scan project and generate config |
| `self-heal` | Log correction traces for pattern analysis |
| `self-analyze` | Analyze mistakes to generate rules |

## CLI Commands

```bash
coworker init              # Auto-scan project, generate config
coworker sync              # Sync skills to all detected IDEs
coworker status            # Show config status

coworker analytics create-db     # Initialize analytics database
coworker analytics import        # Import session data
coworker analytics dashboard     # Start analytics dashboard

coworker project add/edit/list/remove/show    # Manage project catalog
coworker project sync                          # Inject catalog into IDE configs

coworker initiative start/create/edit/activate/deactivate/list/show/remove
coworker skill list/new
```

Every command has a matching AI skill so your AI can run them for you.

## Skill Categories

28 skills organized by function:

| Category | Skills |
|----------|--------|
| `flow-*` | 5-stage development pipeline |
| `gate-*` | Code quality and security checks |
| `self-*` | AI self-management and healing |
| `bug-*` | Issue creation and debugging |
| `doc-*` | Document merging and protection |
| `connect-*` | IDE integrations (GitHub, Slack, etc.) |

## Configuration

`coworker init` generates two config files:

- `~/.coworker/coworker.yaml` — Global MCP servers, skills, permissions
- `./coworker.yaml` — Project-level overrides

Example:
```yaml
version: "1"
scope: project
skills:
  - name: flow-understand
    path: skills/flow-understand
    enabled: true
permissions:
  allow:
    - Bash(git *)
    - Read(*)
    - Write(*)
```
