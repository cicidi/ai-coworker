---
name: understand
description: Understand user requirements through clarifying questions. Always start here before any coding task.
aliases: [understand, clarify]
---

# Understand Requirements

Stage 1 of the workflow. Clarify what the user wants before touching any code.

## Goal
Form a clear, confirmed understanding of the task. No implementation yet.

## Process

### 1. Parse the Request
```
→ Identify: what we're building/fixing
→ Identify: scope boundaries (what's in, what's out)
→ Identify: any constraints mentioned (language, framework, performance, etc.)
```

### 2. Ask Clarifying Questions
For any ambiguity, ask the user. Key areas to probe:
- **Scope**: Which components/systems are affected?
- **Priority**: Is this urgent or can it wait?
- **Constraints**: Specific tech choices, deadlines, dependencies?
- **Success criteria**: How will we know it's done?

### 3. Confirm Understanding
After questions are resolved, summarize back to user:
```
Understood: {1-2 sentence summary}
Scope: {files/systems involved}
Key decisions: {choices made}
```
Wait for user confirmation before moving to decompose.

## Rules
- Do NOT read or edit any source files during this stage
- Do NOT propose solutions yet — just understand the problem
- If the request is crystal clear (no ambiguity), confirm and move on immediately
- Be concise — don't ask questions you can infer from context
