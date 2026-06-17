from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from coworker.models import (
    InitiativeConfig,
    InitiativeProjectRef,
    Decision,
    LinkRef,
    ReferenceDoc,
    ProjectCatalog,
    ProjectEntry,
    KnowledgePoolEntry,
    Refs,
    GitHubRef,
    SlackRef,
)
from coworker.adapters.claude import (
    _build_static_block,
    _build_initiative_block,
    _remove_all_initiative_blocks,
    _replace_or_append_block,
    STATIC_START,
    STATIC_END,
)

ASSERT = True


class TestStaticBlock:
    def test_empty_catalog(self):
        catalog = ProjectCatalog()
        block = _build_static_block(catalog)
        assert STATIC_START in block
        assert STATIC_END in block
        assert "(no projects configured)" in block

    def test_catalog_with_projects(self):
        catalog = ProjectCatalog(
            projects=[
                ProjectEntry(
                    name="auth-service",
                    local_path="/tmp/auth",
                    upstream=[],
                    downstream=[],
                )
            ]
        )
        block = _build_static_block(catalog)
        assert "auth-service" in block
        assert "/tmp/auth" in block

    def test_catalog_with_knowledge_pools(self):
        catalog = ProjectCatalog(
            projects=[
                ProjectEntry(
                    name="svc",
                    local_path="/tmp/svc",
                    knowledge_pool=[
                        KnowledgePoolEntry(
                            url="https://wiki", type="confluence"
                        )
                    ],
                )
            ]
        )
        block = _build_static_block(catalog)
        assert "confluence" in block
        assert "wiki" in block

    def test_catalog_with_refs(self):
        catalog = ProjectCatalog(
            projects=[
                ProjectEntry(
                    name="svc",
                    local_path="/tmp/svc",
                    refs=Refs(
                        github=[GitHubRef(owner="org", repo="svc")],
                        slack=[SlackRef(channel="#svc", id="C123")],
                    ),
                )
            ]
        )
        block = _build_static_block(catalog)
        assert "org/svc" in block
        assert "#svc" in block

    def test_block_replacement(self):
        old = (
            "---\nold content\n<!-- COWORKER:STATIC START -->\n"
            "old block\n<!-- COWORKER:STATIC END -->\nmore\n"
        )
        new_block = "<!-- COWORKER:STATIC START -->\nnew block\n<!-- COWORKER:STATIC END -->\n"
        result = _replace_or_append_block(
            old, STATIC_START, STATIC_END, new_block
        )
        assert "new block" in result
        assert "old content" in result
        assert "old block" not in result
        assert "more" in result

    def test_block_appended_when_missing(self):
        content = "# Title\n\n## Section\n"
        new_block = "<!-- COWORKER:STATIC START -->\nblock\n<!-- COWORKER:STATIC END -->\n"
        result = _replace_or_append_block(
            content, STATIC_START, STATIC_END, new_block
        )
        assert "# Title" in result
        assert "block" in result

    def test_static_block_has_docs_directory_structure(self):
        catalog = ProjectCatalog()
        block = _build_static_block(catalog)
        assert "## Docs Directory Structure" in block
        assert "docs/" in block
        assert "docs/architecture/" in block
        assert "docs/spec/" in block
        assert "docs/planning/" in block

    def test_static_block_has_coworker_skills_guidance(self):
        catalog = ProjectCatalog()
        block = _build_static_block(catalog)
        assert "## Coworker Skills" in block
        assert "coworker-dev-*" in block
        assert "coworker-do-*" in block
        assert "coworker-debug-*" in block
        assert "Prefer coworker skills" in block

    def test_static_block_has_karpathy_guidelines(self):
        catalog = ProjectCatalog()
        block = _build_static_block(catalog)
        assert "## Additional Behavioral Guidelines" in block
        assert "andrej-karpathy-skills" in block
        assert "Think Before Coding" in block
        assert "Simplicity First" in block
        assert "Surgical Changes" in block
        assert "Goal-Driven Execution" in block
        assert "fewer unnecessary diffs" in block


class TestInitiativeBlock:
    def test_minimal_initiative(self):
        config = InitiativeConfig(name="test")
        block = _build_initiative_block(config)
        assert "<!-- INITIATIVE:test START -->" in block
        assert "<!-- INITIATIVE:test END -->" in block
        assert "## Active Initiative: test" in block

    def test_full_initiative(self):
        config = InitiativeConfig(
            name="auth-migration",
            description="Migrate auth",
            projects=[
                InitiativeProjectRef(
                    name="auth-service",
                    role="upstream",
                    branches=["main", "feat/oauth2"],
                )
            ],
            decisions=[
                Decision(
                    date="2026-06-01",
                    decision="Use OAuth2",
                    rationale="Standard",
                    by="cicidi",
                )
            ],
            links=[LinkRef(url="https://wiki", title="Design Doc")],
            reference_docs=[
                ReferenceDoc(path="~/docs/spec.md", title="Spec")
            ],
        )
        block = _build_initiative_block(config)
        assert "Migrate auth" in block
        assert "auth-service" in block
        assert "upstream" in block
        assert "feat/oauth2" in block
        assert "Use OAuth2" in block
        assert "cicidi" in block
        assert "Design Doc" in block
        assert "Spec" in block


class TestRemoveInitiativeBlocks:
    def test_remove_single_block(self):
        content = (
            "# My Project\n\n"
            "<!-- INITIATIVE:test START -->\n"
            "## Active Initiative: test\n"
            "<!-- INITIATIVE:test END -->\n\n"
            "## End\n"
        )
        result = _remove_all_initiative_blocks(content)
        assert "INITIATIVE" not in result
        assert "# My Project" in result
        assert "## End" in result

    def test_remove_multiple_blocks(self):
        content = (
            "start\n"
            "<!-- INITIATIVE:a START -->\nblock a\n<!-- INITIATIVE:a END -->\n"
            "middle\n"
            "<!-- INITIATIVE:b START -->\nblock b\n<!-- INITIATIVE:b END -->\n"
            "end\n"
        )
        result = _remove_all_initiative_blocks(content)
        assert "INITIATIVE" not in result
        assert "start" in result
        assert "middle" in result
        assert "end" in result

    def test_no_blocks_unchanged(self):
        content = "# My Project\n\n## No initiatives\n"
        result = _remove_all_initiative_blocks(content)
        assert result.strip() == content.strip()
