---
name: design-p2f
description: PRD → Features. Propagate PRD changes to FEATURE.md, classify new/changed/removed features
aliases: [p2f]
---

# PRD → Features (p2f)

Stage 1 of the 8-stage pipeline. Reads PRD.md and updates FEATURE.md.

## Process

### 1. Read Inputs
```
→ Read docs/prd/PRD.md (or path from .local_config.yaml)
→ Read docs/design/FEATURE.md (current state)
→ Diff: what changed in PRD since last p2f run?
```

### 2. Classify Changes
For each PRD requirement, classify as:
- **NEW** — appears in PRD but not in FEATURE.md → add with status `TBD`
- **CHANGED** — exists in both but PRD description changed → update, keep status
- **REMOVED** — in FEATURE.md but removed from PRD → mark `DEPRECATED`
- **UNCHANGED** — no change → skip

### 3. Update FEATURE.md
Add new features in this format:
```markdown
## Feature: {feature-name}
**Status:** TBD
**PRD Reference:** {section in PRD}
**Description:** {what it does}
**Acceptance Criteria:**
- [ ] {criterion 1}
- [ ] {criterion 2}
```

### 4. Output
- Summary: "Added X, updated Y, deprecated Z features"
- Show diff of FEATURE.md changes
- Do NOT commit — let user review first

## Notes
- Never modify PROTECTED blocks in FEATURE.md
- Preserve existing status values (COMPLETE, IN_PROGRESS, etc.)
- Ask user before marking anything DEPRECATED
