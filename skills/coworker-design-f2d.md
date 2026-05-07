---
name: coworker-design-f2d
triggers:
  - f2d
  - features to design
  - create DESIGN.md
  - design from features
description: |
  Create or update DESIGN.md with architecture, API specs, data model, and
  diagrams from FEATURE.md. Produces a full technical design document.
services:
  category: coworker-design
when_to_use: |
  When FEATURE.md is ready and needs a technical design. When user says "f2d",
  "create the design", or "design this feature".
when_not_to_use: |
  Do not use without a FEATURE.md. Use the full 8-stage pipeline.
dependencies:
  - coworker-design-p2f
version: 1.0.0
---

# Features → Design (f2d)

Stage 2 of the 8-stage pipeline. Creates or updates DESIGN.md based on TBD features.

## Process

### 1. Read Inputs
```
→ Read FEATURE.md — find all features with status TBD
→ Read existing DESIGN.md (if exists)
→ Read existing code for context (if project already has code)
```

### 2. Design Each Feature
For each TBD feature, produce:

**Architecture**
- How does it fit into existing system?
- What new components/services are needed?
- What existing components are modified?

**API Design** (if applicable)
```
GET/POST/PUT/DELETE /endpoint
Request: { field: type }
Response: { field: type }
Errors: 400/401/404/500
```

**Data Model** (if applicable)
```
Table/Collection: {name}
Fields: { field: type, constraints }
Indexes: { field }
Relations: { foreign keys }
```

**Diagrams** (as ASCII or Mermaid)
```mermaid
graph TD
    A --> B
```

### 3. Update DESIGN.md
Structure:
```markdown
# Design: {project}

## Architecture Overview
...

## Feature: {name}
### Overview
### API
### Data Model
### Diagrams
### Open Questions
```

### 4. Output
- Updated DESIGN.md
- List of open questions for human review
- Do NOT commit — let user review

## Model Recommendation
Use the most capable model available (Opus) for design decisions.
