---
name: coworker-gate-tests
triggers:
  - verify tests
  - check unit tests
  - run test verification
  - 3-level test check
description: |
  3-level test verification: structural/frontmatter → content quality → dry-run
  before commit. Ensures tests exist, are meaningful, and pass before pushing.
services:
  category: coworker-do
when_to_use: |
  Before every commit that includes new functions or classes. When user asks
  to "verify tests" or "make sure tests are good".
when_not_to_use: |
  Skip for documentation-only changes or config tweaks with no logic.
version: 1.0.0
---

# Unit Tests (Auto-Applied)

3-level verification before every commit.

## Level 1 — Structural Check
Verify test files exist and are properly structured:
```
→ For each new/modified source file:
  → Is there a corresponding test file?
  → Does test file have at least 1 test function?
  → Are test functions named descriptively?

Pass: all source files have test coverage
Fail: list files missing tests → block commit
```

## Level 2 — Content Quality
Review test quality (don't run, just read):
```
→ Each test has: Arrange / Act / Assert structure
→ Tests are not trivially passing (no `assert True`)
→ At least one negative/error case per feature
→ No time-dependent tests (no `sleep()`, fixed timestamps)
→ No tests calling external services without mocking
```

## Level 3 — Dry Run
Actually run the tests:
```bash
# Auto-detect test framework and run
python: pytest {changed_files_test_paths} -v
node:   npx jest --testPathPattern={pattern} --verbose
java:   mvn test -pl {module}
go:     go test ./...
rust:   cargo test
```

### On Failure
```
❌ Tests failed:
{test output}

→ Fix tests before committing? (y/n)
→ If no: commit anyway? (requires explicit confirmation)
```

### On Success
```
✅ Tests passed: {N} tests, {N} passed, {coverage}%
→ Proceeding with commit
```

## Skip Conditions
Tests can be skipped for:
- `docs:` commits (markdown-only changes)
- `chore:` commits (dependency updates, config)
Must be explicitly stated: `git commit -m "chore: ... [skip-tests]"`
