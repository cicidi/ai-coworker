---
name: review-checkpoint
description: After each pipeline phase, prompt user to confirm with the right reviewer before proceeding
aliases: [checkpoint, confirm-phase]
---

# Review Checkpoint (Auto-Applied)

Runs automatically after each stage of the 8-stage pipeline. Human confirms before proceeding.

## Checkpoints

### After p2f (PRD → Features)
```
📋 FEATURE.md updated:
  Added: {N} features
  Updated: {N} features
  Deprecated: {N} features

Please review FEATURE.md before proceeding to Design.
→ Continue to f2d? (y/n)
```

### After f2d (Features → Design)
```
📐 DESIGN.md updated:
  {Summary of design decisions}
  Open questions: {N}

⚠️  Open questions need answers before planning:
  - {question 1}
  - {question 2}

→ Resolve questions and continue to d2pl? (y/n)
```

### After d2pl (Design → Plan)
```
📝 Plan created: docs/planning/plan_{id}.md
  Waves: {N}
  Tasks: {N}
  MAC: {N} criteria

MAC preview:
{list MAC items}

→ Approve plan and start coding? (y/n)
```

### After pl2c Wave N
```
⚡ Wave {N} complete:
  Tasks: {N}/{total} done
  Commits: {list}
  Failures: {N}

→ Continue to Wave {N+1}? (y/n)
```

### After verify
```
✅ / ❌ MAC Verification:
  Passed: {N}/{total} criteria
  
{If failed}: Root cause: {description}
             Fix required before PR

→ Create PR? (y/n)
```

### After review-checkpoint
```
📤 PR ready:
  Title: {title}
  Reviewer: {name}
  Message drafted

→ Send review request? (y/n)
```

## Override
If user says "skip checkpoint" or "just do it":
```
→ Log: "Checkpoint skipped by user"
→ Proceed
→ Note in PR description that checkpoint was bypassed
```
