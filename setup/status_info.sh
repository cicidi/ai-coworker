#!/bin/sh
# tmux status bar: session name | project | branch: X | status: X | initiative: X

SESSION=$(tmux display-message -p '#{session_name}' 2>/dev/null)
PANE_PATH=$(tmux display-message -p -F '#{pane_current_path}' 2>/dev/null)

if [ ! -d "$PANE_PATH" ]; then
    exit 0
fi
cd "$PANE_PATH" || exit 0

# ── Session name ──
printf "#[fg=colour240]tmux:#[fg=green]%s#[fg=colour240] | " "$SESSION"

# ── Project folder ──
PROJECT_DIR=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$PROJECT_DIR" ]; then
    FOLDER=$(basename "$PROJECT_DIR")
else
    FOLDER=$(basename "$PWD")
fi
printf "#[fg=colour240]project:#[fg=brightwhite]%s#[fg=colour240] | " "$FOLDER"

# ── Worktree name (only shown inside a git worktree) ──
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)
GIT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null)
SUPERPROJECT=$(git rev-parse --show-superproject-working-tree 2>/dev/null)
if [ "$GIT_DIR" != "$GIT_COMMON" ] && [ -z "$SUPERPROJECT" ]; then
    WORKTREE_NAME=$(basename "$GIT_DIR")
    printf "#[fg=colour240]worktree:#[fg=brightcyan]%s#[fg=colour240] | " "$WORKTREE_NAME"
fi

# ── Git branch ──
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$BRANCH" ]; then
    printf "#[fg=colour240]branch:#[fg=cyan]%s" "$BRANCH"
else
    printf "#[fg=colour240]branch:#[fg=colour245]--"
fi

# ── Git status (ahead/behind/dirty) ──
if [ -n "$BRANCH" ]; then
    BEHIND=0
    AHEAD=0
    REMOTE=$(git rev-parse --abbrev-ref "@{u}" 2>/dev/null)
    if [ -n "$REMOTE" ]; then
        BEHIND=$(git rev-list --count HEAD.."@{u}" 2>/dev/null || echo 0)
        AHEAD=$(git rev-list --count "@{u}"..HEAD 2>/dev/null || echo 0)
    fi

    DIRTY=0
    STAGED=0
    UNTRACKED=0
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        DIRTY=1
        STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l)
        UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l)
    fi

    printf " #[fg=colour240]status:"
    [ "$AHEAD" -gt 0 ] && printf "#[fg=yellow]%s" "↑${AHEAD}"
    [ "$BEHIND" -gt 0 ] && printf "#[fg=red]%s" "↓${BEHIND}"
    [ "$STAGED" -gt 0 ] && printf "#[fg=green]%s" "+${STAGED}"
    [ "$UNTRACKED" -gt 0 ] && printf "#[fg=magenta]%s" "?${UNTRACKED}"
    [ "$DIRTY" -eq 1 ] && printf "#[fg=yellow]*" || printf "#[fg=green]✓"
fi

# ── Initiative ──
INITIATIVE=""
for DIR in "$PANE_PATH" "$PROJECT_DIR" "$HOME"; do
    if [ -n "$DIR" ] && [ -f "$DIR/.coworker/initiatives/.active" ]; then
        INITIATIVE=$(cat "$DIR/.coworker/initiatives/.active" 2>/dev/null)
        break
    fi
done
if [ -n "$INITIATIVE" ]; then
    printf " #[fg=colour240]| initiative:#[fg=magenta]%s" "$INITIATIVE"
fi
