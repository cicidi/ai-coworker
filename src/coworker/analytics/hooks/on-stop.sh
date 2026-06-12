#!/usr/bin/env bash
source "${0%/*}/common.sh"
ensure_session

ts=$(date '+%Y-%m-%dT%H:%M:%S%z')
echo "closed: \"$ts\"" >> "$SESSIONS/$SESSION_ID/session.yaml"

msg_count=$(wc -l < "$SESSIONS/$SESSION_ID/messages.jsonl" 2>/dev/null || echo 0)
tool_count=$(wc -l < "$SESSIONS/$SESSION_ID/tools.jsonl" 2>/dev/null || echo 0)
created=$(grep "created:" "$SESSIONS/$SESSION_ID/session.yaml" 2>/dev/null | head -1 | cut -d'"' -f2)

printf '{"session_id":"%s","created":"%s","ide":"claude-code","message_count":%s,"tool_count":%s}\n' \
  "$SESSION_ID" "$created" "$msg_count" "$tool_count" >> "$BASE/index.jsonl"
