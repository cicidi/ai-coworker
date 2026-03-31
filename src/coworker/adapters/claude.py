from __future__ import annotations
import json
import shutil
from pathlib import Path
from ..models import CoworkerConfig

CLAUDE_GLOBAL_DIR = Path.home() / ".claude"
CLAUDE_GLOBAL_SETTINGS = CLAUDE_GLOBAL_DIR / "settings.json"
CLAUDE_GLOBAL_SKILLS = CLAUDE_GLOBAL_DIR / "skills"


def sync(config: CoworkerConfig, project_dir: Path | None = None) -> list[str]:
    """Sync coworker config to Claude Code. Returns list of actions taken."""
    actions = []

    if project_dir:
        settings_path = project_dir / ".claude" / "settings.json"
        skills_dir = project_dir / ".claude" / "skills"
    else:
        settings_path = CLAUDE_GLOBAL_SETTINGS
        skills_dir = CLAUDE_GLOBAL_SKILLS

    # --- settings.json ---
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if settings_path.exists():
        with open(settings_path) as f:
            existing = json.load(f)

    # apply claude overrides
    overrides = config.claude.model_dump(exclude={"extra"})
    overrides.update(config.claude.extra)
    existing.update(overrides)

    # apply permissions
    if config.permissions.allow:
        existing["permissions"] = existing.get("permissions", {})
        existing["permissions"]["allow"] = config.permissions.allow
    if config.permissions.deny:
        existing.setdefault("permissions", {})["deny"] = config.permissions.deny

    # apply MCP servers
    if config.mcp:
        mcp_servers = {}
        for server in config.mcp:
            if not server.enabled:
                continue
            entry: dict = {"command": server.command, "args": server.args}
            if server.env:
                entry["env"] = server.env
            mcp_servers[server.name] = entry
        existing["mcpServers"] = mcp_servers

    with open(settings_path, "w") as f:
        json.dump(existing, f, indent=2)
    actions.append(f"updated {settings_path}")

    # --- skills ---
    skills_dir.mkdir(parents=True, exist_ok=True)
    for skill in config.skills:
        if not skill.enabled:
            continue
        skill_path = Path(skill.path)
        if not skill_path.is_absolute():
            # resolve relative to coworker global dir or project dir
            base = project_dir or (Path.home() / ".coworker")
            skill_path = base / skill.path
        if not skill_path.exists():
            actions.append(f"  [warn] skill path not found: {skill_path}")
            continue
        dest = skills_dir / skill.name
        dest.mkdir(parents=True, exist_ok=True)
        if skill_path.is_dir():
            for f in skill_path.iterdir():
                shutil.copy2(f, dest / f.name)
        else:
            shutil.copy2(skill_path, dest / skill_path.name)
        actions.append(f"  installed skill '{skill.name}' → {dest}")

    return actions
