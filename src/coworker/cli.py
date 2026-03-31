from __future__ import annotations
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .config import (
    GLOBAL_DIR, GLOBAL_CONFIG, PROJECT_CONFIG_NAME,
    load_global_config, load_project_config, merged_config, save_config
)
from .models import CoworkerConfig
from .adapters import ADAPTERS

console = Console()

GLOBAL_CONFIG_TEMPLATE = """\
version: "1"
scope: global

# MCP Servers — shared across Claude Code, Gemini, OpenCode
mcp: []
  # - name: filesystem
  #   command: npx
  #   args: ["-y", "@modelcontextprotocol/server-filesystem", "/home"]
  #   enabled: true

# Skills — point to SKILL.md files or directories
skills: []
  # - name: commit
  #   path: skills/commit
  #   enabled: true

# Permissions (Claude Code)
permissions:
  allow:
    - Bash(git *)
    - Read(*)
    - Write(*)
  deny: []

# Claude Code specific settings
claude:
  effortLevel: medium
  skipDangerousModePermissionPrompt: false

# Gemini CLI specific settings
gemini:
  extra: {}

# OpenCode specific settings
opencode:
  extra: {}
"""

PROJECT_CONFIG_TEMPLATE = """\
version: "1"
scope: project

# Project-level MCP servers (merged with global)
mcp: []

# Project-level skills (merged with global)
skills: []

# Project permissions override global
permissions:
  allow: []
  deny: []
"""


@click.group()
def main():
    """Coworker — unified AI dev environment for Claude Code, Gemini & OpenCode."""
    pass


@main.command()
@click.option("--global", "is_global", is_flag=True, default=False, help="Init global config")
@click.option("--project", "is_project", is_flag=True, default=False, help="Init project config in cwd")
def init(is_global, is_project):
    """Initialize global or project config."""
    if not is_global and not is_project:
        is_global = click.confirm("Init global config (~/.coworker/)?", default=True)
        if not is_global:
            is_project = True

    if is_global:
        GLOBAL_DIR.mkdir(parents=True, exist_ok=True)
        skills_dir = GLOBAL_DIR / "skills"
        skills_dir.mkdir(exist_ok=True)
        if GLOBAL_CONFIG.exists():
            console.print(f"[yellow]Already exists:[/yellow] {GLOBAL_CONFIG}")
        else:
            GLOBAL_CONFIG.write_text(GLOBAL_CONFIG_TEMPLATE)
            console.print(f"[green]Created:[/green] {GLOBAL_CONFIG}")
        console.print(f"[dim]Skills dir:[/dim] {skills_dir}")

    if is_project:
        project_config = Path.cwd() / PROJECT_CONFIG_NAME
        project_config.parent.mkdir(parents=True, exist_ok=True)
        if project_config.exists():
            console.print(f"[yellow]Already exists:[/yellow] {project_config}")
        else:
            project_config.write_text(PROJECT_CONFIG_TEMPLATE)
            console.print(f"[green]Created:[/green] {project_config}")


@main.command()
@click.option("--tool", type=click.Choice(["claude", "gemini", "opencode", "all"]), default="all")
@click.option("--project", "is_project", is_flag=True, default=False, help="Sync project-level config only")
@click.option("--global", "is_global", is_flag=True, default=False, help="Sync global config only")
def sync(tool, is_project, is_global):
    """Sync config to Claude Code, Gemini, and/or OpenCode."""
    config = merged_config()
    tools = list(ADAPTERS.keys()) if tool == "all" else [tool]

    project_dir = Path.cwd() if is_project else None

    for t in tools:
        adapter = ADAPTERS[t]
        console.print(f"\n[bold cyan]{t}[/bold cyan]")
        try:
            actions = adapter.sync(config, project_dir=project_dir)
            for action in actions:
                console.print(f"  [green]✓[/green] {action}")
        except Exception as e:
            console.print(f"  [red]✗ {e}[/red]")

    console.print("\n[bold green]Done.[/bold green]")


@main.command()
def status():
    """Show current config status."""
    table = Table(title="Coworker Config Status")
    table.add_column("Scope", style="cyan")
    table.add_column("Path")
    table.add_column("Status")
    table.add_column("MCPs")
    table.add_column("Skills")

    g = load_global_config()
    global_path = GLOBAL_CONFIG
    table.add_row(
        "global",
        str(global_path),
        "[green]found[/green]" if g else "[red]not found[/red]",
        str(len(g.mcp)) if g else "-",
        str(len(g.skills)) if g else "-",
    )

    p = load_project_config()
    from .config import find_project_config
    proj_path = find_project_config()
    table.add_row(
        "project",
        str(proj_path) if proj_path else "(none)",
        "[green]found[/green]" if p else "[dim]none[/dim]",
        str(len(p.mcp)) if p else "-",
        str(len(p.skills)) if p else "-",
    )

    console.print(table)


