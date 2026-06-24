# AI Coworker Rules

## Identity
- Read `.local_config.yaml` for username, project name, and doc paths
- Use `personal/context/projects.yaml` for project metadata catalog

## Core Philosophy
- **Human decides, AI executes.** When uncertain, ask — never assume.
- **Rapid execution.** Once human confirms, move fast.
- **Self-healing.** Log every correction. Patterns become rules.

## Guardrails — OWASP & Standard Security

### Git & Code
- Never push to main/master — all changes through PR
- Never force push
- Never delete remote branches without confirmation
- Never merge PRs without human approval
- Branch naming: `{type}/{issue-id}-{short-description}` (e.g., `feat/123-add-login`)
- Commits: Conventional Commits format (`feat:`, `fix:`, `chore:`, etc.)

### Security (OWASP Top 10)
- **A01 Broken Access Control** — Never bypass auth checks; always validate permissions server-side
- **A02 Cryptographic Failures** — Never hardcode secrets; use env vars. Never log sensitive data.
- **A03 Injection** — Always use parameterized queries; never interpolate user input into SQL/shell/HTML
- **A04 Insecure Design** — Validate inputs at system boundaries; distrust all external data
- **A05 Security Misconfiguration** — Never commit `.env` files; never expose stack traces in responses
- **A06 Vulnerable Components** — Flag use of outdated dependencies when spotted
- **A07 Auth Failures** — Never hardcode credentials; tokens in env vars only; never send tokens in messages
- **A08 Software Integrity** — Never skip review on dependency changes
- **A09 Logging Failures** — Never log passwords, tokens, or PII
- **A10 SSRF** — Never make server-side requests to user-provided URLs without validation

### Infrastructure & Data
- Never modify production config without confirmation
- Never run DB migrations without confirmation
- Never delete files without confirmation
- Never install system-level dependencies without confirmation

### Documents & Workflow
- Never modify PROTECTED blocks (between `<!-- PROTECTED -->` and `<!-- END PROTECTED -->`)
- Never fabricate information — ask user when uncertain
- Never skip review checkpoints
- Never create pure-AI PRs — all PRs must be human co-created
- Never create skill files without the `skill-create` workflow (in skill-factory)
- Never commit skill changes without the `skill-edit` workflow (in skill-factory)

## MCP Usage
- **GitHub**: use for issues, PRs, comments. Re-auth if session expired.
- **Slack**: use channel registry in team.yaml for correct channel IDs
- **Telegram**: use for direct notifications to cicidi
- **Discord**: use for community/team channel messages
- **Google Drive**: re-auth via browser flow each session if needed

## Git Conventions
- Branch: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`
- Commit: Conventional Commits (enforced by pre-commit hook)
- PR: every PR must reference a GitHub Issue number

## Issue-Driven Development
- Detect bug signals → create GitHub Issue first, then fix
- Every code change should have a corresponding issue or PR description
- All design discussion happens in the conversation, not in documents

## Self-Healing
- On every user correction, log a trace via `self-heal`
- Run `self-analyze` periodically to find patterns
- Generated skills go through PR review before merging

## Code Quality
- Run linting and formatting before every commit
- Tests required for all new functions/classes
- No commented-out code in PRs
- No `TODO` comments without a linked issue
