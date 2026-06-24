---
name: coworker-gate-guardrails
triggers:
  - security check
  - owasp check
  - check for vulnerabilities
  - run guardrails
description: |
  Auto-applied pre-commit guardrails based on OWASP Top 10 and standard security
  practices. Triggers before every commit to catch injection, secrets, auth issues.
services:
  category: coworker-do
when_to_use: |
  Before every commit. When user asks for security review or mentions OWASP.
  Auto-applies to all code changes.
when_not_to_use: |
  false
version: 1.0.0
---

# Guardrails (Auto-Applied)

Runs automatically before every commit and PR creation. AI must check and refuse violations.

## OWASP Top 10 Checks

### A01 — Broken Access Control
- [ ] No authorization logic bypassed (no `if (false)` guarding auth)
- [ ] All new endpoints have auth middleware applied
- [ ] No direct object references without ownership check

### A02 — Cryptographic Failures
- [ ] No plaintext secrets in code or config files
- [ ] No hardcoded API keys, tokens, passwords
- [ ] No sensitive data logged
- [ ] Passwords hashed (bcrypt/argon2), never stored plain

### A03 — Injection
- [ ] All SQL uses parameterized queries / ORM — no string concatenation
- [ ] All shell commands use argument arrays — no string interpolation with user data
- [ ] All HTML output is escaped — no raw user content in HTML
- [ ] No `eval()` with user input

### A04 — Insecure Design
- [ ] All user inputs validated at system boundaries
- [ ] No trust of user-provided data without validation
- [ ] Error messages don't expose stack traces or internal paths

### A05 — Security Misconfiguration
- [ ] No `.env` files committed
- [ ] No debug mode enabled in production configs
- [ ] No default credentials left in config

### A06 — Vulnerable Components
- [ ] New dependencies flagged for review
- [ ] No known-vulnerable packages (check `npm audit` / `pip audit`)

### A07 — Authentication Failures
- [ ] Tokens only in env vars — never in code
- [ ] No tokens in log statements
- [ ] Session management follows framework best practices

### A08 — Software Integrity
- [ ] No dependency changes without review
- [ ] Lock files committed alongside dependency updates

### A09 — Logging Failures
- [ ] No passwords, tokens, or PII in log statements
- [ ] Errors logged but sensitive data redacted

### A10 — SSRF
- [ ] No server-side requests to user-provided URLs without allowlist

## Git-Specific Checks
- [ ] Not pushing to main/master directly
- [ ] Branch name follows convention: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`
- [ ] No force push flags in command

## On Violation
```
→ Block the action
→ Explain: "Blocked: {rule} — {OWASP category}"
→ Suggest fix
→ Do NOT proceed until human confirms resolution
```
