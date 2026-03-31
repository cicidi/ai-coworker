from __future__ import annotations
import json
from pathlib import Path
from ..models import CoworkerConfig

GEMINI_DIR = Path.home() / ".gemini"
GEMINI_SETTINGS = GEMINI_DIR / "settings.json"


def sync(config: CoworkerConfig, project_dir: Path | None = None) -> list[str]:
    """Sync coworker config to Gemini CLI. Returns list of actions taken."""
    actions = []

    if project_dir:
        settings_path = project_dir / ".gemini" / "settings.json"
    else:
        settings_path = GEMINI_SETTINGS

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if settings_path.exists():
        with open(settings_path) as f:
            existing = json.load(f)

    # apply gemini-specific overrides
    existing.update(config.gemini.extra)

    # apply MCP servers (Gemini CLI uses same mcpServers format)
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

    return actions
