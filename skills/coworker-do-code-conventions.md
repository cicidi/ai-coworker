---
name: coworker-do-code-conventions
triggers:
  - check code conventions
  - enforce code style
  - run formatter
  - style check before commit
description: |
  Enforces team code style — runs language-specific formatters, checks naming
  conventions, and validates commit message format before every commit.
  Trigger whenever code is about to be committed or reviewed for style.
services:
  category: coworker-do
when_to_use: |
  Before committing code. When user asks to "check style", "run formatter",
  or "enforce conventions". Auto-applied pre-commit.
when_not_to_use: |
  Do not apply to generated files, vendor code, or auto-formatted migrations.
version: 1.0.0
---

# Code Conventions (Auto-Applied)

Enforces code style and commit message format before every commit.

## Commit Message (Conventional Commits)

Format: `type(scope): description`

Valid types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `style`, `perf`, `ci`, `build`

Rules:
- Subject line max 72 characters
- Imperative mood: "Add feature" not "Added feature"
- No period at end of subject line
- Reference issue: `(closes #123)` or `(refs #123)`
- Body optional — use for "why", not "what"

Examples:
```
feat(auth): add JWT refresh token rotation (closes #42)
fix(api): return 404 when resource not found (refs #55)
chore: update dependencies to latest patch versions
```

## Branch Naming
`{type}/{issue-id}-{kebab-description}`
Examples: `feat/42-add-refresh-tokens`, `fix/55-404-on-missing-resource`

## Naming Conventions (auto-detect language)

**Python**
- `snake_case` for functions, variables, modules
- `PascalCase` for classes
- `SCREAMING_SNAKE_CASE` for constants
- Private: `_prefixed`

**TypeScript/JavaScript**
- `camelCase` for functions, variables
- `PascalCase` for classes, React components, types
- `SCREAMING_SNAKE_CASE` for constants
- Files: `kebab-case.ts`

**Java**
- `camelCase` for methods, variables
- `PascalCase` for classes, interfaces
- `SCREAMING_SNAKE_CASE` for constants
- Packages: `lowercase.dotted`

**Go**
- `camelCase` for unexported, `PascalCase` for exported
- Short names for receivers: `u` for `User`, not `user`
- Files: `snake_case.go`

## Formatting
Always run formatter before commit:
- Python: `black` or `ruff format`
- TypeScript: `prettier`
- Java: `google-java-format` or project's checkstyle
- Go: `gofmt`
- Rust: `rustfmt`

## On Violation
Flag violations before commit. Formatting issues: auto-fix. Naming violations: suggest fix, ask to confirm.
