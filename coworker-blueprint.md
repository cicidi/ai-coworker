# AI Coworker System — Complete Blueprint

> **Purpose:** This document is a complete specification for building a team-wide AI coworker system. Give this to a Claude (or any LLM) and it can recreate the entire system from scratch for any team.

> **Origin:** Based on a production system serving a 25-person fintech engineering team. All team-specific details have been generalized.

> **What is a "Coworker"?** A centralized Git repository that stores everything needed to align every team member's AI assistant (Claude Code, Cursor, Windsurf) with team standards — eliminating repeated mistakes, providing shared context, and creating a self-improving feedback loop.

---

## Table of Contents

1. [Core Philosophy](#1-core-philosophy)
2. [Four-Layer Skill Architecture](#2-four-layer-skill-architecture)
3. [Fork-Based Collaboration Model](#3-fork-based-collaboration-model)
4. [Configuration Layer Design](#4-configuration-layer-design)
5. [Directory Structure](#5-directory-structure)
6. [Eight-Stage Agentic Workflow](#6-eight-stage-agentic-workflow)
7. [Skill Catalog (41 Skills)](#7-skill-catalog-41-skills)
8. [MCP Integrations (9 Tools)](#8-mcp-integrations-9-tools)
9. [Guardrails / Safety Rules](#9-guardrails--safety-rules)
10. [Self-Healing System](#10-self-healing-system)
11. [Installer Specification](#11-installer-specification)
12. [Setup Questionnaire Flow](#12-setup-questionnaire-flow)
13. [Example Configurations](#13-example-configurations)
14. [Design Decisions & Rationale](#14-design-decisions--rationale)
15. [Getting Started: How to Build Your Own](#15-getting-started-how-to-build-your-own)

---

## 1. Core Philosophy

> **"Human decides, AI executes."**

**Four pillars:**

1. **Human-centric** — When AI is uncertain, it finds the right person to confirm. Never assume, or skip humans.
2. **Rapid execution** — Once humans confirm decisions, AI executes fast: writes code, syncs docs, sends messages.
3. **Continuous supervision** — AI monitors for problems in both the work (code bugs, missing tests) AND the coworker system itself (stale configs, outdated rules).
4. **Self-healing** — Discover problem → ask the right person → persist the answer → suggest PR → whole team learns.

---

## 2. Four-Layer Skill Architecture

Follows Java class inheritance model. More specific layers override less specific.

```
Layer 4: Personal
(~25 files per person)
Personal workflows, preferences
Location: personal/ (gitignored)

        ↑ overrides

Layer 3: Project
(per-service configs)
Service-specific skills, context
Location: templates/projects/{svc}/

        ↑ overrides

Layer 2: Role (optional)
Backend, Frontend, Architect, PM
Can be merged into Personal layer

        ↑ overrides

Layer 1: Team Common
(shared by everyone)
Team-wide rules, MCP configs
Location: templates/team-common/
```

**Priority:** Personal > Project > Role > Team Common

---

## 3. Fork-Based Collaboration Model

```
Upstream (team repo)          ← PRs from forks
templates/ = source
personal/ = template

        fork

  Person A    personal/ = gitignored, unique to each fork
  Person B
  Person C
```

**Workflow:**
1. Each team member forks the upstream repo
2. `personal/` folder is gitignored in each fork (never pushed upstream)
3. Team-common changes go through PRs to upstream
4. Good personal patterns → PR to upstream → team reviews → merge → everyone runs `update.sh`

**Key rule:** `personal/` in upstream is template-only. Never push personal configs to upstream.

---

## 4. Configuration Layer Design

```
secrets (tokens, passwords)
  ↑ stored in
environment vars (~/.zshrc, never committed)
  ↑ referenced by
global private (~/.config/{team}-coworker/config.yaml)
  ↑ overridden by
project private ({project}/.local_config.yaml, gitignored)
  ↑ overridden by
project public ({project}/.mcp.json, committed)
  ↑ overridden by
team public (templates/*/context/*.yaml, committed)
```

**Golden Rule:** Tokens ONLY in env vars. Config files reference variable names only (e.g., `$SPLUNK_TOKEN`).

---

## 5. Directory Structure

```
{team}-coworker/
├── templates/                      # All installable content
│   ├── team-common/                # Layer 1: Shared by everyone
│   │   ├── context/
│   │   │   ├── profiles/
│   │   │   │   └── team.yaml       # All team members + roles
│   │   │   └── projects/
│   │   │       └── projects.yaml   # Index of all team projects
│   │   └── skills/
│   │       ├── dev-ai-tool-setup-coworker.md
│   │       ├── dev-ai-tool-report-issue.md
│   │       ├── doc-create-skill.md
│   │       ├── doc-edit-skill.md
│   │       ├── doc-merge-docs.md
│   │       ├── doc-protection.md
│   │       ├── doc-review-request.md
│   │       ├── mcp-*.md            # MCP integration skills (9 files)
│   │       └── plugin-*.md         # Plugin skills (3 files)
│   └── personal/                   # Layer 4: Personal skill templates
│       ├── context/
│       │   └── config-template.yaml
│       └── skills/
│           ├── design-*.md         # 5 workflow skills (p2f, f2d, d2pl, c2d, c2f)
│           ├── dev-feat-*.md       # 2 execution skills (plan-to-code)
│           ├── dev-ai-tool-*.md    # 4 AI self-improvement skills
│           ├── issue-*.md          # 3 issue management skills
│           ├── commit-*.md         # 6 pre-commit/quality skills
│           └── project-*.md        # Project-specific skills
│   └── projects/
│       └── {service-name}/
│           ├── context/
│           │   └── project-context.yaml  # Service metadata, deps, contacts
│           └── skills/                   # Service-specific skills
├── docs/
│   ├── prd/PRD.md
│   ├── design/DESIGN.md            # Architecture document
│   ├── design/FEATURE.md           # Feature tracking
│   └── planning/PLANNING.md        # Phase breakdown
├── .claude_local.yaml              # Project identity + local paths
├── CLAUDE.md                       # AI rules (core of the system)
├── README.md
├── LICENSE (MIT)
└── tests/
└── personal/                       # (gitignored) User's installed
    ├── context/
    └── skills/
└── setup/
    ├── install.sh                  # Main installer (~600 lines)
    └── update.sh                   # Keeps installed skills up to date
```

---

## 6. Eight-Stage Agentic Workflow

The core development pipeline — every feature flows through these stages:

```
PRD.md
  ↓ Stage 1: p2f (PRD → Features)
FEATURE.md [status: TBD]
  ↓ Stage 2: f2d (Features → Design)
DESIGN.md [architecture, API, data model]
  ↓ Stage 3: d2pl (Design → Plan)
plan_{feature_id}.md [tasks, waves, MAC]
  ↓ Stage 4: pl2c (Plan → Code, via subagents)
Code + Tests + Atomic Commits
  ↓ Stage 5: c2f (Code → Features, mark COMPLETE)
FEATURE.md [status: COMPLETE]
  ↓ Stage 6: c2d (Code → Design, sync back)
DESIGN.md [updated to match code]
  ↓ Stage 7: verify (MAC check in fresh session)
✅ Feature complete
  ↓ Stage 8: review-checkpoint (find reviewer, send message)
PR ready for human review
```

### Stage Details

#### Stage 1: PRD → Features (p2f)
- **Input:** PRD.md changes
- **Output:** FEATURE.md with new features marked "TBD"
- **Process:** Diff PRD vs FEATURE.md features → classify as new/changed/removed → add TBD entries

#### Stage 2: Features → Design (f2d)
- **Input:** FEATURE.md (TBD features)
- **Output:** DESIGN.md with architecture, API, data model, diagrams
- **Model:** Use strongest model (e.g., Opus) for design decisions

#### Stage 3: Design → Plan (d2pl)
- **Input:** DESIGN.md changes
- **Output:** `plan_{feature_id}.md` with tasks grouped into waves
- **Key concept — Waves:** Tasks in the same wave can run in parallel (no file conflicts). Sequential waves depend on prior waves.
- **Key concept — MAC (Minimum Acceptance Criteria):** Smallest checks to prove the feature works. Not comprehensive tests, just proof of delivery.

#### Stage 4: Plan → Code (pl2c) — Orchestrator + Subagent Model

```
Orchestrator session (spawns subagents)
  Wave 1 (parallel)
    ├── Subagent 1 → Task 1 → Commit → Destroyed
    └── Subagent 2 → Task 2 → Commit → Destroyed
  Wave 2 (sequential, depends on Wave 1)
    └── Subagent 3 → Task 3 → Commit → Destroyed
  Auto-trigger Verify (fresh session)
```

**Why one task = one subagent = one commit:**
1. Context isolation: no context bleeding between tasks
2. Atomic commits: easy to revert
3. Parallel execution: multiple subagents can run same wave
4. Clean state: subagent is destroyed after commit

#### Stage 5: Code → Features (c2f)
- Scan code for implemented features → mark as COMPLETE in FEATURE.md
- Detect untracked features (code not in FEATURE.md)

#### Stage 6: Code → Design (c2d)
- Sync code changes back to DESIGN.md (APIs, data model, architecture)
- Prevents docs from going stale

#### Stage 7: Verify (qp)
- Run MAC checks from plan file against code + tests
- Must run in a fresh session (check: no context contamination from coding session)
- Pass → ready for PR. Fail → root cause analysis → fix instructions

#### Stage 8: Review Checkpoint (auto-applied)
- Find the reviewer (check Slack activity, team.yaml)
- Draft review request message
- User confirms and sends

#### Quick Mode (bypass for small changes)
For changes <100 lines: skip PRD/Design/Plan → create single-task plan → execute in current session → verify → done.

---

## 7. Skill Catalog (41 Skills)

### 7.1 Team Common Skills (16 skills) — Shared by everyone

#### Documentation & Workflow (7 skills)

| Skill | Description |
|-------|-------------|
| `**setup-coworker**` | 5-step interactive setup: scan project → generate CLAUDE.md → detect identity → create local config → install git hooks |
| `**report-issue**` | Report coworker bugs to the coworker's own GitHub Issues |
| `**create-skill**` | Create new skill file with enforced frontmatter, duplicate detection, auto PR |
| `**edit-skill**` | Edit existing skill: update content, changelog validation, auto commit |
| `**merge-docs**` | Merge two markdown doc versions (e.g., after upstream merge conflicts) |
| `**doc-protection**` | Manage PROTECTED blocks in documents. AI must never modify content inside protected blocks |
| `**review-request**` | Auto-find the right reviewer (from team.yaml + Slack activity) and draft review request message |

#### MCP Integration Skills (9 skills)

| Skill | Integration | Description |
|-------|-------------|-------------|
| `**mcp-slack**` | Slack | Read/write messages. Channel registry with pre-configured team channels. Bot + User token support |
| `**mcp-jira**` | Jira | Create/search/comment on issues. Session-based auth |
| `**mcp-confluence**` | Confluence | Search/read wiki pages. Atlassian Cloud API |
| `**mcp-google-drive**` | Google Drive | Read/write Google Docs/Sheets/Slides. OAuth-based |
| `**mcp-splunk**` | Splunk | Query logs via REST API. Prod/non-prod support with service-specific query templates |
| `**mcp-playwright**` | Playwright | Browser automation for auth-protected pages. Uses browser session (no credentials needed) |
| `**mcp-coda**` | Coda | Read docs, pages, tables via REST API |
| `**mcp-identity-switcher**` | Auth | Generate auth headers for internal APIs |
| `**mcp-knowledge-repo-search**` | Knowledge repos | Auto-search external knowledge repos when local search fails |

### 7.2 Personal Skills (25 skills) — Per-person, customizable

#### Design Workflow (5 skills)

| Skill | Alias | Flow |
|-------|-------|------|
| `**design-p2f**` | p2f | PRD → Features. Propagate PRD changes to FEATURE.md |
| `**design-f2d**` | f2d | Features → Design. Create architecture, API, data model |
| `**design-d2pl**` | d2pl | Design → Plan. Break into tasks, waves, MAC |
| `**design-c2d**` | c2d | Code → Design. Sync code changes back to DESIGN.md |
| `**design-c2f**` | c2f | Code → Features. Mark implemented features as COMPLETE |

#### Feature Development (2 skills)

| Skill | Description |
|-------|-------------|
| `**plan-to-code**` | Execute plan tasks via orchestrator + subagent model. One task = one subagent = one commit |
| `**quick-task**` | Small change (<100 lines) without full PRD/Design/Plan pipeline. Bug fixes, config tweaks |

#### AI Self-Improvement (4 skills)

| Skill | Description |
|-------|-------------|
| `**self-healing-trace**` | Auto-log correction traces when user corrects AI behavior. Stores in YAML format |
| `**self-analyze**` | Analyze traces for patterns (2+ occurrences). Generate new skills from patterns |
| `**strain-sites**` | Train AI on specific patterns through self-iteration; independent analysis + human expert → extract failure patterns → update skill |
| `**auto-patches**` | Auto-correct English grammar errors for non-native speakers. Minor in italics |

#### Issue Management (3 skills)

| Skill | Description |
|-------|-------------|
| `**issue-create**` | Doc-driven change request via GitHub Issue. 6-step structured discussion → approval → execute |
| `**issue-debug**` | Scientific debugging: hypothesis → test → confirm → fix. Best with strongest model |
| `**issue-investigate**` | Deep investigation of tickets/Slack threads/on-call issues. Follows every lead autonomously |

#### Pre-Commit Quality Gates (6 skills, all auto-applied)

| Skill | Description |
|-------|-------------|
| `**guardrails**` | Prohibited operations (git, secrets, infrastructure, documents). AI must check and refuse |
| `**code-review**` | Review against known anti-patterns. Self-improving: new patterns added via self-healing |
| `**code-conventions**` | Team code style enforcement (language-specific formatters, naming, structure) |
| `**review-checkpoint**` | After each phase, prompt user to confirm with the right reviewer |
| `**unit-tests**` | 3-level verification: structural/frontmatter → content quality → dry-run |
| `**verify-plan**` | Post-execution MAC verification in a fresh session |

#### Project-Specific Skills (variable count)

These are team-specific. Examples:
- VOC (Voice of Customer) feedback analysis from Slack
- Service-specific knowledge base installation
- On-call summary generation

---

## 8. MCP Integrations (9 Tools)

### 8.1 Slack MCP

| Field | Value |
|-------|-------|
| **Purpose** | Read/write Slack messages, search, channel management |
| **Server** | Custom MCP server (slack_server.py) |
| **Install** | `git clone` + Python venv + pip install |
| **Env vars** | `SLACK_TOKEN` (xoxp-), `SLACK_USER_TOKEN` (xoxp-) |
| **Key features** | Pre-configured channel IDs for team channels. Token sends as the person, bot token sends as the app |
| **Bot scopes** | app_mentions:read, channels:history, channels:read, channels:write, chat:write, files:read, groups:history, groups:read, im:history, im:read, im:write, reactions:read, reactions:write, team:read, users:read, usergroups:read, users.profile:read |
| **User scopes** | channels:history, channels:read, channels:write, chat:write, files:read, groups:history, groups:read, im:history, im:read, im:write, search:read, search:read:private, search:read:public, team:read, users:read |

### 8.2 Jira MCP

| Field | Value |
|-------|-------|
| **Purpose** | Create/search/comment on Jira issues |
| **Server** | Via developer desktop app or direct Atlassian API |
| **Install** | Developer desktop app + SSO auth, or `mcp-atlassian` |
| **Auth** | Session-based (re-auth each session) or API token |
| **Key features** | Issue creation with structured fields, search with JQL |

### 8.3 Confluence MCP

| Field | Value |
|-------|-------|
| **Purpose** | Search/read wiki pages |
| **Server** | `mcp-atlassian` (uvx) |
| **Install** | `uvx mcp-atlassian` |
| **Env vars** | `CONFLUENCE_EMAIL`, `CONFLUENCE_API_TOKEN`, `CONFLUENCE_CLOUD_ID` |
| **Key features** | Full-text search across wiki, read page content |

### 8.4 Google Drive MCP

| Field | Value |
|-------|-------|
| **Purpose** | Read/write Google Docs, Sheets, Slides |
| **Server** | Custom MCP server (intuit-google-drive-mcp or similar) |
| **Install** | `git clone` + Python venv |
| **Auth** | No API key needed, uses browser flow |
| **Key features** | Create/edit documents, read spreadsheets, search files |

### 8.5 Splunk Integration

| Field | Value |
|-------|-------|
| **Purpose** | Query application logs (prod and non-prod) |
| **Server** | Python REST client (not a full MCP, uses Splunk REST API) |
| **Install** | Python script with requests library |
| **Env vars** | `SPLUNK_USERNAME`, `SPLUNK_PASSWORD` |
| **Key features** | Pre-configured query templates per service. Downloads results to `/tmp/splunk/` for analysis by subagent |

### 8.6 Playwright MCP

| Field | Value |
|-------|-------|
| **Purpose** | Browser automation for auth-protected pages |
| **Server** | `@playwright/mcp` (npm `@microsoft/mcp-playwright`) |
| **Install** | `npm i @microsoft/mcp-playwright` |
| **Auth** | Uses existing browser session (no credentials needed) |
| **Key features** | Access internal dashboards, CSR tools, MCP marketplace |

### 8.7 Coda Integration

| Field | Value |
|-------|-------|
| **Purpose** | Read Coda docs, pages, tables |
| **Server** | Pure REST API (no MCP needed) |
| **Env vars** | `CODA_API_TOKEN` |
| **Key features** | Read structured data from Coda tables |

### 8.8 Auth/Identity MCP

| Field | Value |
|-------|-------|
| **Purpose** | Generate auth headers for internal APIs |
| **Server** | Custom identity-switcher-mcp or marketplace plugin |
| **Key features** | Switch between different auth contexts (e.g., different user types, environments) |

### 8.9 Knowledge Repo Search

| Field | Value |
|-------|-------|
| **Purpose** | Auto-search external knowledge repos when local search fails |
| **Server** | Configuration-based (reads from `.local_config.yaml` deps) |
| **Key features** | Resolves local path from config, falls back to git clone. Auto-applied — no user trigger |

---

## 9. Guardrails & Safety Rules

All auto-applied. AI must check and refuse violations.

### 9.1 Git & Code (G1–G4)
- **G1:** Never push to main/master → all changes through PR
- **G2:** Never force push → destroys history
- **G3:** Never delete remote branches without confirmation
- **G4:** Never merge PRs without human approval

### 9.2 Secrets & Security (S1–S4)
- **S1:** Never hardcode credentials → use `.env` + variable names
- **S2:** Never write tokens into committed files → env vars only
- **S3:** Never log/print secrets
- **S4:** Never send tokens in Slack/PR → use variable names

### 9.3 Infrastructure & Data (I1–I4)
- **I1:** Never modify production config → manual approval + change management
- **I2:** Never run DB migrations without confirmation
- **I3:** Never delete files without confirmation
- **I4:** Never install system dependencies without confirmation

### 9.4 Documents & Workflow (D1–D7)
- **D1:** Never modify PROTECTED blocks
- **D2:** Never fabricate information → ask user
- **D3:** Never skip review checkpoints
- **D4:** Never create pure-AI PRs → all must be co-created (AI + human)
- **D5:** Never modify `personal/` in upstream PRs
- **D6:** Never create skill files without "create-skill" workflow
- **D7:** Never commit skill changes without "edit-skill" workflow

### 9.5 PROTECTED Blocks

Format:
```html
<!-- PROTECTED -->
Content that AI must never modify
<!-- END PROTECTED -->
```

AI **MUST NOT** modify, move, remove, or reformat content between markers.
AI **CAN** read protected content for context and suggest adding protection to critical sections.

---

## 10. Self-Healing System

A feedback loop where AI learns from its mistakes:

```
User corrects AI
      ↓
self-healing-trace: logs correction to ~/.claude/self-healing/traces/ (YAML)
      ↓
self-healing-analyze: finds patterns (2+ occurrences of same mistake)
      ↓
Generates new skill or updates existing skill
      ↓
PR to upstream → team reviews → merge
      ↓
Everyone's AI stops making that mistake
```

### Trace Format (YAML)
```yaml
trigger: 2026-03-28T10:30:00Z
trigger: user_correction
context: "User said 'no, don't use FQN' after AI wrote java.util.Map"
correction: "Use imports, not fully qualified package names"
category: code-conventions
frequency: 1
```

### Pattern Detection
- Minimum 2 occurrences to be considered a pattern
- Patterns grouped by category (code-conventions, workflow, communication)
- Each pattern generates a rule that can be added to existing skills

### Hook-Based Detection
A `UserPromptSubmit` hook runs on every user message to detect correction signals:
- "no", "don't", "stop", "wrong", "not like that"
- Automatically triggers trace logging

---

## 11. Installer Specification

### install.sh (~600 lines)

**Arguments:**
- `--global` — install to `~/.claude/commands/` (available in all projects)
- `--project /path` — install to `{project}/.claude/commands/`
- (none) — interactive mode, asks user

**Steps:**
1. **Parse arguments** (global vs project vs interactive)
2. **Select role(s)** — prompt: "What's your role? (backend/frontend/architect/pm)" → multi-select
3. **Detect IDEs** — check for Claude Code, Cursor, Windsurf in environment
4. **Install skills to IDE directories:**
   - Team Common: `templates/team-common/skills/*.md` → target commands dir
   - Personal: `templates/personal/skills/*.md` → target commands dir
   - Project-specific: `templates/projects/{svc}/*.md` → target commands dir
5. **Copy personal templates** → `templates/personal/` → `personal/` (gitignored)
6. **Save global configs** → `~/.config/{team}-coworker/config.yaml` with install choices
7. **Create project-level configs** (if project mode):
   - `.local_config.yaml` — identity, doc paths, dependency paths
   - `.mcp.json` — MCP server definitions
8. **Sync IDE configs:**
   - `.cursorrules` → symlink to CLAUDE.md
   - `.windsurfrules` → symlink to CLAUDE.md
9. **Update .gitignore** → add `.local_config.yaml`, `.env`, `personal/`

**Output:**
```
Created: N files
Updated: N files
Skipped: N unchanged
```

### update.sh
- Auto-detects install mode (global vs project) from saved config
- Runs `git fetch upstream` + `git merge upstream/main`
- Re-runs install to same location
- Startup auto-check: every new IDE window, AI checks for upstream updates

### uninstall.sh
- Removes skills from `~/.claude/commands/` or `{project}/.claude/commands/`
- Does not touch personal config or `.local_config.yaml`

---

## 12. Setup Questionnaire Flow

Interactive chat-based setup (alternative to install.sh):

### Step 1: Identity Detection
```
→ Run whoami → get system username
→ Get project name from current folder
→ "Detected identity: {user} working on {project}. Correct?"
```

### Step 2: Prerequisites Check
```
→ "Do you have the coworker repo cloned locally?"
→ If no: guide through fork + clone + upstream remote
→ If yes: validate path exists
```

### Step 3: Role Selection
```
→ "What's your role? (backend/frontend/architect/pm — multi-select)"
→ Copy team-common + role skills to IDE config directory
```

### Step 4: IDE Detection
```
→ Auto-detect from environment
→ If not found: "Which IDE? (Claude Code/Cursor/Windsurf)"
→ Install skills to appropriate location
```

### Step 5: MCP Tool Setup
```
→ For each integration (Slack, Jira, Wiki, Logs, etc.):
  → Check if already installed
  → If not: "Install {tool}? (y/n)"
  → Auto-install if possible
  → Prompt for env vars (tokens) if needed
```

### Step 6: Verify
```
→ Check: team rules loaded ✓
→ Check: role skills loaded ✓
→ Check: .local_config.yaml exists ✓
→ Check: MCP tools connected ✓
→ "Setup complete!"
```

---

## 13. Example Configurations

### team.yaml (team member registry)
```yaml
team:
  name: "{Team Name}"
  size: 25

members:
  - username: jsmith
    name: John Smith
    role: [backend, architect]
    services: [user-service, auth-service]
    slack_id: U0ABC123
    email: jsmith@company.com

  - username: jdoe
    name: Jane Doe
    role: [frontend]
    services: [web-app, mobile-app]
    slack_id: U0DEF456
    email: jdoe@company.com

  # ... all team members
```

### projects.yaml (project index)
```yaml
projects:
  - name: user-service
    type: backend
    language: Java
    framework: Spring Boot
    repo: github@github.com:team/user-service.git
    slack_channel: "#user-service-dev"
    contacts:
      primary: jsmith
      secondary: jdoe

  - name: web-app
    type: frontend
    language: TypeScript
    framework: React
    repo: git@github.com:team/web-app.git
    slack_channel: "#web-app-dev"
    contacts:
      primary: jdoe
```

### .local_config.yaml (per-project identity)
```yaml
identity:
  username: jsmith
  project: user-service

docs:
  prd: docs/prd/PRD.md
  design:
    - docs/design/DESIGN.md
  feature: docs/design/FEATURE.md
  planning: docs/planning/PLANNING.md

deps:
  auth-service: ~/project/auth-service
  shared-lib: ~/project/shared-lib
```

### CLAUDE.md (core AI rules — example structure)
```markdown
# {Team Name} AI Coworker Rules

## Identity
- Read .local_config.yaml for username, project, doc paths
- Use team.yaml for team member lookup

## Workflow
- Follow 8-stage pipeline for features (p2f → f2d → d2pl → pl2c → c2f → c2d → verify → review)
- Use quick-task for changes <100 lines
- All code changes require an approved issue

## Guardrails
- [All G1-G4, S1-S4, I1-I4, D1-D7 rules]

## MCP Usage
- Slack: use channel registry for correct channel
- Jira: re-auth each session
- Logs: use service-specific query templates

## Git Conventions
- Branch: conventional naming
- Commit: conventional commits
- PR: Every human co-created, include issue reference

## Doc-Driven Development
- Detect bug signals → ask to create issue first
- Never skip discussion step
- Every code change has a corresponding issue
```

### Slack Channel Registry (example)
```yaml
channels:
  team_general:
    id: C09NUGJFRF1
    name: "#team-general"
    purpose: Team-wide announcements

  backend_dev:
    id: C0BACKEND1
    name: "#backend-dev"
    purpose: Backend discussions, code reviews

  oncall:
    id: C00NCALL1
    name: "#oncall-alerts"
    purpose: Incident response
```

---

## 14. Design Decisions & Rationale

### Why a custom system instead of existing frameworks?

| Factor | Custom Coworker | Generic Frameworks |
|--------|----------------|--------------------|
| Team-specific rules | Built-in (team.yaml, project.yaml) | Needs extensive customization |
| Fork-based sharing | First-class citizen | Not supported |
| Bidirectional doc-code sync | 8-stage pipeline | Typically one-way |
| Self-healing | Built-in trace + pattern → skill loop | Not available |
| Multi-IDE | Claude Code + Cursor + Windsurf | Usually single IDE |
| Scalable | 25 people can each customize without conflicts | — |

### Why fork model instead of shared branch?
- **Autonomy:** Each person's `personal/` is private
- **Safety:** No risk of personal config overwriting others
- **Contribution:** Good patterns flow upstream through reviewed PRs
- **Scalable:** 25 people can each customize without conflicts

### Why subagent model for code execution?
- **Context isolation:** No bleeding between tasks
- **Atomic execution:** Multiple tasks in same wave
- **Parallel execution:** Destroyed after commit, no lingering context
- **Clean state:** Destroyed after commit, no lingering context

### Why MAC instead of comprehensive tests?
MAC = "smallest checks to prove the feature works." Keeps verification focused on delivery, not side effects. Comprehensive testing is a separate concern.

### Why PROTECTED blocks?
Some content is human judgment (PRD requirements, architecture decisions, business rules). AI should never rewrite these — they represent decisions made by people with context AI doesn't have.

### Why bidirectional doc-code sync?
Without it, docs rot within days. Code → Features (c2f) and Code → Design (c2d) ensure docs always reflect reality.

---

## 15. Getting Started: How to Build Your Own

### Prerequisites
Before starting, you need:
1. A Git repository for the coworker system
2. A list of team members (name, role, services, Slack ID)
3. A list of team projects (name, language, framework, repo URL)
4. Claude Code, Cursor, or Windsurf installed

### Step-by-Step

**Phase 1: Bootstrap**
1. Create a new Git repo: `{your-team}-coworker`
2. Create the directory structure from [Section 5](#5-directory-structure)
3. Fill in `team.yaml` and `projects.yaml` with your team's info
4. Write your `CLAUDE.md` based on [Section 13 example](#claudemd-core-ai-rules--example-structure)

**Phase 2: Core Skills**
1. Create team-common skills (guardrail, code-review, code-conventions, review-checkpoint)
2. Create the 5 design workflow skills (p2f, f2d, d2pl, c2d, c2f)
3. Create the 2 execution skills (plan-to-code, quick-task)
4. Create the issue management skills (create, debug, investigate)
5. Create the 6 pre-commit quality skills

**Phase 3: Integrations**
1. Set up Slack MCP (most impactful — team communication)
2. Set up Jira/issue tracker MCP
3. Set up wiki/docs MCP (Confluence, Notion, etc.)
4. Set up log search (Splunk, Datadog, etc.)
5. Optional: Google Drive, browser automation, auth

**Phase 4: Installer**
1. Write `install.sh` following [Section 11](#11-installer-specification)
2. Write `update.sh` and `uninstall.sh`
3. Test on a team member's machine

**Phase 5: Self-Healing**
1. Add self-healing-trace skill (logs corrections)
2. Add self-healing-analyze skill (finds patterns)
3. Add UserPromptSubmit hook for auto-detection
4. Create PR workflow for sharing learned patterns

**Phase 6: Rollout**
1. Each team member forks the repo
2. Runs `install.sh`
3. Runs interactive setup in their IDE
4. Starts using the 8-stage workflow

### Questions to Ask the New Team

Before building, gather this info:

1. **Team structure:** How many people? What roles (backend, frontend, ML, etc.)?
2. **Projects:** What services/repos does the team own? What languages/frameworks?
3. **Tools:** What issue tracker? What wiki? What logging system? What CI/CD?
4. **Communication:** What Slack channels? What's the review process?
5. **Code style:** What formatters/linters? What commit conventions?
6. **Pain points:** What mistakes does AI keep making? What context does it always lack?
7. **Auth:** How do internal APIs authenticate? What tokens/credentials are needed?
8. **Environments:** What environments exist (dev, QA, staging, prod)? How to access?

---

## Summary

This coworker system transforms AI from a simple code assistant into a full team member that:

- **Knows the team** — who does what, who to ask, which channel to post in
- **Follows the rules** — guardrails, code conventions, review checkpoints
- **Drives the workflow** — 8-stage pipeline from PRD to verified PR
- **Learns from mistakes** — self-healing loop turns corrections into team knowledge
- **Stays in sync** — bidirectional doc-code sync prevents knowledge rot
- **Scales** — fork model lets 25+ people customize without conflicts

**Total: 41 skills, 9 MCP integrations, 4-layer architecture, 8-stage workflow, self-healing feedback loop.**
