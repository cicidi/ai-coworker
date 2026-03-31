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
