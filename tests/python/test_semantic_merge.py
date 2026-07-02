# tests/python/test_semantic_merge.py
from coworker.semantic_merge import (
    classify_sections,
    apply_merge,
    OVERWRITE,
    MERGE_ADD,
    KEEP,
)

CURRENT = """# Project CLAUDE.md

## Identity
python, fastapi

## My Custom Rules
my custom content

<!-- PROTECTED -->
do not touch
<!-- END PROTECTED -->

## Context Management
old version
"""

FUTURE = """# Project CLAUDE.md

## Identity
python, fastapi, pydantic

## Context Management
new version

## Workflow Heuristics
new workflow guide
"""


class TestClassifySections:
    def test_overwrite_identity(self):
        c = classify_sections(CURRENT, FUTURE)
        identity = [x for x in c if x.category == OVERWRITE and "Identity" in x.heading]
        assert len(identity) == 1

    def test_overwrite_context_mgmt(self):
        c = classify_sections(CURRENT, FUTURE)
        ctx = [x for x in c if x.category == OVERWRITE and "Context Management" in x.heading]
        assert len(ctx) == 1

    def test_keep_custom_rules(self):
        c = classify_sections(CURRENT, FUTURE)
        keeps = [x for x in c if x.category == KEEP]
        headings = [x.heading for x in keeps]
        assert any("Custom Rules" in h for h in headings)

    def test_merge_add_workflow(self):
        c = classify_sections(CURRENT, FUTURE)
        adds = [x for x in c if x.category == MERGE_ADD]
        assert any("Workflow Heuristics" in x.heading for x in adds)

    def test_protected_block_kept(self):
        c = classify_sections(CURRENT, FUTURE)
        protected = [x for x in c if "PROTECTED" in x.current_content]
        assert len(protected) >= 1
        assert protected[0].category == KEEP


class TestApplyMerge:
    def test_merged_contains_overwrite(self):
        c = classify_sections(CURRENT, FUTURE)
        result = apply_merge(c, CURRENT, FUTURE)
        assert "pydantic" in result
        assert "new version" in result

    def test_merged_keeps_custom(self):
        c = classify_sections(CURRENT, FUTURE)
        result = apply_merge(c, CURRENT, FUTURE)
        assert "my custom content" in result

    def test_merged_adds_new_sections(self):
        c = classify_sections(CURRENT, FUTURE)
        result = apply_merge(c, CURRENT, FUTURE)
        assert "new workflow guide" in result

    def test_merged_keeps_protected(self):
        c = classify_sections(CURRENT, FUTURE)
        result = apply_merge(c, CURRENT, FUTURE)
        assert "do not touch" in result

    def test_no_duplicate_headings(self):
        c = classify_sections(CURRENT, FUTURE)
        result = apply_merge(c, CURRENT, FUTURE)
        assert result.count("## Identity") == 1
