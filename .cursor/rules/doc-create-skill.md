---
name: create-skill
description: Create a new skill file with enforced frontmatter, duplicate detection, and auto PR
aliases: [new-skill]
---

# Create Skill

Creates a new skill file following the standard format, with duplicate detection and automatic PR creation.

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

### 3. Create File
Location: `templates/{layer}/skills/{name}.md`

Required frontmatter:
```yaml
---
name: {skill-name}
description: {one-line description}
aliases: [{alias1}, {alias2}]
version: 1.0.0
created: {date}
---
```

### 4. Install to IDEs
After creation, install to:
- `.claude/commands/{name}.md`
- `.cursor/rules/{name}.md`
- `.opencode/instructions/{name}.md`
- `.gemini/{name}.md`

### 5. Create PR
```
→ git checkout -b skill/add-{name}
→ git add templates/{layer}/skills/{name}.md
→ git commit -m "skill: add {name}"
→ Create GitHub PR with description of what the skill does
```
