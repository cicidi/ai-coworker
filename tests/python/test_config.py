from __future__ import annotations
import importlib
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from coworker.models import ProjectEntry, ProjectCatalog, InitiativeConfig
import coworker.config as cfg


class TestProjectCatalogConfig:
    def test_load_empty(self, temp_coworker_dir):
        catalog = cfg.load_project_catalog()
        assert catalog.projects == []

    def test_save_and_load(self, temp_coworker_dir):
        catalog = ProjectCatalog(
            projects=[ProjectEntry(name="svc", local_path="/tmp/svc")]
        )
        cfg.save_project_catalog(catalog)
        loaded = cfg.load_project_catalog()
        assert len(loaded.projects) == 1
        assert loaded.projects[0].name == "svc"

    def test_overwrite(self, temp_coworker_dir):
        catalog = ProjectCatalog(
            projects=[ProjectEntry(name="old", local_path="/tmp/old")]
        )
        cfg.save_project_catalog(catalog)
        catalog.projects = [
            ProjectEntry(name="new", local_path="/tmp/new")
        ]
        cfg.save_project_catalog(catalog)
        loaded = cfg.load_project_catalog()
        assert loaded.projects[0].name == "new"


class TestInitiativeConfig:
    def test_save_and_load(self, temp_initiatives_dir):
        cfg.save_initiative(
            InitiativeConfig(name="test-init", description="Test"),
        )
        loaded = cfg.load_initiative("test-init")
        assert loaded is not None
        assert loaded.name == "test-init"
        assert loaded.description == "Test"

    def test_initiative_exists(self, temp_initiatives_dir):
        assert not cfg.initiative_exists("test-init")
        cfg.save_initiative(InitiativeConfig(name="test-init"))
        assert cfg.initiative_exists("test-init")

    def test_list_initiatives(self, temp_initiatives_dir):
        cfg.save_initiative(InitiativeConfig(name="init-a"))
        cfg.save_initiative(InitiativeConfig(name="init-b"))
        results = cfg.list_initiatives()
        assert len(results) == 2
        names = {i.name for i in results}
        assert names == {"init-a", "init-b"}

    def test_load_nonexistent(self, temp_initiatives_dir):
        assert cfg.load_initiative("does-not-exist") is None
