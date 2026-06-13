---
name: coworker-meta-doc-protection
triggers:
  - protect this section
  - add protected block
  - lock this content
  - never edit this block
description: |
  Manage PROTECTED blocks in documents. AI must never modify content inside
  blocks marked with PROTECTED and END PROTECTED tags.
services:
  category: coworker-meta
when_to_use: |
  When user wants to protect a section of a document from AI edits. When
  user says "never change this" or "lock this section".
when_not_to_use: |
  false
version: 1.0.0
---

# Document Protection

PROTECTED blocks mark content that AI must never modify — human judgments, business rules, architecture decisions.

## PROTECTED Block Format

```html
<!-- PROTECTED -->
Content that AI must never modify, move, remove, or reformat.
This represents human decisions with context AI doesn't have.
<!-- END PROTECTED -->
```

## Rules (enforced automatically)
- AI **MUST NOT** modify, move, remove, or reformat content between markers
- AI **CAN** read protected content for context
- AI **CAN** suggest adding protection to critical sections
- AI **CAN** add new content outside protected blocks

## Adding Protection

To protect a section, wrap it:
```
→ Ask: "Which section should be protected?"
→ Add <!-- PROTECTED --> before and <!-- END PROTECTED --> after
→ Commit with message: "docs: protect {section name}"
```

## Removing Protection

Only the human can remove protection:
```
→ User explicitly says "unprotect this section"
→ Remove the markers
→ Commit with message: "docs: unprotect {section name}"
```

## Good Candidates for Protection
- PRD requirements (written by product)
- Architecture decisions with business context
- Legal / compliance language
- Team agreements and SLAs
- Security policies
