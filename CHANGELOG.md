# Changelog

## 2026-06-24 — Review & Testing Update

### Fixes
- Fixed broken references in CLAUDE.md to non-existent `templates/team-common/` paths

### Tests
- Added `tests/python/test_cli.py` — 11 CLI tests (version, status, help, project list, config validation, skill references)
- Added `tests/python/test_skill_factory_integration.py` — 11 integration tests (source repo validation, deploy consistency, CLAUDE.md references)
- All 33+ existing tests still pass; 22 new tests added

### Documentation
- Updated README with testing instructions and skill management workflow
