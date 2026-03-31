from __future__ import annotations
import json
from pathlib import Path
from ..models import CoworkerConfig

OPENCODE_DIR = Path.home() / ".config" / "opencode"
OPENCODE_CONFIG = OPENCODE_DIR / "config.json"


def sync(config: CoworkerConfig, project_dir: Path | None = None) -> list[str]:
    """Sync coworker config to OpenCode. Returns list of actions taken."""
    actions = []

    if project_dir:
        config_path = project_dir / ".opencode" / "config.json"
    else:
        config_path = OPENCODE_CONFIG

    config_path.parent.mkdir(parents=True, exist_ok=True)
    existing = {}
    if config_path.exists():
        with open(config_path) as f:
            existing = json.load(f)

    # apply opencode-specific overrides
    existing.update(config.opencode.extra)

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
        existing["mcp"] = {"servers": mcp_servers}

    with open(config_path, "w") as f:
        json.dump(existing, f, indent=2)
    actions.append(f"updated {config_path}")

    return actions
