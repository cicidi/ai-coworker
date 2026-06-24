---
name: bug-report
description: Create a GitHub Issue — for project bugs, coworker system issues, or feature requests
aliases: [new-issue, create-issue, report-bug, issue]
---

# Bug Report

Create a structured GitHub Issue. Covers project bugs, coworker system issues, and feature requests.

## When to Use

- User reports a bug or unexpected behavior
- Coworker system itself malfunctions
- Feature request that needs discussion
- Any non-trivial change before code

## Process

### 1. Detect Scope

```
→ Is this a code bug? → label: bug
→ Is this a coworker system issue? → label: coworker
→ Is this a feature request? → label: enhancement
```

### 2. Gather Context

```
→ What happened vs what was expected?
→ Steps to reproduce (if bug)
→ Relevant files, error messages, screenshots
→ Affected components
```

### 3. Title

```
fix: {short description}    (for bugs)
feat: {short description}   (for features)
chore: {short description}  (for maintenance)
```

### 4. Body

```markdown
## What happened
{description}

## Expected behavior
{expected}

## Steps to reproduce (if bug)
1. 
2. 

## Context
- Project: {name}
- Branch: {branch}
- Relevant files: {paths}
```

### 5. Create & Link

```bash
gh issue create \
  --title "fix: {description}" \
  --body "{body}" \
  --label "{labels}" \
  --assignee @me
```

### 6. If AI Mistake

If this was caused by an AI error, also:

```
→ Log self-heal trace for this correction
→ Note in issue body: "AI caused: {what went wrong}"
```

## Rules

- One issue per problem
- Fill in all sections before creating
- Always assign yourself
- Never skip the issue for non-trivial changes
