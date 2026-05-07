---
name: coworker-meta-report-issue
triggers:
  - report coworker bug
  - something is wrong with the ai
  - file a coworker issue
description: |
  Report a bug or problem with the AI coworker system itself to GitHub Issues.
  Use when the AI misbehaves, produces wrong output, or a skill fails.
services:
  category: coworker-meta
when_to_use: |
  When user says "report this bug", "the AI did something wrong", or a skill
  consistently fails or behaves unexpectedly.
when_not_to_use: |
  Do not use for project bugs — use coworker-debug-issue-create instead.
version: 1.0.0
---

# Report Coworker Issue

Use this skill to report bugs, missing features, or incorrect behavior in the ai-coworker system.

## Process

1. **Describe the problem**
   - What did AI do that was wrong?
   - What was the expected behavior?
   - Which skill or rule caused the issue?

2. **Draft GitHub Issue**
   ```
   Title: [coworker] {short description}
   
   ## What happened
   {description of incorrect AI behavior}
   
   ## Expected behavior
   {what should have happened}
   
   ## Affected skill/rule
   {skill name or CLAUDE.md section}
   
   ## Reproduction steps
   1. ...
   2. ...
   
   ## Suggested fix
   {optional — if you know the fix}
   ```

3. **Create issue via GitHub MCP**
   - Repo: `cicidi/ai-coworker`
   - Label: `coworker-bug` or `coworker-improvement`
   - Assign to: cicidi

4. **Log a self-healing trace** if this was an AI mistake (run `self-healing-trace`)
