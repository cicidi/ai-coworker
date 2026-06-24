---
name: self-strain
description: Train AI on specific patterns through self-iteration — extract failure patterns and update skills
aliases: [train, improve-skill]
---

# Strain Sites (AI Self-Improvement)

Targeted self-improvement on a specific pattern or behavior. Unlike self-healing-analyze (reactive),
this is proactive training on identified weak areas.

## When to Use
- AI keeps making same mistake despite trace logs
- You want to pre-emptively train on a known edge case
- You want to improve AI quality on a specific codebase pattern

## Process

### 1. Define the Strain Site
```
→ Ask: "What behavior do you want to improve?"
→ Examples:
  - "Always writes N+1 queries"
  - "Forgets to add error handling"
  - "Uses wrong auth pattern for this service"
```

### 2. Collect Examples
```
→ Find 3-5 examples from codebase or git history where AI got it wrong
→ Find 3-5 examples of the correct behavior
→ Write them as before/after pairs
```

### 3. Distill Rule
```
→ From the examples, extract the general rule:
  BAD:  {pattern}
  GOOD: {pattern}
  RULE: {generalized rule in one sentence}
```

### 4. Verify Rule
```
→ Test the rule against 3 new examples (not the training ones)
→ Does the rule correctly predict the right behavior?
→ If not: refine the rule
```

### 5. Encode in Skill
```
→ Find the relevant skill (code-conventions, guardrails, etc.)
→ Add the rule with examples
→ Run edit-skill workflow
```

### 6. Validate
```
→ Present 5 test cases to AI using the updated skill
→ Verify AI now behaves correctly on all 5
→ Log: "Strain site '{name}' resolved after {N} iterations"
```
