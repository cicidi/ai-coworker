---
name: coworker-design-c2d
triggers:
  - c2d
  - sync design doc
  - update DESIGN.md from code
  - code changed update design
description: |
  Sync code changes back to DESIGN.md to prevent doc rot. Run after any code
  change that affects APIs, data models, or architecture. Keeps design docs
  in sync with the actual implementation.
services:
  category: coworker-design
when_to_use: |
  After implementing code that changes APIs, data models, or system architecture.
  When user says "c2d", "update the design doc", or "sync design".
when_not_to_use: |
  Skip for pure bug fixes that do not change any interface or data structure.
version: 1.0.0
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
