#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# ai-coworker install.sh
# Installs skills to all detected IDEs (Claude Code, Cursor, OpenCode, Gemini)
# Usage:
#   ./setup/install.sh              # interactive mode
#   ./setup/install.sh --global     # install to ~/.claude/commands/ etc.
#   ./setup/install.sh --project /path/to/project
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALL_MODE=""
PROJECT_PATH=""
CREATED=0
UPDATED=0
SKIPPED=0

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log()    { echo -e "${BLUE}→${NC} $*"; }
ok()     { echo -e "${GREEN}✓${NC} $*"; }
warn()   { echo -e "${YELLOW}⚠${NC}  $*"; }
error()  { echo -e "${RED}✗${NC} $*"; }

# =============================================================================
# Parse arguments
# =============================================================================
while [[ $# -gt 0 ]]; do
  case "$1" in
    --global)   INSTALL_MODE="global"; shift ;;
    --project)  INSTALL_MODE="project"; PROJECT_PATH="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: install.sh [--global | --project /path]"
      exit 0 ;;
    *) error "Unknown argument: $1"; exit 1 ;;
  esac
done

# =============================================================================
# Step 1 — Identity detection
# =============================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI Coworker — Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

USERNAME=$(whoami)
CURRENT_PROJECT=$(basename "$(pwd)")
log "Detected identity: ${USERNAME} working on ${CURRENT_PROJECT}"
read -rp "  Is this correct? (y/n) [y]: " CONFIRM
CONFIRM="${CONFIRM:-y}"
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  read -rp "  Enter your username: " USERNAME
  read -rp "  Enter your project name: " CURRENT_PROJECT
fi

# =============================================================================
# Step 2 — Install mode
# =============================================================================
if [[ -z "$INSTALL_MODE" ]]; then
  echo ""
  echo "Install location:"
  echo "  1) Global (~/.claude/commands/ etc.) — available in all projects"
  echo "  2) Project (current directory) — only this project"
  read -rp "  Choose [1]: " CHOICE
  CHOICE="${CHOICE:-1}"
  case "$CHOICE" in
    1) INSTALL_MODE="global" ;;
    2) INSTALL_MODE="project"; PROJECT_PATH="$(pwd)" ;;
    *) error "Invalid choice"; exit 1 ;;
  esac
fi

if [[ "$INSTALL_MODE" == "project" && -z "$PROJECT_PATH" ]]; then
  PROJECT_PATH="$(pwd)"
fi

# =============================================================================
# Step 3 — Role selection
# =============================================================================
echo ""
echo "Select your role(s) (space-separated, e.g. '1 3'):"
echo "  1) Backend"
echo "  2) Frontend"
echo "  3) Architect"
echo "  4) PM / Product"
echo "  5) All"
read -rp "  Roles [5]: " ROLE_INPUT
ROLE_INPUT="${ROLE_INPUT:-5}"
ROLES=()
for r in $ROLE_INPUT; do
  case "$r" in
    1) ROLES+=("backend") ;;
    2) ROLES+=("frontend") ;;
    3) ROLES+=("architect") ;;
    4) ROLES+=("pm") ;;
    5) ROLES+=("backend" "frontend" "architect" "pm") ;;
  esac
done

# =============================================================================
# Step 4 — Detect IDEs
# =============================================================================
echo ""
log "Detecting IDEs..."

CLAUDE_CODE_DIR=""
CURSOR_DIR=""
OPENCODE_DIR=""
GEMINI_DIR=""

if [[ "$INSTALL_MODE" == "global" ]]; then
  [[ -d "$HOME/.claude" ]] && CLAUDE_CODE_DIR="$HOME/.claude/commands"
  [[ -d "$HOME/.cursor" ]] && CURSOR_DIR="$HOME/.cursor/rules"
  [[ -d "$HOME/.opencode" ]] && OPENCODE_DIR="$HOME/.opencode/instructions"
  [[ -d "$HOME/.gemini" ]] && GEMINI_DIR="$HOME/.gemini"
