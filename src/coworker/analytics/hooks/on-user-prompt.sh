#!/usr/bin/env bash
source "${0%/*}/common.sh"
ensure_session

content=$(cat)
seq=$(next_seq)
ts=$(date '+%Y-%m-%dT%H:%M:%S%z')
escaped=$(echo "$content" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))" 2>/dev/null || echo "\"$content\"")

printf '{"ts":"%s","type":"user","seq":%s,"content":%s}' "$ts" "$seq" "$escaped" | append_jsonl "messages.jsonl"
