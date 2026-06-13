from __future__ import annotations
import json
from pathlib import Path
from ..models import CoworkerConfig, ProjectCatalog, InitiativeConfig

OPENCODE_DIR = Path.home() / ".config" / "opencode"
OPENCODE_CONFIG = OPENCODE_DIR / "config.json"


def _resolve_instructions_md(project_dir: Path | None) -> Path:
    if project_dir:
        return project_dir / ".opencode" / "instructions.md"
    return Path.cwd() / ".opencode" / "instructions.md"


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
            command = [server.command] + (server.args or [])
            entry: dict = {"type": "local", "enabled": True, "command": command}
            if server.env:
                entry["env"] = server.env
            mcp_servers[server.name] = entry
        existing["mcp"] = mcp_servers

    with open(config_path, "w") as f:
        json.dump(existing, f, indent=2)
    actions.append(f"updated {config_path}")

    return actions


# ── Context injection ───────────────────────────────────────────────────────


def inject_static_context(
    catalog: ProjectCatalog, project_dir: Path | None = None
) -> list[str]:
    from .claude import (
        _build_static_block,
        _replace_or_append_block,
        STATIC_START,
        STATIC_END,
    )
    actions = []
    block = _build_static_block(catalog)
    target = _resolve_instructions_md(project_dir)

    content = target.read_text() if target.exists() else ""
    content = _replace_or_append_block(content, STATIC_START, STATIC_END, block)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)

    verb = "updated" if STATIC_START in content else "injected"
    actions.append(f"{verb} static context in {target.name}")
    return actions


def inject_initiative(
    config: InitiativeConfig, project_dir: Path | None = None
) -> list[str]:
    from .claude import _build_initiative_block, _remove_all_initiative_blocks
    actions = []
    block = _build_initiative_block(config)
    target = _resolve_instructions_md(project_dir)

    content = target.read_text() if target.exists() else ""
    content = _remove_all_initiative_blocks(content)
    content = content.rstrip() + "\n\n" + block + "\n"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    actions.append(f"injected initiative '{config.name}' into {target.name}")
    return actions


def remove_initiative(project_dir: Path | None = None) -> list[str]:
    from .claude import _remove_all_initiative_blocks
    actions = []
    target = _resolve_instructions_md(project_dir)
    if not target.exists():
        return actions

    content = target.read_text()
    new_content = _remove_all_initiative_blocks(content)
    if new_content != content:
        target.write_text(new_content)
        actions.append(f"removed initiative context from {target.name}")
    return actions
