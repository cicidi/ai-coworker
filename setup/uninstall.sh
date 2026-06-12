#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# ai-coworker uninstall.sh
# Removes installed skills from IDE directories
# Does NOT touch personal/ or .local_config.yaml
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
error() { echo -e "${RED}✗${NC} $*"; }
ok()    { echo -e "${GREEN}✓${NC} $*"; }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI Coworker — Uninstall"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
warn "This will remove AI coworker skills from your IDE directories."
warn "It will NOT delete personal/ or .local_config.yaml"
echo ""
read -rp "Continue? (y/n) [n]: " CONFIRM
CONFIRM="${CONFIRM:-n}"
[[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]] && echo "Aborted." && exit 0

echo ""
echo "Remove from:"
echo "  1) Global (~/.claude/commands/ etc.)"
echo "  2) Project (current directory)"
echo "  3) Both"
read -rp "Choice [1]: " CHOICE
CHOICE="${CHOICE:-1}"

REMOVED=0

remove_skills() {
  local target_dir="$1"
  if [[ ! -d "$target_dir" ]]; then return; fi

  # Get list of skill filenames from templates
  for skill in "$REPO_ROOT"/templates/team-common/skills/*.md \
               "$REPO_ROOT"/templates/personal/skills/*.md; do
    [[ -f "$skill" ]] || continue
    filename="$(basename "$skill")"
    if [[ -f "$target_dir/$filename" ]]; then
      rm "$target_dir/$filename"
      ((REMOVED++)) || true
    fi
  done
}

case "$CHOICE" in
  1)
    remove_skills "$HOME/.claude/commands"
    remove_skills "$HOME/.cursor/rules"
    remove_skills "$HOME/.opencode/instructions"
    remove_skills "$HOME/.gemini"
    ;;
  2)
    remove_skills "$(pwd)/.claude/commands"
    remove_skills "$(pwd)/.cursor/rules"
    remove_skills "$(pwd)/.opencode/instructions"
    remove_skills "$(pwd)/.gemini"
    ;;
  3)
    remove_skills "$HOME/.claude/commands"
    remove_skills "$HOME/.cursor/rules"
    remove_skills "$HOME/.opencode/instructions"
    remove_skills "$HOME/.gemini"
    remove_skills "$(pwd)/.claude/commands"
    remove_skills "$(pwd)/.cursor/rules"
    remove_skills "$(pwd)/.opencode/instructions"
    remove_skills "$(pwd)/.gemini"
    ;;
  *) error "Invalid choice"; exit 1 ;;
esac

echo ""
ok "Uninstall complete — removed $REMOVED skill files"
echo "   personal/ and .local_config.yaml preserved"

# Cleanup analytics hooks from Claude Code settings
CLAUDE_SETTINGS="$HOME/.claude/settings.json"
if [[ -f "$CLAUDE_SETTINGS" ]]; then
  python3 -c "
import json
with open('$CLAUDE_SETTINGS') as f: cfg = json.load(f)
hooks = cfg.get('hooks', {})
for h in ['UserPromptSubmit', 'PreToolUse', 'PostToolUse', 'Stop']:
    hooks.pop(h, None)
if not hooks: cfg.pop('hooks', None)
with open('$CLAUDE_SETTINGS', 'w') as f: json.dump(cfg, f, indent=2)
print('Hooks removed')
" 2>/dev/null && echo "  Analytics hooks removed from Claude Code"
fi

# Remove OpenCode plugin registration
OPENCODE_CONFIG="$HOME/.config/opencode/config.json"
if [[ -f "$OPENCODE_CONFIG" ]]; then
  python3 -c "
import json
with open('$OPENCODE_CONFIG') as f: cfg = json.load(f)
plugins = cfg.get('plugin', [])
plugin_path = '$REPO_ROOT/.opencode/coworker-analytics'
cfg['plugin'] = [p for p in plugins if p != plugin_path]
with open('$OPENCODE_CONFIG', 'w') as f: json.dump(cfg, f, indent=2)
print('Plugin removed')
" 2>/dev/null && echo "  OpenCode analytics plugin unregistered"
fi

echo "   Analytics data at ~/.coworker/analytics/ preserved (delete manually if needed)"
