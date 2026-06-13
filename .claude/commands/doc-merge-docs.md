---
name: merge-docs
description: Merge two versions of a markdown doc (e.g., after upstream sync conflicts)
aliases: [merge-markdown]
---

# Merge Docs

Merges two versions of a markdown document, preserving PROTECTED blocks and resolving conflicts intelligently.

## Process

### 1. Identify Files
```
→ Ask: "Which two files/versions to merge?"
→ Read both versions
→ Identify conflict markers (<<<<<<, =======, >>>>>>>)
```

### 2. Merge Strategy
- **PROTECTED blocks** — always keep unchanged; never modify content between `<!-- PROTECTED -->` markers
- **Headings** — preserve structure from the newer version
- **New content** — add content that appears in one version but not the other
- **Conflicting content** — show both options and ask user to choose
- **Formatting** — normalize to consistent markdown style

### 3. Validate Result
- All headings have proper hierarchy (no skipped levels)
- All links are valid
- No duplicate sections
- PROTECTED blocks are intact

### 4. Output
- Write merged result to target file
- Show diff summary: "Added X sections, resolved Y conflicts, kept Z PROTECTED blocks"
- Do NOT auto-commit — let user review first