@main.group()
def skill():
    """Manage skills."""
    pass


@skill.command("list")
def skill_list():
    """List all skills."""
    config = merged_config()
    if not config.skills:
        console.print("[dim]No skills configured.[/dim]")
        return
    table = Table(title="Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Path")
    table.add_column("Enabled")
    for s in config.skills:
        table.add_row(s.name, s.path, "[green]yes[/green]" if s.enabled else "[red]no[/red]")
    console.print(table)


@skill.command("new")
@click.argument("name")
@click.option("--global", "is_global", is_flag=True, default=True)
def skill_new(name, is_global):
    """Scaffold a new skill."""
    if is_global:
        skill_dir = GLOBAL_DIR / "skills" / name
    else:
        skill_dir = Path.cwd() / ".coworker" / "skills" / name

    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists():
        console.print(f"[yellow]Already exists:[/yellow] {skill_file}")
        return

    skill_file.write_text(f"""\
---
name: {name}
description: "{name} skill — describe what this skill does and when to use it"
user-invocable: true
---

# {name}

## When to use
Describe when Claude should invoke this skill.

## Steps
1. Step one
2. Step two
3. Step three
""")
    console.print(f"[green]Created:[/green] {skill_file}")
    console.print(f"[dim]Add to coworker.yaml:[/dim]")
    console.print(f"  skills:\n    - name: {name}\n      path: skills/{name}")


@main.command()
@click.argument("package")
def install(package):
    """Install an MCP server package (npm/pip)."""
    console.print(f"Installing [cyan]{package}[/cyan]...")
    result = subprocess.run(
        ["npm", "install", "-g", package],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        console.print(f"[green]✓[/green] Installed {package}")
    else:
        console.print(f"[red]✗[/red] {result.stderr}")
        sys.exit(1)


@main.command("import-mcp")
@click.argument("mcp_file", default=".mcp.json", required=False)
@click.option("--dry-run", is_flag=True, default=False, help="Preview without writing")
def import_mcp(mcp_file, dry_run):
    """Import MCP servers from a .mcp.json file into coworker.yaml."""
    import json

    mcp_path = Path(mcp_file)
    if not mcp_path.is_absolute():
        mcp_path = Path.cwd() / mcp_path

    if not mcp_path.exists():
        console.print(f"[red]Not found:[/red] {mcp_path}")
        sys.exit(1)

    with open(mcp_path) as f:
        data = json.load(f)

    servers_raw = data.get("mcpServers", {})
    if not servers_raw:
        console.print("[yellow]No mcpServers found in file.[/yellow]")
        return

    from .models import McpServer
    new_servers = []
    for name, cfg in servers_raw.items():
        new_servers.append(McpServer(
            name=name,
            command=cfg.get("command", "npx"),
            args=cfg.get("args", []),
            env=cfg.get("env", {}),
            enabled=True,
        ))

    console.print(f"Found [cyan]{len(new_servers)}[/cyan] MCP server(s) in {mcp_path.name}:")
    for s in new_servers:
        console.print(f"  [dim]+[/dim] {s.name} ({s.command} {' '.join(s.args[:2])}...)")

    if dry_run:
        console.print("\n[yellow]Dry run — no changes written.[/yellow]")
        return

    # Merge into global coworker.yaml
    if not GLOBAL_CONFIG.exists():
        console.print(f"[red]Global config not found:[/red] {GLOBAL_CONFIG}")
        console.print("Run [cyan]coworker init --global[/cyan] first.")
        sys.exit(1)

    config = load_global_config()
    existing_names = {s.name for s in config.mcp}
    added = 0
    for server in new_servers:
        if server.name not in existing_names:
            config.mcp.append(server)
            added += 1
        else:
            # overwrite existing
            config.mcp = [server if s.name == server.name else s for s in config.mcp]

    save_config(config, GLOBAL_CONFIG)
    console.print(f"\n[green]✓[/green] Added/updated {len(new_servers)} server(s) in {GLOBAL_CONFIG}")
    console.print("Run [cyan]coworker sync[/cyan] to apply to all tools.")
