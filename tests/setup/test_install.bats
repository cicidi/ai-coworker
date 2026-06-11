#!/usr/bin/env bats

# Tests for install.sh — CLAUDE.md creation, skill-factory setup, install modes

setup() {
  TEST_TMP="$(mktemp -d)"
  export HOME="$TEST_TMP/home"
  mkdir -p "$HOME/.claude"
  mkdir -p "$HOME/.config/opencode/skills"

  # Mock git
  mkdir -p "$TEST_TMP/bin"
  cat > "$TEST_TMP/bin/git" << 'GITEOF'
#!/usr/bin/env bash
case "$1" in
  clone)
    mkdir -p "${@: -1}/ai-coworker-skills/skill-create" "${@: -1}/personal-skills" "${@: -1}/import-skills/tdd"
    cat > "${@: -1}/ai-coworker-skills/skill-create/SKILL.md" << 'SKEOF'
---
name: ai-coworker-skill-create
description: Use when creating a new skill
license: MIT
compatibility: opencode
metadata:
  triggers:
    - create a skill
---
# ai-coworker-skill-create
SKEOF
    cat > "${@: -1}/import-skills/tdd/SKILL.md" << 'SKEOF'
---
name: tdd
description: Use when writing tests first
license: MIT
compatibility: opencode
metadata:
  triggers:
    - test-driven
---
# TDD
SKEOF
    echo "Cloned."
    ;;
  pull)
    echo "Already up to date."
    ;;
  -C)
    shift
    "$@"
    ;;
  *)
    exit 0
    ;;
esac
GITEOF
  chmod +x "$TEST_TMP/bin/git"
  export PATH="$TEST_TMP/bin:$PATH"

  # Mock coworker CLI
  cat > "$TEST_TMP/bin/coworker" << 'COEOF'
#!/usr/bin/env bash
exit 0
COEOF
  chmod +x "$TEST_TMP/bin/coworker"

  # Set up repo root pointing to the real install.sh
  export REPO_ROOT
  REPO_ROOT="$(cd "$(dirname "$BATS_TEST_DIRNAME")/.." && pwd)"
}

teardown() {
  rm -rf "$TEST_TMP"
}

# =============================================================================
# Test: Global CLAUDE.md creation
# =============================================================================
@test "creates global CLAUDE.md when missing" {
  rm -f "$HOME/.claude/CLAUDE.md"

  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  [ -f "$HOME/.claude/CLAUDE.md" ]
  grep -q "Question Requirement" "$HOME/.claude/CLAUDE.md"
  grep -q "ask 1-3 clarifying questions" "$HOME/.claude/CLAUDE.md"
}

@test "preserves existing global CLAUDE.md" {
  echo "Custom content" > "$HOME/.claude/CLAUDE.md"

  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  grep -q "Custom content" "$HOME/.claude/CLAUDE.md"
}

# =============================================================================
# Test: Skill-factory setup
# =============================================================================
@test "clones skill-factory to correct path" {
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  [ -d "$HOME/.config/opencode/skills/skill-factory" ]
  [ -d "$HOME/.config/opencode/skills/skill-factory/ai-coworker-skills" ]
  [ -d "$HOME/.config/opencode/skills/skill-factory/personal-skills" ]
  [ -d "$HOME/.config/opencode/skills/skill-factory/import-skills" ]
}

# =============================================================================
# Test: Global install mode
# =============================================================================
@test "installs to global Claude Code directory" {
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  [ -d "$HOME/.claude/commands" ]
}

# =============================================================================
# Test: Project install mode
# =============================================================================
@test "installs to project Claude Code directory" {
  local project_dir="$TEST_TMP/myproject"
  mkdir -p "$project_dir"

  run bash "$REPO_ROOT/setup/install.sh" --project "$project_dir" <<< $'0'
  [ "$status" -eq 0 ]
  [ -d "$project_dir/.claude/commands" ]
}

# =============================================================================
# Test: coworker-meta-setup-coworker always installed
# =============================================================================
@test "always installs coworker-meta-setup-coworker" {
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  [ -f "$HOME/.claude/commands/coworker-meta-setup-coworker.md" ]
}

# =============================================================================
# Test: Skill selection — none (default)
# =============================================================================
@test "installs no extra skills when none selected" {
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  # Only setup-coworker should be installed
  [ -f "$HOME/.claude/commands/coworker-meta-setup-coworker.md" ]
  run ls "$HOME/.claude/commands/"
  # Should have exactly 1 file
  [ "${#lines[@]}" -eq 1 ]
}

# =============================================================================
# Test: Skill selection — all
# =============================================================================
@test "installs all skills when 'all' selected" {
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'1'
  [ "$status" -eq 0 ]
  [ -f "$HOME/.claude/commands/coworker-meta-setup-coworker.md" ]
  [ -f "$HOME/.claude/commands/skill-create.md" ]
  [ -f "$HOME/.claude/commands/tdd.md" ]
}

# =============================================================================
# Test: Skill upgrade (existing file updated)
# =============================================================================
@test "updates existing skill when source changed" {
  # Install first time
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]

  # Modify the installed file to simulate an old version
  echo "old content" > "$HOME/.claude/commands/coworker-meta-setup-coworker.md"

  # Re-install — should update
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  ! grep -q "old content" "$HOME/.claude/commands/coworker-meta-setup-coworker.md"
}

# =============================================================================
# Test: Skill skips when identical
# =============================================================================
@test "skips already up-to-date skills" {
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]

  # Re-install — should skip
  run bash "$REPO_ROOT/setup/install.sh" --global <<< $'0'
  [ "$status" -eq 0 ]
  echo "$output" | grep -q "Skipped"
}

# =============================================================================
# Test: Invalid install choice fails gracefully
# =============================================================================
@test "handles invalid mode choice gracefully" {
  run bash "$REPO_ROOT/setup/install.sh" <<< $'99'
  [ "$status" -ne 0 ]
}
