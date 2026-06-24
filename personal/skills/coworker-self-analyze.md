---
name: coworker-self-analyze
triggers:
  - analyze correction traces
  - self analyze
  - find correction patterns
  - generate new rules from traces
description: |
  Analyze correction traces (2+ occurrences of same mistake) and generate new
  skills or rules to prevent recurrence. Self-improving loop for the AI coworker.
services:
  category: coworker-meta
when_to_use: |
  When user asks to analyze correction patterns, after 5+ traces accumulate,
  or periodically for self-improvement of the AI system.
when_not_to_use: |
  Skip if fewer than 2 correction traces exist — patterns need volume to be reliable.
dependencies:
  - coworker-meta-self-healing-trace
version: 1.0.0
---

# Self-Healing Analyze

Reads all correction traces and generates actionable rules or new skills from patterns.

## Process

### 1. Load Traces
```
→ Read all files in ~/.claude/self-healing/traces/
→ Parse YAML
→ Group by category
→ Sort by frequency descending
```

### 2. Find Patterns
A pattern = same correction occurring 2+ times:
```
→ Group traces by (category + normalized correction text)
→ Flag groups with frequency >= 2
→ Show: "Found pattern: '{rule}' occurred {N} times"
```

### 3. Generate Rules
For each pattern, generate a rule:

**For code-conventions patterns** → add to `commit-code-conventions.md`
**For workflow patterns** → add to `CLAUDE.md` workflow section
**For security patterns** → add to `commit-guardrails.md`
**For tool-use patterns** → add to relevant `mcp-*.md` skill

Rule format:
```markdown
- **Never {bad behavior}** — {reason from traces}
  Example: "Never use fully qualified Java class names — use imports instead"
```

### 4. Suggest New Skill (if needed)
If pattern is complex enough to warrant its own skill:
```
→ "Pattern '{name}' is complex. Create a new skill? (y/n)"
→ If yes: invoke create-skill with the pattern as the skill body
```

### 5. Create PR
```
→ git checkout -b fix/self-healing-{date}
→ Add generated rules to appropriate files
→ git commit -m "self-healing: add rules from {N} correction patterns"
→ Create PR for review
```

### 6. Archive Traces
After processing, mark traces as processed:
```yaml
processed: true
processed_date: {date}
generated_rule: "{rule text}"
```
