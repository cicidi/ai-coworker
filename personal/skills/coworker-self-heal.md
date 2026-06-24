---
name: coworker-self-heal
triggers:
  - log correction
  - trace this mistake
  - you did that wrong
  - record this error
description: |
  Log a correction trace when AI makes a mistake. Stores in YAML for pattern
  analysis. Must be called every time the user corrects the AI.
services:
  category: coworker-meta
when_to_use: |
  Every time the user corrects the AI or says "you did X wrong". Log before
  proceeding. This feeds into coworker-meta-self-analyze for pattern detection.
when_not_to_use: |
  false
version: 1.0.0
---

# Self-Healing Trace

Triggered automatically when user corrects AI behavior, or manually via this skill.

## Trigger Signals (auto-detected via UserPromptSubmit hook)
Keywords: "no", "don't", "stop", "wrong", "not like that", "never do", "I told you"

## Trace Format

Stored in `~/.claude/self-healing/traces/YYYY-MM-DD.yaml`

```yaml
- id: {uuid}
  timestamp: {ISO8601}
  trigger: user_correction
  context: "{what AI did}"
  correction: "{what user said}"
  category: {code-conventions|workflow|communication|security|architecture}
  project: {project from .local_config.yaml}
  frequency: 1
```

## Process

### 1. Capture
```
→ On correction signal detected:
→ Note: what was AI doing? What did user say?
→ Infer the rule: "AI should never... / AI should always..."
```

### 2. Write Trace
```python
# Append to ~/.claude/self-healing/traces/{date}.yaml
trace = {
    "id": uuid4(),
    "timestamp": now(),
    "context": "AI used java.util.Map instead of import",
    "correction": "Use imports, not fully qualified names",
    "category": "code-conventions",
    "frequency": 1
}
```

### 3. Acknowledge
```
"Got it — logged correction: '{rule}'. 
I'll avoid this in future. (Run self-healing-analyze to find patterns)"
```

## Categories
- `code-conventions` — style, formatting, imports, naming
- `workflow` — pipeline steps, commit messages, PR process  
- `communication` — message format, tone, channel choice
- `security` — OWASP violations, secret handling
- `architecture` — design patterns, structure decisions
- `tool-use` — wrong tool, wrong MCP, wrong command
