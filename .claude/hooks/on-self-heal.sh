#!/usr/bin/env bash
# Detects user corrections and writes trace YAML to .self-healing/traces/
input=$(cat)
if echo "$input" | grep -qiE "\b(no|don'?t|stop|wrong|not like that|never|i told you)\b"; then
  DIR=".self-healing/traces"
  mkdir -p "$DIR"
  FILE="$DIR/$(date +%Y-%m-%d).yaml"
  ID=$(uuidgen 2>/dev/null || echo "$(date +%s)-$RANDOM")
  cat >> "$FILE" <<YAML
- id: $ID
  timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
  context: "AI corrected by user"
  correction: "$(echo "$input" | tr '\n' ' ' | sed 's/"/\\"/g' | cut -c1-300)"
  category: workflow
YAML
fi
echo " "
