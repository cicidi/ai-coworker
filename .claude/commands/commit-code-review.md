---
name: code-review
description: Auto pre-commit code review against known anti-patterns. Self-improving via self-healing.
aliases: [review-code, pre-commit-review]
---

# Code Review (Auto-Applied)

Runs before every commit. Reviews against known anti-patterns, language best practices, and self-healing rules.

## Review Checklist

### Correctness
- [ ] Logic is correct — no off-by-one errors, wrong conditions, inverted booleans
- [ ] Edge cases handled: null/empty inputs, empty collections, zero values
- [ ] Error handling present for all failure paths
- [ ] No infinite loops or missing break conditions

### Code Quality
- [ ] Functions have single responsibility
- [ ] No functions longer than ~50 lines (flag, don't block)
- [ ] No deeply nested conditions (>3 levels — suggest early return)
- [ ] No duplicate code blocks (>5 lines repeated — suggest extraction)
- [ ] Variable names are descriptive — no single letters except loop indices

### Tests
- [ ] New public functions have at least one test
- [ ] Tests cover happy path AND at least one error case
- [ ] No tests that always pass regardless of implementation
- [ ] Test names describe behavior: `test_returns_404_when_user_not_found()`

### Dependencies
- [ ] No new dependencies added without explicit user confirmation
- [ ] No unused imports

### Language-Specific (auto-detect language)
**Python:** type hints on function signatures, f-strings not %-format, no bare `except:`
**TypeScript:** no `any` types without justification, proper async/await (no `.then()` chains)
**Java:** no raw types, resources closed in try-with-resources, no `System.out.println` in production
**Go:** errors checked (not `_`), no naked returns in long functions
**Rust:** no `unwrap()` in production paths without comment explaining why safe

## Output Format
```
Code Review Summary:
✅ No critical issues
⚠️  Warnings (non-blocking):
  - line 42: function `processData` is 80 lines — consider splitting
  - line 67: missing test for error case
❌ Blockers (must fix before commit):
  - line 15: bare except clause catches all exceptions
```

## Self-Improving
New anti-patterns discovered via self-healing traces are automatically added to this review checklist.
