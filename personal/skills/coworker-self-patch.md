---
name: coworker-self-patch
triggers:
  - fix grammar
  - auto-correct response
  - patch english errors
description: |
  Auto-correct minor English grammar errors in AI responses for non-native speakers.
  Applies transparently on every response without user prompting.
services:
  category: coworker-meta
when_to_use: |
  When any AI response contains grammar errors. Auto-applied silently.
when_not_to_use: |
  Do not apply to code, config files, or quoted user text.
version: 1.0.0
---

# Auto Patches

Automatically corrects minor English grammar and phrasing errors in AI-written content
(comments, commit messages, PR descriptions, docs).

## What It Fixes

### Grammar
- Subject-verb agreement: "The functions are..." not "The functions is..."
- Article usage: "a function" vs "an error"
- Tense consistency within a sentence
- Plural/singular consistency

### Common Technical Writing Errors
- "it's" vs "its"
- "affect" vs "effect"
- "which" vs "that" in relative clauses
- Missing Oxford comma (standardize to include)

### Commit Message Style
- Ensure imperative mood: "Add feature" not "Added feature"
- Conventional commits format: `type(scope): description`
- Max 72 chars for subject line

## How It Works

Corrections are applied inline — the corrected version replaces the original without comment.

Minor corrections (grammar): applied silently.
Style changes (phrasing, structure): shown in *italics* with the original for review.

## What It Does NOT Change
- Technical terminology
- Variable/function names
- Code comments that are intentionally terse
- Language that is correct but informal

## Trigger
Run manually: `/auto-patches` on a specific piece of text
Or apply to: commit messages, PR descriptions, doc sections before publishing.
