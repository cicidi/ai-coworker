---
name: design-c2d
description: Code → Design. Sync code changes back to DESIGN.md to prevent doc rot
aliases: [c2d]
---

# Code → Design (c2d)

Stage 6 of the 8-stage pipeline. Keeps DESIGN.md accurate after implementation.

## Process

### 1. Detect Changes
```
→ git diff main...HEAD -- "*.{go,py,ts,js,java,rs,rb}" 
→ Identify: new endpoints, changed data models, new services, removed APIs
```

### 2. Compare with DESIGN.md
For each code change, check:
- Is it documented in DESIGN.md?
- If yes — is the documentation accurate?
- If no — is it missing intentionally (internal detail) or accidentally?

### 3. Update DESIGN.md
Update only what changed:
- **New endpoints** → add to API section
- **Changed request/response shape** → update schema
- **New data model fields** → update data model section
- **Removed endpoints** → mark as deprecated or remove
- **New components** → add to architecture section

### 4. Flag Divergences
If code diverges significantly from design, flag:
```
⚠️ Divergence detected:
Design says: POST /users returns { id, email }
Code returns: { id, email, createdAt }
→ Updated DESIGN.md to match code
```

### 5. Commit
```
git add docs/design/DESIGN.md
git commit -m "docs: sync design with implementation — {summary}"
```

## Notes
- Never remove PROTECTED sections
- When in doubt, ask rather than guess intent
- If design divergence is large, surface it for human review before updating
