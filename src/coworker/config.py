from __future__ import annotations
import os
from pathlib import Path
import yaml
from .models import CoworkerConfig

GLOBAL_DIR = Path.home() / ".coworker"
GLOBAL_CONFIG = GLOBAL_DIR / "coworker.yaml"
PROJECT_CONFIG_NAME = ".coworker/coworker.yaml"


def find_project_config() -> Path | None:
    """Walk up from cwd to find .coworker/coworker.yaml"""
    current = Path.cwd()
    while current != current.parent:
        candidate = current / PROJECT_CONFIG_NAME
        if candidate.exists():
            return candidate
        current = current.parent
    return None


def load_config(path: Path) -> CoworkerConfig:
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return CoworkerConfig(**data)


def load_global_config() -> CoworkerConfig | None:
    if GLOBAL_CONFIG.exists():
        return load_config(GLOBAL_CONFIG)
    return None


def load_project_config() -> CoworkerConfig | None:
    path = find_project_config()
    if path:
        return load_config(path)
    return None


def merged_config() -> CoworkerConfig:
    """Project config overrides global config."""
    base = load_global_config() or CoworkerConfig()
    project = load_project_config()
    if not project:
        return base

    # merge: project MCP + skills append to global, project permissions override
    merged = base.model_copy(deep=True)

    # add project MCP servers (deduplicate by name)
    existing_names = {s.name for s in merged.mcp}
    for server in project.mcp:
        if server.name not in existing_names:
            merged.mcp.append(server)
        else:
            # project overrides global for same-name server
            merged.mcp = [server if s.name == server.name else s for s in merged.mcp]

    # add project skills (deduplicate by name)
    existing_skills = {s.name for s in merged.skills}
    for skill in project.skills:
        if skill.name not in existing_skills:
            merged.skills.append(skill)

    # project permissions override global
    if project.permissions.allow:
        merged.permissions.allow = project.permissions.allow
    if project.permissions.deny:
        merged.permissions.deny = project.permissions.deny

    return merged


def save_config(config: CoworkerConfig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = config.model_dump(exclude_none=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
