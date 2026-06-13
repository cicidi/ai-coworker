---
name: coworker-meta-create-skill
triggers:
  - create a new skill
  - new skill
  - add skill
  - build a skill
description: |
  Create a new skill file with enforced frontmatter, duplicate detection, and
  auto PR. Use when adding a new capability to the AI coworker system.
services:
  category: coworker-meta
when_to_use: |
  When user asks to create a new skill, add a new capability, or says "new skill".
  Always check for duplicates before creating.
when_not_to_use: |
  If a similar skill already exists, use coworker-meta-edit-skill instead.
version: 1.1.0
updated: 2026-05-06
---

# Create Skill

Creates a new skill file following the standard format, with duplicate detection, auto commit & push to skill factory, then pulls and installs from remote.

## Process

### 1. Gather Info
Ask user:
- Skill name (kebab-case, e.g., `design-p2f`)
- Category: `design` | `dev-feat` | `dev-ai-tool` | `issue` | `commit` | `mcp` | `doc`
- Description (one line, used in frontmatter)
- Target layer: `team-common` or `personal`
- Aliases (optional)

### 2. Duplicate Check
```
→ Search templates/ for similar skill names
→ Search for similar descriptions
→ If duplicate found: "Similar skill exists: {name}. Edit that instead? (y/n)"
```

### 3. Create File in Skill Factory
Location: `~/project/ai-coworker/skills/{name}.md`

Required frontmatter:
```yaml
---
name: {name}
triggers:
  - {trigger phrase 1}
  - {trigger phrase 2}
description: |
  {one-line description}
services:
  category: {category}
when_to_use: |
  {when to use this skill}
when_not_to_use: |
  {when NOT to use this skill}
version: 1.0.0
---
```

### 4. Commit and Push to Remote
```bash
cd ~/project/ai-coworker
git add templates/{layer}/skills/{name}.md
git commit -m "feat: add skill {name} — {one-line description}"
git push origin main
```

### 5. Pull and Install from Remote
```bash
cd ~/project/ai-coworker
bash setup/update.sh
```

This pulls the latest from remote and re-runs `install.sh`, which syncs the new skill to all configured IDE locations (Claude Code, Cursor, OpenCode, Gemini).

### 6. Confirm
Tell the user:
- Skill file created at `templates/{layer}/skills/{name}.md`
- Pushed to `origin/main`
- Installed via `update.sh`
- Available immediately in Claude Code as `/{name}`
