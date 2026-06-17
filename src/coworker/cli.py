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
    load_global_config, load_project_config, merged_config, save_config,
    load_project_catalog, save_project_catalog,
    load_initiative, save_initiative, list_initiatives, initiative_exists,
)
from .models import (
    CoworkerConfig, ProjectEntry, ProjectRef, ProjectCatalog,
    InitiativeConfig, InitiativeProjectRef, LinkRef, Decision, ReferenceDoc,
    KnowledgePoolEntry,
)
from .adapters import ADAPTERS
from .initiatives.manager import InitiativeManager

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


# ── Project Catalog ───────────────────────────────────────────────────────


@main.group()
def project():
    """Manage project catalog (project.yaml)."""
    pass


@project.command("list")
def project_list():
    """List all tracked projects."""
    catalog = load_project_catalog()
    if not catalog.projects:
        console.print(
            "[dim]No projects configured. Use 'coworker project add'.[/dim]"
        )
        return
    table = Table(title="Project Catalog")
    table.add_column("Name", style="cyan")
    table.add_column("Path")
    table.add_column("Upstream")
    table.add_column("Downstream")
    for p in catalog.projects:
        up = ", ".join(u.name for u in p.upstream) or "-"
        down = ", ".join(d.name for d in p.downstream) or "-"
        table.add_row(p.name, p.local_path, up, down)
    console.print(table)


@project.command("show")
@click.argument("name")
def project_show(name):
    """Show details of a single project."""
    catalog = load_project_catalog()
    for p in catalog.projects:
        if p.name == name:
            import yaml
            data = p.model_dump(exclude_none=True)
            console.print(
                yaml.dump(data, default_flow_style=False, allow_unicode=True)
            )
            return
    console.print(f"[red]Project '{name}' not found.[/red]")


@project.command("add")
@click.argument("name")
@click.option("--path", "local_path", default=None, help="Local directory")
@click.option("--repo", default=None, help="Git remote URL")
@click.option("--team", default=None, help="Owning team")
def project_add(name, local_path, repo, team):
    """Add a project to the catalog."""
    catalog = load_project_catalog()
    for p in catalog.projects:
        if p.name == name:
            console.print(f"[yellow]Project '{name}' already exists.[/yellow]")
            return

    entry = ProjectEntry(
        name=name,
        local_path=local_path or str(Path.cwd()),
        repo=repo or "",
        team=team or "",
    )
    catalog.projects.append(entry)
    save_project_catalog(catalog)
    console.print(f"[green]Added project '{name}' to catalog.[/green]")


@project.command("edit")
@click.argument("name")
@click.option("--path", "local_path", default=None)
@click.option("--repo", default=None)
@click.option(
    "--add-upstream", multiple=True, help="Add upstream project name"
)
@click.option(
    "--add-downstream", multiple=True, help="Add downstream project name"
)
@click.option("--add-kp-url", "kp_url", default=None)
@click.option("--add-kp-type", "kp_type", default="other")
def project_edit(
    name, local_path, repo, add_upstream, add_downstream, kp_url, kp_type
):
    """Edit a project entry."""
    catalog = load_project_catalog()
    for p in catalog.projects:
        if p.name == name:
            if local_path:
                p.local_path = local_path
            if repo:
                p.repo = repo
            for up in add_upstream:
                if not any(u.name == up for u in p.upstream):
                    p.upstream.append(ProjectRef(name=up))
            for down in add_downstream:
                if not any(d.name == down for d in p.downstream):
                    p.downstream.append(ProjectRef(name=down))
            if kp_url:
                p.knowledge_pool.append(
                    KnowledgePoolEntry(url=kp_url, type=kp_type)
                )
            save_project_catalog(catalog)
            console.print(f"[green]Updated project '{name}'.[/green]")
            return
    console.print(f"[red]Project '{name}' not found.[/red]")


@project.command("remove")
@click.argument("name")
def project_remove(name):
    """Remove a project from the catalog."""
    catalog = load_project_catalog()
    before = len(catalog.projects)
    catalog.projects = [p for p in catalog.projects if p.name != name]
    if len(catalog.projects) == before:
        console.print(f"[yellow]Project '{name}' not found.[/yellow]")
        return
    save_project_catalog(catalog)
    console.print(f"[green]Removed project '{name}'.[/green]")


