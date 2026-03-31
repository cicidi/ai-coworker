---
name: edit-skill
description: Edit an existing skill — update content, bump version, validate changelog, auto-commit
aliases: [update-skill]
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
