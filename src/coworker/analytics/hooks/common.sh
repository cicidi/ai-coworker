#!/usr/bin/env bash
BASE="$HOME/.coworker/analytics"
SESSIONS="$BASE/sessions"

generate_session_id() {
  echo "$(date +%Y-%m-%d-T%H%M%S)-$(openssl rand -hex 3)"
}

ensure_session() {
  if [ -z "$SESSION_ID" ] || [ ! -d "$SESSIONS/$SESSION_ID" ]; then
    SESSION_ID=$(ls -t "$SESSIONS" 2>/dev/null | head -1)
    if [ -z "$SESSION_ID" ]; then
      SESSION_ID=$(generate_session_id)
      mkdir -p "$SESSIONS/$SESSION_ID"
      cat > "$SESSIONS/$SESSION_ID/session.yaml" <<YAML
session_id: "$SESSION_ID"
created: "$(date '+%Y-%m-%dT%H:%M:%S%z')"
ide: "claude-code"
cwd: "$(pwd)"
YAML
    fi
  fi
  SEQ_FILE="$SESSIONS/$SESSION_ID/.seq"
}

next_seq() {
  local seq=0
  [ -f "$SEQ_FILE" ] && seq=$(cat "$SEQ_FILE")
  seq=$((seq + 1))
  echo "$seq" > "$SEQ_FILE"
  echo "$seq"
}

append_jsonl() {
  local file="$1" json="$2"
  echo "$json" >> "$SESSIONS/$SESSION_ID/$file" 2>/dev/null || true
}

escape_json() {
  echo "$1" | sed 's/\\/\\\\/g; s/"/\\"/g' | tr -d '\n'
}