@project.command("sync")
def project_sync():
    """Re-inject static context into IDE configs."""
    mgr = InitiativeManager()
    actions = mgr.inject_static_context()
    for action in actions:
        console.print(f"  [green]✓[/green] {action}")
    console.print("[bold green]Static context synced.[/bold green]")


# ── Initiative ─────────────────────────────────────────────────────────────


@main.group()
def initiative():
    """Manage initiatives."""
    pass


@initiative.command("start")
@click.argument("name")
@click.option("--description", "-d", default="")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
@click.option("--role", default="peer", help="Project role: upstream|downstream|peer")
@click.option("--branch", "-b", "branches", default="main", help="Branches (comma-separated)")
def initiative_start(name, description, proj_dir, role, branches):
    """Quick-start: create, add project, and activate in one step."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    mgr = InitiativeManager(project_dir=pd)

    try:
        mgr.create(name, description)
    except FileExistsError:
        console.print(f"[yellow]Initiative '{name}' exists, activating it.[/yellow]")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        return

    if proj_dir:
        config = load_initiative(name, project_dir=pd)
        if config and not any(p.name == proj_dir for p in config.projects):
            branch_list = [b.strip() for b in branches.split(",") if b.strip()]
            config.projects.append(
                InitiativeProjectRef(
                    name=proj_dir,
                    role=role,
                    branches=branch_list,
                )
            )
            save_initiative(config, project_dir=pd)

    try:
        actions = mgr.activate(name)
        for action in actions:
            console.print(f"  [green]✓[/green] {action}")
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")


@initiative.command("create")
@click.argument("name")
@click.option("--description", "-d", default="")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
def initiative_create(name, description, proj_dir):
    """Create a new initiative."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    mgr = InitiativeManager(project_dir=pd)
    try:
        mgr.create(name, description)
        console.print(f"[green]Created initiative '{name}' in {pd}[/green]")
    except FileExistsError as e:
        console.print(f"[red]{e}[/red]")


@initiative.command("edit")
@click.argument("name")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
@click.option("--description", "-d", default=None)
@click.option("--add-project", "add_proj", default=None, help="Add project (name:role:branches)")
@click.option("--add-link", "add_link_spec", default=None, help="Add link (Title|URL)")
@click.option("--add-decision", "add_decision_spec", default=None, help="Add decision (date|decision|rationale|by)")
@click.option("--add-doc", "add_doc_spec", default=None, help="Add reference doc (Title|path)")
@click.option("--archive", "do_archive", is_flag=True, default=False, help="Archive the initiative")
def initiative_edit(name, proj_dir, description, add_proj, add_link_spec, add_decision_spec, add_doc_spec, do_archive):
    """Edit an existing initiative."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    config = load_initiative(name, project_dir=pd)
    if config is None:
        console.print(f"[red]Initiative '{name}' not found.[/red]")
        return

    if description is not None:
        config.description = description
    if do_archive:
        config.status = "archived"

    if add_proj:
        parts = add_proj.split(":")
        proj_name = parts[0]
        existing = [p for p in config.projects if p.name == proj_name]
        if existing:
            console.print(
                f"[yellow]Project '{proj_name}' is already in this initiative.[/yellow]"
            )
            return
        proj = InitiativeProjectRef(
            name=proj_name,
            role=parts[1] if len(parts) > 1 else "peer",
            branches=(
                parts[2].split(",") if len(parts) > 2 and parts[2] else []
            ),
        )
        config.projects.append(proj)

    if add_link_spec:
        parts = add_link_spec.split("|", 1)
        config.links.append(
            LinkRef(
                title=parts[0],
                url=parts[1] if len(parts) > 1 else parts[0],
            )
        )

    if add_decision_spec:
        parts = add_decision_spec.split("|")
        config.decisions.append(
            Decision(
                date=parts[0] if len(parts) > 0 else "",
                decision=parts[1] if len(parts) > 1 else "",
                rationale=parts[2] if len(parts) > 2 else "",
                by=parts[3] if len(parts) > 3 else "",
            )
        )

    if add_doc_spec:
        parts = add_doc_spec.split("|", 1)
        config.reference_docs.append(
            ReferenceDoc(
                title=parts[0],
                path=parts[1] if len(parts) > 1 else parts[0],
            )
        )

    save_initiative(config, project_dir=pd)
    console.print(f"[green]Updated initiative '{name}'.[/green]")


@initiative.command("list")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
@click.option("--verbose", "-v", is_flag=True, default=False)
def initiative_list(proj_dir, verbose):
    """List all initiatives for a project."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    mgr = InitiativeManager(project_dir=pd)
    active = mgr.active_name()
    initiatives = mgr.list_all()
    if not initiatives:
        console.print(f"[dim]No initiatives in {pd}. Use 'coworker initiative create'.[/dim]")
        return

    table = Table(title=f"Initiatives ({pd})")
    table.add_column("Name", style="cyan")
    table.add_column("Status")
    table.add_column("Active")
    if verbose:
        table.add_column("Projects")
    table.add_column("Description")
    for i in initiatives:
        mark = "[green]✓[/green]" if i.name == active else ""
        sc = "green" if i.status == "active" else "dim"
        row = [i.name, f"[{sc}]{i.status}[/{sc}]", mark]
        if verbose:
            proj_str = ", ".join(p.name for p in i.projects) or "-"
            row.append(proj_str)
        row.append(i.description or "-")
        table.add_row(*row)
    console.print(table)


