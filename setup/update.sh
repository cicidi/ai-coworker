#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# ai-coworker update.sh
# Pulls latest from upstream and re-runs install
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}→${NC} $*"; }
ok()  { echo -e "${GREEN}✓${NC} $*"; }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI Coworker — Update"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$REPO_ROOT"

# Check for upstream remote
if ! git remote get-url upstream &>/dev/null; then
  log "No upstream remote found. Fetching from origin..."
  git fetch origin main
  git merge origin/main --no-edit
else
  log "Fetching from upstream..."
  git fetch upstream
  git merge upstream/main --no-edit
fi

ok "Repository updated"

# Re-run install with same mode as before
CONFIG="$HOME/.config/ai-coworker/config.yaml"
if [[ -f "$CONFIG" ]]; then
  SAVED_MODE=$(grep "install_mode:" "$CONFIG" 2>/dev/null | awk '{print $2}' || echo "global")
  log "Re-running install (mode: $SAVED_MODE)..."
  bash "$SCRIPT_DIR/install.sh" "--$SAVED_MODE"
else
  log "Re-running install..."
  bash "$SCRIPT_DIR/install.sh" --global
fi

ok "Update complete!"
