---
name: meta-import-skill
description: Import a skill from any source (GitHub URL, git repo, local file), check its license, convert it to the AI coworker format, and auto-install.
aliases: [import-skill, install-skill-from, add-skill-from]
---

# Import Skill

Fetches an external skill from GitHub, a raw URL, or a local file — checks the license, converts the frontmatter to the AI coworker format, preserves original content verbatim, and installs it.

## Process

### 1. Resolve Source

```
→ GitHub repo URL (e.g., github.com/user/repo or github.com/user/repo/tree/main/skills/foo)
     → fetch SKILL.md via raw.githubusercontent.com
     → also fetch LICENSE and any root-level copyright file
→ Raw URL (e.g., raw.githubusercontent.com/.../SKILL.md)
     → fetch directly
→ Local file path (e.g., ~/Downloads/skill.md or skill.zip / .skill package)
     → read directly; unzip if archive
```

For GitHub repos without a direct file path, search in order:
1. `SKILL.md` at repo root
2. `skills/*/SKILL.md`
3. Any `.md` with YAML frontmatter containing `name` and `description`

### 2. License Check

**Do this before writing any file.** Detect the license from:
- `LICENSE`, `LICENSE.md`, `LICENSE.txt`, `COPYING` at source root
- `license:` field in SKILL.md frontmatter
- Copyright header comments inside the skill file

**Decision table:**

| License | Action |
|---|---|
| MIT, Apache 2.0, BSD-2, BSD-3, ISC, Unlicense, CC0, CC-BY | ✅ Proceed — add attribution block |
| GPL, LGPL, AGPL, EUPL | ⚠️ Warn: copyleft — modifications must be shared under same license. Ask user to confirm before continuing. |
| CC-BY-SA | ⚠️ Warn: derivative works must use same license. Ask user to confirm. |
| CC-BY-NC | ⚠️ Warn: non-commercial use only. Ask user to confirm. |
| No license found | ⚠️ No license = all rights reserved by default. Ask: "Do you have explicit permission from the author?" Do not install without confirmation. |
| Proprietary / "all rights reserved" | ❌ Refuse. Do not install without written permission from the author. Tell the user why. |

If the user declines or cannot confirm permission: stop here.

### 3. Extract Original Content

From the source file, collect:
- All frontmatter fields
- Full body (everything after the frontmatter `---` block)
- Author name (from frontmatter, git blame, or file header)
- Copyright notice (exact text)
- Referenced files if available (scripts/, references/, assets/)

**Do not rewrite or summarize the body.** Keep it character-for-character.

### 4. Convert Frontmatter

Map to the AI coworker format. Show the user the result before writing:

```yaml
---
name: {kebab-case — use original if valid; propose alternative and ask if it conflicts with an existing skill}
description: {original description — verbatim}
aliases: [{2–3 natural trigger phrases derived from name + description}]
imported_from: {source URL or absolute file path}
original_author: {author name, or "unknown"}
original_license: {SPDX license identifier, e.g., MIT}
version: 1.0.0
updated: {today's date YYYY-MM-DD}
---
```

Prepend an attribution block immediately after the frontmatter closing `---`:

```markdown
<!--
  Imported from: {source URL}
  Original author: {author}
  License: {license name}
  Copyright: {copyright notice if found, else "see source"}
  Imported on: {date}
  Original content preserved. Frontmatter reformatted only.
-->
```

Then append the original body unchanged.

### 5. Confirm with User

Before writing any file, display:
- Proposed skill name
- License + any obligations
- The full converted frontmatter block
- Where it will be installed

Ask: "Install as `{name}` under `{layer}`? (y/n)"

### 6. Duplicate Check

```
→ Search templates/ for same name
→ Search descriptions for >80% similarity
→ If conflict: "Similar skill exists: {existing-name}. Overwrite, rename, or cancel? (o/r/c)"
```

### 7. Determine Install Layer

Default: **personal**. Ask if unclear.
- `personal` → `~/project/ai-coworker/templates/personal/skills/{name}.md`
- `team-common` → `~/project/ai-coworker/templates/team-common/skills/{name}.md`

### 8. Write, Commit, and Install

```bash
# Write converted skill
cat > ~/project/ai-coworker/templates/{layer}/skills/{name}.md << 'EOF'
{converted content}
EOF

# Commit with license info in message
cd ~/project/ai-coworker
git add templates/{layer}/skills/{name}.md
git commit -m "feat: import skill {name} [{license}] from {source}"
git push origin main

# Install to all IDE targets
bash setup/update.sh
```

### 9. Confirm and Remind

Tell the user:
- ✅ Skill `{name}` installed and available as `/{name}` in Claude Code
- File: `templates/{layer}/skills/{name}.md`
- Attribution preserved in file header

Print the applicable post-install obligation:

| License | Obligation |
|---|---|
| MIT / Apache / BSD / ISC | Attribution required in the file. No further action needed. |
| Apache 2.0 | Include original NOTICE file content if one existed. |
| GPL / LGPL / AGPL | Any modifications you distribute must be released under the same license. |
| CC-BY | Credit the original author whenever you share or publish work using this skill. |
| CC-BY-SA | Derivative works must carry the same CC-BY-SA license. |
| CC-BY-NC | Non-commercial use only. Do not use in paid products or services. |

## Notes

- Never strip or alter the attribution comment block after install.
- If the source is a multi-skill repo, import one skill at a time and run this process for each.
- If the imported skill references bundled files (scripts/, assets/), copy them to the same skill directory and note the paths in the attribution block.
