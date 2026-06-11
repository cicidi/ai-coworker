#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# ai-coworker update.sh
# Updates coworker itself from upstream. Optionally updates skill-factory.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_FACTORY_DIR="$HOME/.config/opencode/skills/skill-factory"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}→${NC} $*"; }
ok()  { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}⚠${NC}  $*"; }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI Coworker — Update"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# =============================================================================
# Step 1 — Update coworker repository
# =============================================================================
log "Updating ai-coworker..."

cd "$REPO_ROOT"

if ! git remote get-url upstream &>/dev/null; then
  log "Fetching from origin..."
  git fetch origin main 2>/dev/null || {
    warn "Could not fetch from origin. Is the network available?"
  }
  git merge origin/main --no-edit 2>/dev/null || {
    warn "Could not merge. You may have local changes. Resolve manually."
  }
else
  log "Fetching from upstream..."
  git fetch upstream 2>/dev/null || warn "Could not fetch upstream."
  git merge upstream/main --no-edit 2>/dev/null || {
    warn "Merge conflict or local changes detected. Resolve manually."
  }
fi

ok "ai-coworker repository updated"

# =============================================================================
# Step 2 — Re-run install with saved mode
# =============================================================================
log "Re-running install to sync skills..."

CONFIG="$HOME/.config/ai-coworker/config.yaml"
if [[ -f "$CONFIG" ]]; then
  SAVED_MODE=$(grep "install_mode:" "$CONFIG" 2>/dev/null | awk '{print $2}' || echo "global")
  bash "$SCRIPT_DIR/install.sh" "--$SAVED_MODE"
else
  bash "$SCRIPT_DIR/install.sh" --global
fi

# =============================================================================
# Step 3 — Optionally update skill-factory
# =============================================================================
echo ""
if [[ -d "$SKILL_FACTORY_DIR" ]]; then
  read -rp "  Update skill-factory from GitHub? (y/n) [n]: " UPDATE_SF
  UPDATE_SF="${UPDATE_SF:-n}"
  if [[ "$UPDATE_SF" == "y" || "$UPDATE_SF" == "Y" ]]; then
    log "Updating skill-factory..."
    git -C "$SKILL_FACTORY_DIR" pull --ff-only origin main 2>/dev/null && \
      ok "Skill-factory updated" || \
      warn "Could not update skill-factory (dirty, offline, or no upstream)."
  else
    log "Skipped skill-factory update."
  fi
else
  log "Skill-factory not installed. Run install.sh first to set it up."
fi

echo ""
ok "Update complete!"
