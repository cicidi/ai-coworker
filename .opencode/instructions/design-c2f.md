---
name: design-c2f
description: Code → Features. Scan code to mark implemented features as COMPLETE in FEATURE.md
aliases: [c2f]
---

# Code → Features (c2f)

Stage 5 of the 8-stage pipeline. Marks features as COMPLETE after implementation.

## Process

### 1. Scan Code
```
→ Read all changed/new files in the PR or current branch
→ Map code to features in FEATURE.md by:
  - Function/endpoint names matching feature descriptions
  - File names matching feature areas
  - Comments referencing feature IDs
```

### 2. Verify Against Acceptance Criteria
For each feature candidate:
- Check each acceptance criterion in FEATURE.md
- Mark ✅ if criterion is met by code
- Leave ❌ if not yet implemented

### 3. Update FEATURE.md Status
- If all criteria ✅ → status: `COMPLETE`
- If some criteria ✅ → status: `IN_PROGRESS`, note which criteria remain
- If no criteria ✅ → leave as `TBD` or `IN_PROGRESS`

### 4. Detect Untracked Features
If code implements something NOT in FEATURE.md:
```
⚠️ Untracked feature detected:
Code implements: {description}
Not found in FEATURE.md
→ Add to FEATURE.md? (y/n)
```

### 5. Output
- Summary: "Marked X features COMPLETE, Y IN_PROGRESS, found Z untracked"
- Show FEATURE.md diff
- Commit:
```
git commit -m "docs: mark {feature names} as COMPLETE"
```
