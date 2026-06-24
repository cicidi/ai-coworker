from __future__ import annotations
from pathlib import Path
import yaml
from click.testing import CliRunner

from coworker.cli import main


runner = CliRunner()


class TestVersion:
    def test_version_matches_pyproject(self):
        import tomllib

        root = Path(__file__).parent.parent.parent
        pyproject = root / "pyproject.toml"
        data = tomllib.loads(pyproject.read_text())
        version = data["project"]["version"]
        assert version == "0.1.0"


class TestStatus:
    def test_status(self):
        result = runner.invoke(main, ["status"])
        assert result.exit_code == 0


class TestInitHelp:
    def test_init_help(self):
        result = runner.invoke(main, ["init", "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output or "usage:" in result.output
        assert "init" in result.output.lower()


class TestSyncHelp:
    def test_sync_help(self):
        result = runner.invoke(main, ["sync", "--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output or "usage:" in result.output
        assert "sync" in result.output.lower()


class TestProjectList:
    def test_project_list(self):
        result = runner.invoke(main, ["project", "list"])
        assert result.exit_code == 0
        # Output should either show a table header or "No projects" message
        output_lower = result.output.lower()
        has_table_or_msg = (
            "project catalog" in output_lower
            or "no projects" in output_lower
            or "project" in output_lower
        )
        assert has_table_or_msg, f"Unexpected output: {result.output}"


class TestConfigConventions:
    def test_local_config_exists(self):
        config_path = Path(__file__).parent.parent.parent / ".local_config.yaml"
        assert config_path.exists(), f"{config_path} does not exist"

    def test_local_config_valid_yaml(self):
        config_path = Path(__file__).parent.parent.parent / ".local_config.yaml"
        content = config_path.read_text()
        data = yaml.safe_load(content)
        assert data is not None, "YAML file is empty or invalid"

    def test_local_config_has_required_keys(self):
        config_path = Path(__file__).parent.parent.parent / ".local_config.yaml"
        data = yaml.safe_load(config_path.read_text())
        assert "identity" in data, "Missing 'identity' section"
        identity = data["identity"]
        assert "username" in identity, "Missing identity.username"
        assert "project" in identity, "Missing identity.project"
        assert identity["username"] != "", "username must not be empty"
        assert identity["project"] != "", "project must not be empty"

    def test_local_config_docs_section_valid(self):
        config_path = Path(__file__).parent.parent.parent / ".local_config.yaml"
        data = yaml.safe_load(config_path.read_text())
        if "docs" in data:
            docs = data["docs"]
            root = Path(__file__).parent.parent.parent
            if "prd" in docs:
                prd_path = root / docs["prd"]
                assert prd_path.exists(), f"PRD path not found: {prd_path}"
            if "feature" in docs:
                feature_path = root / docs["feature"]
                assert feature_path.exists(), f"Feature path not found: {feature_path}"

    def test_local_config_github_section(self):
        config_path = Path(__file__).parent.parent.parent / ".local_config.yaml"
        data = yaml.safe_load(config_path.read_text())
        assert "github" in data, "Missing 'github' section"
        assert "repo" in data["github"], "Missing github.repo"
        assert data["github"]["repo"] == "cicidi/ai-coworker"


class TestSkillReferences:
    def test_skill_references_valid(self):
        root = Path(__file__).parent.parent.parent
        claude_md = root / "CLAUDE.md"
        content = claude_md.read_text()

        skill_names = set()
        for line in content.splitlines():
            if "skill-create" in line:
                skill_names.add("skill-create")
            if "skill-edit" in line:
                skill_names.add("skill-edit")
            if "self-heal" in line:
                skill_names.add("self-heal")
            if "self-analyze" in line:
                skill_names.add("self-analyze")

        assert len(skill_names) > 0, "No skill references found in CLAUDE.md"

        skills_dir = root / "skills"
        skill_factory_skills = (
            Path.home() / ".config/opencode/skills/skill-factory/ai-coworker-skills"
        )
        skill_factory_personal = (
            Path.home() / ".config/opencode/skills/skill-factory/personal-skills"
        )

        for skill_name in skill_names:
            found = False

            # Check project-local skills/
            if (skills_dir / skill_name / "SKILL.md").exists():
                found = True

            # Check skill-factory source
            if not found and (skill_factory_skills / skill_name / "SKILL.md").exists():
                found = True
            if not found and (skill_factory_personal / skill_name / "SKILL.md").exists():
                found = True

            # Check for imported skills
            import_skills = Path.home() / ".config/opencode/skills/skill-factory/import-skills"
            if not found and (import_skills / skill_name / "SKILL.md").exists():
                found = True

            assert found, (
                f"Skill '{skill_name}' referenced in CLAUDE.md not found "
                f"in project skills/ or skill-factory"
            )