else
  TARGET="$PROJECT_PATH"
  CLAUDE_CODE_DIR="$TARGET/.claude/commands"
  CURSOR_DIR="$TARGET/.cursor/rules"
  OPENCODE_DIR="$TARGET/.opencode/instructions"
  GEMINI_DIR="$TARGET/.gemini"
fi

# Check which are actually installed
FOUND_IDES=()
command -v claude &>/dev/null && FOUND_IDES+=("claude-code") || true
command -v cursor &>/dev/null && FOUND_IDES+=("cursor") || true
command -v opencode &>/dev/null && FOUND_IDES+=("opencode") || true
command -v gemini &>/dev/null && FOUND_IDES+=("gemini-cli") || true

if [[ ${#FOUND_IDES[@]} -eq 0 ]]; then
  warn "No IDEs auto-detected. Installing to all locations anyway."
fi

ok "IDE locations:"
echo "   Claude Code : ${CLAUDE_CODE_DIR}"
echo "   Cursor      : ${CURSOR_DIR}"
echo "   OpenCode    : ${OPENCODE_DIR}"
echo "   Gemini CLI  : ${GEMINI_DIR}"

# =============================================================================
# Helper: install a skill file to a target directory
# =============================================================================
install_skill() {
  local src="$1"
  local target_dir="$2"
  local filename
  filename="$(basename "$src")"

  mkdir -p "$target_dir"
  if [[ ! -f "$target_dir/$filename" ]]; then
    cp "$src" "$target_dir/$filename"
    ((CREATED++)) || true
  elif ! diff -q "$src" "$target_dir/$filename" &>/dev/null; then
    cp "$src" "$target_dir/$filename"
    ((UPDATED++)) || true
  else
    ((SKIPPED++)) || true
  fi
}

# =============================================================================
# Step 5 — Install skills
# =============================================================================
echo ""
log "Installing team-common skills..."

TEAM_SKILLS_DIR="$REPO_ROOT/templates/team-common/skills"
for skill in "$TEAM_SKILLS_DIR"/*.md; do
  [[ -f "$skill" ]] || continue
  [[ -n "$CLAUDE_CODE_DIR" ]] && install_skill "$skill" "$CLAUDE_CODE_DIR"
  [[ -n "$CURSOR_DIR" ]]      && install_skill "$skill" "$CURSOR_DIR"
  [[ -n "$OPENCODE_DIR" ]]    && install_skill "$skill" "$OPENCODE_DIR"
  [[ -n "$GEMINI_DIR" ]]      && install_skill "$skill" "$GEMINI_DIR"
done

log "Installing personal skills..."
PERSONAL_SKILLS_DIR="$REPO_ROOT/templates/personal/skills"
for skill in "$PERSONAL_SKILLS_DIR"/*.md; do
  [[ -f "$skill" ]] || continue
  [[ -n "$CLAUDE_CODE_DIR" ]] && install_skill "$skill" "$CLAUDE_CODE_DIR"
  [[ -n "$CURSOR_DIR" ]]      && install_skill "$skill" "$CURSOR_DIR"
  [[ -n "$OPENCODE_DIR" ]]    && install_skill "$skill" "$OPENCODE_DIR"
  [[ -n "$GEMINI_DIR" ]]      && install_skill "$skill" "$GEMINI_DIR"
done

# =============================================================================
# Step 6 — Copy personal templates (gitignored)
# =============================================================================
log "Setting up personal folder..."
PERSONAL_DIR="$REPO_ROOT/personal"
mkdir -p "$PERSONAL_DIR/context" "$PERSONAL_DIR/skills"

if [[ ! -f "$PERSONAL_DIR/context/config.yaml" ]]; then
  cp "$REPO_ROOT/templates/personal/context/config-template.yaml" \
     "$PERSONAL_DIR/context/config.yaml"
  # Fill in identity
  sed -i "s/username: cicidi/username: $USERNAME/" "$PERSONAL_DIR/context/config.yaml"
  sed -i "s/project: \"\"/project: $CURRENT_PROJECT/" "$PERSONAL_DIR/context/config.yaml"
  ok "Created personal/context/config.yaml"
fi

# =============================================================================
# Step 7 — Create .local_config.yaml (project mode)
# =============================================================================
if [[ "$INSTALL_MODE" == "project" ]]; then
  LOCAL_CONFIG="$PROJECT_PATH/.local_config.yaml"
  if [[ ! -f "$LOCAL_CONFIG" ]]; then
    cp "$REPO_ROOT/templates/personal/context/config-template.yaml" "$LOCAL_CONFIG"
    sed -i "s/username: cicidi/username: $USERNAME/" "$LOCAL_CONFIG"
    sed -i "s/project: \"\"/project: $CURRENT_PROJECT/" "$LOCAL_CONFIG"
    ok "Created .local_config.yaml"
  fi
fi

# =============================================================================
# Step 8 — Symlink CLAUDE.md for Cursor / OpenCode / Gemini
# =============================================================================
if [[ "$INSTALL_MODE" == "project" ]]; then
  CLAUDE_MD="$REPO_ROOT/CLAUDE.md"
  [[ -n "$CURSOR_DIR" ]] && ln -sf "$CLAUDE_MD" "$PROJECT_PATH/.cursorrules" 2>/dev/null || true
  [[ -n "$OPENCODE_DIR" ]] && ln -sf "$CLAUDE_MD" "$PROJECT_PATH/AGENTS.md" 2>/dev/null || true
  [[ -n "$GEMINI_DIR" ]] && ln -sf "$CLAUDE_MD" "$PROJECT_PATH/GEMINI.md" 2>/dev/null || true
fi

# =============================================================================
# Step 9 — Update .gitignore
# =============================================================================
GITIGNORE="$REPO_ROOT/.gitignore"
for entry in "personal/" ".local_config.yaml" ".env" ".cursorrules" "AGENTS.md" "GEMINI.md"; do
  grep -qxF "$entry" "$GITIGNORE" 2>/dev/null || echo "$entry" >> "$GITIGNORE"
done

# =============================================================================
# Done
# =============================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ok "Setup complete!"
echo "   Created : $CREATED files"
echo "   Updated : $UPDATED files"
echo "   Skipped : $SKIPPED files (already up-to-date)"
echo ""
# =============================================================================
# Step 10 — Sync MCP config via coworker CLI
# =============================================================================
if command -v coworker &>/dev/null; then
  echo ""
  log "Syncing MCP config via coworker CLI..."

  # Import .mcp.json if it exists in repo root
  MCP_JSON="$REPO_ROOT/.mcp.json"
  if [[ -f "$MCP_JSON" ]]; then
    log "Importing MCP servers from .mcp.json..."
    coworker import-mcp "$MCP_JSON" && ok "MCP servers imported"
  fi

  # Run sync
  coworker sync && ok "Config synced to all tools"
else
  warn "coworker CLI not found. Run: pipx install $REPO_ROOT"
  warn "Then re-run this script to sync MCP config."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next steps:"
echo "  1. Add env vars to ~/.coworker/.env (or ~/.zshrc):"
echo "     GITHUB_PERSONAL_ACCESS_TOKEN=..."
echo "     SLACK_BOT_TOKEN=..."
echo "     TELEGRAM_BOT_TOKEN=..."
echo "     TELEGRAM_CHAT_ID=..."
echo "     DISCORD_TOKEN=..."
echo "     DISCORD_GUILD_ID=..."
echo "     GDRIVE_CREDENTIALS_PATH=..."
echo "  2. Run: coworker sync"
echo "  3. Start coding with AI — skills are ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
