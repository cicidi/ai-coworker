---
name: self-heal
description: Log correction traces to project's .self-healing/ directory. Auto-detects missing hook.
aliases: [trace, log-correction, heal]
---

# Self-Heal

Log every user correction for pattern analysis.

## Trigger

Auto-detected when user corrects AI. Keywords: "no", "don't", "stop", "wrong", "not like that", "never do", "I told you".

## Process

### 1. Check Hook

```bash
ls .claude/hooks/on-self-heal.sh 2>/dev/null
```

If hook exists → skip to step 2.

If hook NOT found:
```
→ "Self-healing hook not installed. Install it? (y/n)"
→ If yes: create .claude/hooks/on-self-heal.sh
→ Register in .claude/settings.json:
  {
    "hooks": {
      "UserPromptSubmit": [
        {"matcher": "", "command": ".claude/hooks/on-self-heal.sh"}
      ]
    }
  }
```

### 2. Write Trace

Store in project root: `.self-healing/traces/{YYYY-MM-DD}.yaml`

```yaml
- id: {uuid4}
  timestamp: {ISO8601}
  context: "what AI did wrong"
  correction: "what user said"
  category: code-conventions|workflow|security|architecture|tool-use
```

### 3. Acknowledge

```
"Logged correction: '{rule}'. Run self-analyze later to find patterns."
```

## Hook Script

```bash
#!/usr/bin/env bash
# .claude/hooks/on-self-heal.sh
# Detects user corrections and writes trace YAML

input=$(cat)
# Check for correction keywords
if echo "$input" | grep -qiE "\b(no|don'?t|stop|wrong|not like that|never|i told you)\b"; then
  DIR=".self-healing/traces"
  mkdir -p "$DIR"
  FILE="$DIR/$(date +%Y-%m-%d).yaml"
  ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$RANDOM")
  cat >> "$FILE" <<YAML
- id: $ID
  timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
  context: ""
  correction: "$(echo "$input" | tr '\n' ' ' | sed 's/"/\\"/g' | cut -c1-200)"
  category: workflow
YAML
  echo " "  # hook must output something
fi
```

## Categories

- `code-conventions` — style, naming, imports
- `workflow` — pipeline steps, commits, PRs
- `security` — secrets, injection
- `architecture` — design, patterns
- `tool-use` — wrong tool, wrong command
