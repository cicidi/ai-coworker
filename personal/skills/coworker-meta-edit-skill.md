---
name: coworker-meta-edit-skill
triggers:
  - edit skill
  - update skill
  - improve skill
  - modify skill content
description: |
  Edit an existing skill — update content, bump version, validate changelog,
  auto-commit. Use when improving or fixing an existing skill file.
services:
  category: coworker-meta
when_to_use: |
  When user asks to edit, update, or improve an existing skill. Always bump
  version and update changelog entry.
when_not_to_use: |
  If the skill does not exist yet, use coworker-meta-create-skill instead.
version: 1.0.0
---

# Edit Skill

Safely edit an existing skill file with version tracking and auto-commit.

## Process

### 1. Find Skill
```
→ List all skills in templates/
→ Ask: "Which skill do you want to edit?"
→ Read current content and display it
```

### 2. Make Changes
- Edit the skill content as directed by user
- Preserve all frontmatter fields
- Update `version` (bump patch: 1.0.0 → 1.0.1, minor changes: 1.0.0 → 1.1.0)
- Add `updated: {date}` to frontmatter

### 3. Validate
- Frontmatter is valid YAML
- `name` field matches filename
- `description` is present and non-empty
- No broken markdown headings

### 4. Sync to IDEs
Copy updated file to all IDE locations:
- `.claude/commands/{name}.md`
- `.cursor/rules/{name}.md`
- `.opencode/instructions/{name}.md`
- `.gemini/{name}.md`

### 5. Commit
```
git add templates/.../skills/{name}.md {ide-paths}
git commit -m "skill: update {name} — {one-line summary of change}"
```

Do NOT create a PR automatically — let user decide whether to push.
