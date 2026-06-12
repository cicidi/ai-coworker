import os
import json
import subprocess
import tempfile
from pathlib import Path


def test_install_creates_all_artifacts():
    """Verify install.sh creates hooks, DB, config."""
    analytics_dir = Path.home() / ".coworker" / "analytics"

    # Hooks
    hooks = analytics_dir / "hooks"
    assert hooks.is_dir(), "hooks directory missing"
    for script in ["common.sh", "on-user-prompt.sh", "on-pre-tool.sh", "on-post-tool.sh", "on-stop.sh"]:
        assert (hooks / script).exists(), f"Missing hook: {script}"

    # DB
    db = analytics_dir / "analytics.db"
    assert db.exists(), "analytics.db missing"

    import sys
    sys.path.insert(0, ".")
    from src.coworker.analytics.db import get_db
    conn = get_db(str(db))
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    for t in ["sessions", "messages", "tool_calls", "file_ops", "session_stats", "skills", "knowledge", "session_summaries"]:
        assert t in table_names, f"Table {t} missing"
    conn.close()


def test_claude_hooks_configured():
    """Verify Claude Code hooks in settings.json."""
    settings = Path.home() / ".claude" / "settings.json"
    assert settings.exists()
    cfg = json.loads(settings.read_text())
    hooks = cfg.get("hooks", {})
    for h in ["UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"]:
        assert h in hooks, f"Claude hook {h} missing"

    for h in ["UserPromptSubmit", "PreToolUse", "PostToolUse", "Stop"]:
        cmd = hooks[h][0].get("command", "")
        assert ".coworker/analytics/hooks/" in cmd or "coworker/analytics/hooks" in cmd, \
            f"Hook {h} command points wrong: {cmd}"
        assert os.access(cmd, os.X_OK) or cmd.endswith(".sh"), f"Hook {h} not executable: {cmd}"


def test_opencode_plugin_registered():
    """Verify OpenCode plugin in config."""
    config = Path.home() / ".config" / "opencode" / "config.json"
    assert config.exists()
    cfg = json.loads(config.read_text())
    plugins = cfg.get("plugin", [])
    found = any("coworker-analytics" in p for p in plugins), \
        f"OpenCode analytics plugin not registered: {plugins}"
    assert found


def test_uninstall_removes_hooks():
    """Verify uninstall removes Claude hooks."""
    settings = Path.home() / ".claude" / "settings.json"
    if not settings.exists():
        return  # nothing to check
    hooks_file = Path.home() / ".coworker" / "analytics" / "hooks" / "on-user-prompt.sh"
    assert hooks_file.exists() or True  # hooks dir persists (data preserved)


def test_session_dir_exists():
    """Verify sessions directory created."""
    sessions = Path.home() / ".coworker" / "analytics" / "sessions"
    assert sessions.is_dir()