@initiative.command("show")
@click.argument("name")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
def initiative_show(name, proj_dir):
    """Show full initiative config."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    config = load_initiative(name, project_dir=pd)
    if config is None:
        console.print(f"[red]Initiative '{name}' not found.[/red]")
        return
    import yaml
    data = config.model_dump(exclude_none=True)
    console.print(yaml.dump(data, default_flow_style=False, allow_unicode=True))


@initiative.command("activate")
@click.argument("name")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
def initiative_activate(name, proj_dir):
    """Activate an initiative (inject context into IDE configs)."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    mgr = InitiativeManager(project_dir=pd)
    try:
        actions = mgr.activate(name)
        for action in actions:
            console.print(f"  [green]✓[/green] {action}")
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")


@initiative.command("deactivate")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
def initiative_deactivate(proj_dir):
    """Deactivate current initiative."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    mgr = InitiativeManager(project_dir=pd)
    actions = mgr.deactivate()
    for action in actions:
        console.print(f"  [green]✓[/green] {action}")


@initiative.command("remove")
@click.argument("name")
@click.option("--project", "-p", "proj_dir", default=None, help="Project directory (default: current)")
@click.option("--force", is_flag=True, default=False, help="Skip confirmation")
def initiative_remove(name, proj_dir, force):
    """Remove an initiative permanently."""
    pd = Path(proj_dir) if proj_dir else Path.cwd()
    mgr = InitiativeManager(project_dir=pd)
    config = mgr.show(name)
    if config is None:
        console.print(f"[red]Initiative '{name}' not found.[/red]")
        return
    if not force:
        ok = click.confirm(f"Remove initiative '{name}' permanently?", default=False)
        if not ok:
            console.print("[dim]Cancelled.[/dim]")
            return
    try:
        mgr.remove(name)
        console.print(f"[green]Removed initiative '{name}'.[/green]")
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")


# ── Analytics & Dashboard (top-level) ────────────────────────────────────

@initiative.command("analytics-db-init")
def analytics_db_init():
    """Initialize analytics SQLite database."""
    from .analytics.db import init_db
    init_db()
    console.print("[green]Analytics database initialized.[/green]")


@initiative.command("analytics-import")
def analytics_import():
    """Import raw JSONL sessions into SQLite."""
    from .analytics.import_data import import_all
    import_all()


@initiative.command("dashboard")
@click.option("--port", default=8080, help="Port to listen on")
@click.option("--db", default=None, help="Path to analytics database")
def dashboard_serve(port, db):
    """Start the analytics dashboard."""
    import os
    if db:
        os.environ["COWORKER_ANALYTICS_DB"] = db
    import uvicorn
    from .dashboard.app import app
    console.print(f"[green]Dashboard: http://localhost:{port}[/green]")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
