---
name: commit
description: "Create a git commit following conventional commits format. Use when user asks to commit, save changes, or create a checkpoint."
user-invocable: true
---

# Smart Git Commit

## When to use
When the user asks to commit changes, "save progress", or "checkpoint".

## Steps

1. Run `git status` to see what's changed
2. Run `git diff --staged` and `git diff` to understand the changes
3. Categorize the change:
   - `feat:` new feature
   - `fix:` bug fix
   - `refactor:` code restructure, no behavior change
   - `docs:` documentation only
   - `test:` tests only
   - `chore:` build, config, dependencies

4. Write a commit message:
   - First line: `type: short summary` (max 72 chars, lowercase, no period)
   - Body (optional): explain *why*, not *what*

5. Stage relevant files and commit:
   ```
   git add <specific files>
   git commit -m "type: summary"
   ```

6. Never use `git add .` blindly — check for secrets or unintended files first.
7. Never skip hooks (`--no-verify`).
