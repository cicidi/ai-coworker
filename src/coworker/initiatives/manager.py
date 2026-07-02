from __future__ import annotations
import re
from datetime import datetime
from pathlib import Path

from ..config import (
    GLOBAL_DIR,
    INITIATIVES_DIR,
    load_initiative,
    save_initiative,
    list_initiatives,
    initiative_exists,
)
from ..models import (
    InitiativeConfig,
    InitiativeProjectRef,
)
from ..adapters.claude import inject_initiative, remove_initiative
from ..adapters.opencode import (
    inject_initiative as opencode_inject,
    remove_initiative as opencode_remove,
)

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

ACTIVE_MARKER = INITIATIVES_DIR / ".active"


class InitiativeManager:

    def __init__(self, project_dir: Path | None = None):
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

    # ── CRUD ────────────────────────────────────────────────────────────

    def create(self, name: str, description: str = "") -> InitiativeConfig:
        if initiative_exists(name):
            raise FileExistsError(f"Initiative '{name}' already exists.")
        if not KEBAB_RE.match(name):
            raise ValueError(f"Name '{name}' must be kebab-case (e.g. 'auth-migration').")

        config = InitiativeConfig(
            name=name,
            description=description,
            status="active",
            created=datetime.now().strftime("%Y-%m-%d"),
        )
        save_initiative(config)
        return config

    def edit(self, name: str, **updates) -> InitiativeConfig:
        config = load_initiative(name)
        if config is None:
            raise FileNotFoundError(f"Initiative '{name}' not found.")

        for key, value in updates.items():
            if hasattr(config, key):
                setattr(config, key, value)

        save_initiative(config)
        return config

    def show(self, name: str) -> InitiativeConfig | None:
        return load_initiative(name)

    def list_all(self) -> list[InitiativeConfig]:
        return list_initiatives()

    def remove(self, name: str) -> None:
        if not initiative_exists(name):
            raise FileNotFoundError(f"Initiative '{name}' not found.")

        if self.active_name() == name:
            self.deactivate()

        path = INITIATIVES_DIR / f"{name}.yaml"
        path.unlink()

    # ── Activation ──────────────────────────────────────────────────────

    def activate(self, name: str) -> list[str]:
        config = load_initiative(name)
        if config is None:
            raise FileNotFoundError(f"Initiative '{name}' not found.")

        actions = []
        self.deactivate()

        for injector in [inject_initiative, opencode_inject]:
            try:
                actions += injector(config, project_dir=self.project_dir)
            except Exception:
                pass

        ACTIVE_MARKER.write_text(name)
        actions.append(f"Activated initiative '{name}'")
        return actions

    def deactivate(self) -> list[str]:
        actions = []
        had_effect = False

        for remover in [remove_initiative, opencode_remove]:
            try:
                result = remover(project_dir=self.project_dir)
                for r in result:
                    if "removed" in r:
                        had_effect = True
                    actions.append(r)
            except Exception:
                pass

        if ACTIVE_MARKER.exists():
            ACTIVE_MARKER.unlink()

        if had_effect:
            actions.append("Deactivated current initiative")
        else:
            actions.append("No active initiative")
        return actions

    def active_name(self) -> str | None:
        if ACTIVE_MARKER.exists():
            return ACTIVE_MARKER.read_text().strip()
        return None

    def archive(self, name: str) -> InitiativeConfig:
        return self.edit(name, status="archived")

    def inject_static_context(self) -> list[str]:
        from ..config import load_project_catalog
        from ..adapters.claude import inject_static_context
        from ..adapters.opencode import inject_static_context as opencode_static

        catalog = load_project_catalog()
        actions = []
        for injector in [inject_static_context, opencode_static]:
            try:
                actions += injector(catalog, project_dir=self.project_dir)
            except Exception:
                pass
        return actions
