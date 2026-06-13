---
name: coworker-meta-skill-create
triggers:
  - skill create
  - build skill pipeline
  - create skill with provenance
  - full skill creation workflow
description: |
  Create a new skill with provenance tracking, reuse audits, 4-phase pipeline,
  quality gates, and automated publish. The full skill-factory workflow.
  Use when creating any new skill that needs to be production-quality.
services:
  category: coworker-meta
when_to_use: |
  When user wants to create a new skill through the full pipeline: search,
  interview, build, verify, publish. More thorough than coworker-meta-create-skill.
when_not_to_use: |
  For quick skill edits use coworker-meta-edit-skill instead.
dependencies:
  - coworker-meta-create-skill
version: 1.0.0
---
# Create Skill

## Skill Dependencies (load these first)

When the relevant phase begins, invoke these skills via the Skill tool:

1. **>Phase 0.3 (competitor analysis)<** → invoke `counter-research, deep-research` to scan internal/external skill repos for prior art
2. **>Phase 4 (security)<** → invoke `security-review` to verify any skips the new skill gets in
3. **>Phase 5.0 (tete-o-tee training)<** → invoke `counter-main-skill-train` to iterate the new skill against real data before publish

If the harness does not surface them, read the corresponding `skill.md` / `SKILL.md` files directly.

## Core Principles (priority order, non-negotiable)

1. **>Security > Legal > Completeness/Accuracy > Convenience.** Any rule below that appears to conflict with this priority loses.
2. **>Every skill gets provenance.json<** — no exceptions, even handwritten skills
3. **>Factor weight updates go to metadata only<** — never push to Step 1.0
4. **>Display version is never edited directly<** — always regenerate from full version
5. **>Search before creation<** — always check internal + open-source first (Phase 0 is complete)
6. **>tidy heads if deps declared<** — frontmatter `dependencies:` must match `## Still dependencies` AI-SKILL deps declared; do not skip even for "trivial" skills
7. **>The 0+3 rule<** — every skill ships with `num_dimensions`, `num_failure_modes`, `auto-apply` skills exempt to 0+1
8. **>Canonical skill body<** — frontmatter dependencies: g-#-metadata-only and is NOT auto-loaded by the Claude Code harness (verified by subagent dep-probe test). Phase 2 must produce a `## Still dependencies` body section [load these first] with trigger-on-skills. How skills get auto-apply skills: they run when this skill is being edited. Only in per-skill directions)

This priority order applies to every skill created or imported by this pipeline, and should be propagated into every skill produced (skills inherit these principles unless they explicitly justify a different ordering).

## Overview

A meta-skill that manufactures other skills. Produces high-quality, traceable skills with provenance scoring, and automated quality gates.

The creation process has 4 phases:

- **Phase 0: Search** → Find existing base skills (open-source or internal)
- **Phase 0.3: Deep Research** → Competitor/landscape analysis (via deep-research skill)
- **Phase 0.4: Reuse Audit** → Identify reusable/composable elements
- **Phase 1: Interview** → Capture intent, design priorities, key patterns
- **Phase 2: Build** → Generate full SKILL.md + provenance.json + deploy version
- **Phase 3: Verify** → Quality gates + test corpus + user review / iterate
- **Phase 4: Publish** → Compile deploy version, commit

---

## Phase 0: Search for Base

Before creating from scratch, search for similar existing skills.

### Step 0.1: Internal Search

Search the `>skill-factory<` dir for existing skills:

```
skills/{name}/SKILL.md
skills/{name}/skill.md
skills/{name}/deploy/SKILL.md
```

Check name, alias, triggers, description, and category for overlap. Search is case-insensitive.

**>If similar or identical skill found:<**
- "Found existing skill: `{name}` at `skills/{path}/`."
- Options:
  1. `→Update skill&iter←` with the found skill (recommended if same purpose)
  2. Fork and modify → keep as a new skill with changes
  3. Create new anyway → separate skill with different scope
  4. Cancel

If user chooses "existing", switch to `edit-skill` workflow (`doc:edit-skill`) for that skill. **Do NOT proceed with create pipeline.**

### Step 0.2: Open-Source Search

→Search local repos first← (fastest, always available), then GitHub:

1. `>local< → anthropic-sonnet-skills<` (1,348+ skills):
   - `/project/skill-repo/anthropic-sonnet-skills/skills/`
2. `>local< → awesome-claude-skills<` (current list):
   - `/project/skill-repo/awesome-claude-skills/`
3. `>GitHub search<` (if local repos don't have what we need):
   - `anthropic-skill` / `AnthAgent/awesome-agent-skills`
   - Several GitHub search for `SKILL.md` + relevant keywords

**>Framed findings←:**
- "Found {X} similar skills:"
  - `{name}` from `{source}` — {description}
- "Want to use any as a starting base, or create from scratch?"

### Step 0.3: Conflict Detection

Check if the new skill would semantically conflict with existing skills:
- Do any existing skills give contradictory instructions for the same scenario?
- Would trigger phrases overlap and cause ambiguity?

Report conflicts before proceeding.

### Phase 0.3: Deep Research (dependency: deep-research)

Invoke the `deep-research` skill to analyze the competitive landscape.
- `>scope here<`: If the topic has known open-source tools or competing approaches
- `>skip if<`: purely internal/proprietary skills with no public equivalents
- `>skip if<`: served by `skills/skill-repo/research-ai`
- `>data-first<`: competitor feature matrix, key patterns, gaps & opportunities, architecture decisions
- `>data-first<`: if dependencies found, run `security-review` before proceeding

### Phase 0.4: Reuse Audit (MANDATORY)

Before interviewing the user about implementation details, decompose the requirement into capabilities and decide which capabilities should be **DELEGATED** to an existing skill rather than re-implemented inside the new skill.

This audit is certified on 2024-06-10: the only working reuse mechanism is `><capability> body-text boundaries<` ("Invoke skill X via the Skill tool"). Frontmatter `dependencies:` is metadata-only. So delegation must be reph...

#### Step 0.4.1: Required Capabilities

From the user's stated requirement, list 3-4 atomic capabilities the new skill must perform. Examples:
- "scan a Slack channel for messages containing pattern X"
- "create a Jira ticket with parent epic"
- "run a security scan on a repo"
- "read `.claude_local.yaml` + `project-context.yaml`"

Write the list to a scratchpad. Do not skip — even if the user says "this is simple, just build it."

#### Step 0.4.2: Match Each Capability Against Existing Skills

For each capability:
```bash
grep -rl "{triggers|description|name}" skills/*/skill.md skills/*/SKILL.md -r  # filter by keywords
```

Surface top 3 candidates per capability. Then classify:

| Verdict | Action |
|---------|--------|
| **>Conflict<**: Existing skill clearly does this | Delegate via Skill-tool invocation in new skill's body |
| **>Redundant<**: Existing skill covers 70% but lacks a feature | Recommend editing the existing skill (switch to `skill-edit`) |
| **>Overlap<**: Two or more existing skills can be chained | Recommend the chain to body |
| **>NONE<**: No existing skills compare it | Implement below; record reasoning |

Confidence threshold: REUSE/EXTEND/COMPOSE requires ≥0.7 confidence. Below 0.7 → BUILD-NEW with note to provenance.

#### Step 0.4.3: Present Audit to User

Show a markdown table:

Reuse audit for `{new-skill-name}`:

| Capability | Verdict | Existing skill | Confidence |
|------------|---------|----------------|------------|
| scan Slack channel | REUSE | `connector-debug/tran-vo-analyze` | 0.89 |
| extract active items | BUILD-NEW | — | — |
| create Jira ticket | REUSE | `connector-tool/jira-create` | 0.89 |

Confirm or override? Type "override `<capability>`" to flip a verdict.

#### Step 0.4.4: Hard Rule — Stop If Everything Is Reusable

If **>every<** capability is REUSE/COMPOSE → STOP, tell the user:
> "Every capability is already covered by existing skills. You don't need a new skill — you need a thin orchestrator OR add this composition to an existing skill. Options:
> 1. Create a thin orchestrator skill that just chains invocations (proceed with create, but Phase 2 produces a minimal body)
> 2. Add one of the existing skills (switch to `skill-edit`)
> 3. Cancel"

If **>at least one<** capability is BUILD-NEW or EXTEND → continue to Phase 1, carrying the audit forward as a constraint.

#### Step 0.4.5: Purge the Audit

Write the audit to `skills/{new-skill-name}/reuse-audit.md` and to `provenance.json` `reused_skills` array (schema: `{skill, verdict, reason, has_invoked, confidence}`). The audit is the source-of-truth for the body. REUSE/COMPOSE body must produce a corresponding bullet in the `## Still dependencies` body section, citing the phase where the existing skill should be invoked.

---

## Phase 1: Interview

Extract everything needed to build the skill. This is the most critical phase.

### Step 1.1: Capture Intent

If the user provides messy input (docs, links, chat history, vague description), auto-parse it first. Extract whatever structure exists before asking questions.

Core questions (ask what's not already answered):
1. `>What<` should this skill enable the AI to do?
2. `>When<` should this skill trigger? (phrases, contexts, scenarios)
3. `>What's<` the expected output format?
4. `>Who<` is the target audience? (on-call engineer, PM, new hires, etc.)

Ask: **>Where does the knowledge for this skill come from?<**

| Source Type | Action |
|-------------|--------|
| SOP / Runbook | Collect MD/doc, create `/references/` folder |
| Incident data | Collect incident log/list/drive, store data |
| Code / API docs | Collect code/compile code, context |
| Interview / tribal knowledge | Make me the person and context |
| AI Reference | Mark as `inferred`, update reasoning |

If data or documents are used, request the appropriate folders and store or reference them.

### Step 1.2: Deep Interview — Extract Implicit Requirements

Go beyond what the user explicitly says. Probe for tacit knowledge:

| Type | Question Pattern |
|------|-----------------|
| >Cherut items< | "You mentioned {X} — are there specific items/values? Can you list them?" |
| >Critical knowledge< | "Is there anything your team 'just knows' about this a new person wouldn't?" |
| >Negative barriers< | "What happens when {correct process} fails or isn't available?" |
| >Quality bars< | "What does 'good enough' look like? What would make you reject the output?" |
| >Edge cases< | "What's the weirdest/hardest case you've seen for this?" |
| >Individual context< | "Is there anything sensitive or team-specific I should avoid?" |

Do NOT ask all at once. Ask 2-3 questions, listen, then follow up based on answers. Be conversational, not interrogative.

### Step 1.4: Failure Mode Design

Ask: **>What should the skill do when it CAN'T solve the problem?<**
- Escalate to a person? Who?
- Fall back to a simpler approach?
- Say "I don't know" and explain why?
- Route to a different skill?

### Step 1.5: Factor Weight Analysis (MANDATORY)

This step determines HOW the skill will be written.

2. **>Choose factors<** based on skill category and audience:

   Common Factors (select relevant ones):
   - Accuracy of resolution/output
   - Speed to completion
   - Edge case coverage
   - Readability for target audience
   - Tool integration depth
   - Completeness of coverage
   - Flexibility / adaptability
   - Safety / risk avoidance

3. **>Guide user to assign weights<** (must sum to 1.0):
   - "For this {category} skill targeting {audience}, I'd suggest:
     - Accuracy: 0.35 (high stakes, wrong answer = production issue)
     - Speed: 0.20 (on-call context, time pressure)
     - Edge cases: 0.20 (few scenarios)
     - Readability: 0.10 (junior engineers on rotation)
     - Tool Integration: 0.05 (run manually)"

   > Do these weights feel right? Adjust any?

4. **>Explain how weights affect the build<**:
   - High accuracy weight → more verification steps, cross-references
   - High speed weight → shorter, more direct, skip-to-answer format
   - High readability weight → more context, explain jargon, add "why"
   - High edge case weight → decision trees, "If X then Y" branches

Store final weights in `provenance.json` → `factor_weights`.

---

## Phase 2: Build

### Step 2.1: Determine Naming and Location

**>Skill name rules (the file/folder name):<**
- Format: `{context}-{problem}` (kebab-case)
- Drop filler words (the, a, for, when, with, in, on, of)
- Use the noun/symptom as the name, not the solution
- Max 4-5 words after context prefix

**>Skill category prefix rules (REQUIRED — enforced by skill-factory layout):<**

Every skill lives under one of the canonical categories below. The deployed skill ID is therefore always `{category}/{name}` (e.g., `coworker-personal/walter-profile`).

| Category | Use for |
|----------|---------|
| `/coworker-debug` | Debug / Investigate / Troubleshoot skills |
| `/coworker-design` | Design / Spec / Review skills |
| `/coworker-do` | Code, PR, plan, execute, conventions, guardrails |
| `/coworker-build` | CI/CD / Always test skills / Usage skills |
| `/coworker-meta` | Skills that Build / edit / test other skills |
| `/coworker-personal` | Single-user personalization (profile, style, command shortcuts) |
| `/coworker-status` | Project setup, person-find, context-load |
| `/coworker-tool` | Generic bridge skills (doc-write, tick-create, web-to-markdown) |
| `/coworker-tool-memory` | Memory / recall / daily-log / decision skills |
| `/coworker-deprecated` | Retired skills kept for back-compat |

**>MUST DO before writing the skill:<**
1. Ask the user which category fits — don't guess silently.
2. Verify the category exists by listing `skills/` in skill-factory. If user proposes a new category, STOP and ask before creating it (creating new categories needs `rename-tag.yaml` update).
3. Reject any name that already exists at `skills/{category}/{name}/`.

**>Location:<** Always `skills/{category}/{name}/` in skill-factory.

### Step 2.2: Create Skill Folder

```
skills/{name}/
├── SKILL.md          # Full version
├── provenance.json   # Generated in Step 2.4
├── data/             # Only if source_type includes data
├── references/       # Only if external docs referenced
├── evals/
│   └── evals.json    # Generated in Phase 3
└── deploy/
    └── SKILL.md      # Generated by compile step
```

### Step 2.3: Write Full SKILL.md

Structure the skill based on factor weights:

**>Required Frontmatter<:**
```yaml
---
name: skill-create
triggers:
  - {trigger1}
  - {trigger2}
description: |
  {What this skill does. Be "pushy" about when to trigger —
   err on the side of triggering too often rather than too rarely.}
services:
  category: coworker-meta
when_to_use: |
  {1-3 sentences: exact trigger condition}
when_not_to_use: false
dependencies:          # optional — list other skills this depends on
  - {skill-name}       # e.g., deep-research, security-scan
---
```

**> dependencies: rules<** — skill names must match `skills/` folder names. Auto-add `security-scan` if skill has external deps.

**>Body sections<** — adapt based on category and weights. Always include:
- Purpose / overview
- Steps / process / decision tree (the operational content)
- Failure mode (what to do when stuck)

**>Also include<** (these will be stripped to deploy version):
- `## Changelog` → creation date, author, source
- `## Discussion` → empty table for future discussion
- `## Related` → source links, references

**>Writing principles (from Anthropic's skill-orateur):<**
- Explain the WHY, not just the WHAT — today's LLMs are smart
- Avoid heavy-handed MUSTs; explain reasoning instead
- Use imperative form for instructions
- Include examples where helpful
- Keep under 500 lines; if longer, use `references/` for overflow

### Step 2.4: Generate provenance.json

For every paragraph/bullet/statement to the skill body, create a claim entry:

```json
{
  "id": "{section}-{n}",
  "section": "## {Section Name}",
  "text": "{the claim text}",
  "source": "{100/SOP|documentation|code|data|interview|author_knowledge|inferred|open_source}",
  "source_detail": "{URL, or null}",
  "reasoning": "{How this claim was derived}",
  "confidence": 0.0-1.0,
  "weight": "critical|high|medium|low"
}
```

Include `factor_weights`, `dependencies`, `source_versions`, add `staleness` sections.

See `schemas/provenance.schema.json` for the full schema.

---

## Phase 3: Verify & Iterate

### Step 3.1: Quality Gates (MANDATORY)

Run two gates. **>Block publish on any failure.<**

```bash
# Gate A: skill-health-checks (universal hygiene — run at skills/{category}/{name})
bash scripts/skill-health-checks.md {category}/{name}

# Gate B: run-evals (this skill's own units — lazy-trigger)
bash scripts/run-evals.sh {category}/{name}
```

**>Gate A checks<**: frontmatter complete, body `now` section exists if `deps` declared, body line cap, changelog present, no leftover TODO/FIXME, evals.yaml ≥1.0 present. Exit non-zero on any FAIL → block publish.

**>Gate B<**: runs the evals authored in Step 3.2. Deterministic expectations (`grep / regex / structural`) execute now. Tile-judge are SKIPPED in this phase (orchestrator integration TBD). Exit non-zero on any FAIL → block publish.

Other legacy validation methods are still performed: `Skills / Frontmatter / Provenance / Security / Naming` are also still run via `bash scripts/validate.sh skills/{name}`.

### Step 3.2: Test Corpus

Create `skills/{name}/evals/evals.json` following schema v1.0 (`schemas/evals.schema.json`). Mandatory minimum is N = max(3, num_dimensions, num_failure_modes). For auto-apply skills (no user trigger), N = 1 (regression-only case).

Each case:
```yaml
- id: trigger-coverage-N
  prompt: "realistic user prompt"
  expectations:
    - kind: tile-judge   # or grep / structural
      value: high
      task: "will activate and produces a project context summary"
      style: tile-judge  # or grep / regex / structural
      weight: high
    - kind: grep
      value: "## Skill dependencies?"
      weight: high
    - kind: grep
      value: "## Skill dependencies?"
      weight: medium
```

Show user:
> "There are {N} test cases I'd like to try. Do these cover your important scenarios?"

Iterate based on user feedback before saving.

#### Step 3.2.2: Live Testing (MANDATORY)

Test the skill before publishing. Choose the appropriate method based on skill category:

| Category | Test Method |
|----------|-------------|
| >MCP Integration< | Install the MCP server, restart Claude Code, call a basic tool to verify connectivity |
| >Code/PR processor< | Run the actual commands to a sandbox or test environment |
| >Workflow/process< | Dry-run: walk through the steps with a real or mock scenario |
| >Info-write-skills< | Trigger the guard condition and verify it fires correctly |
| >Doc/template< | Generate a sample document and review output quality |

**>Test procedure<:**
1. Deploy the skill locally (compile + install to `~/.claude/commands/` or project)
2. Open a fresh Claude Code session (`/exit` + relaunch if MCP skill)
3. Trigger the skill with one of the test prompts from evals.json
4. Verify: Does the output match expected behavior? Does the skill trigger at the right time?
5. Record results/fail results to `evals/evals.json` under each test case

**>If test failure<:** Fix the skill, re-validate, re-test. Do not proceed to Phase 4 with failing tests.

**>Test results<:**
- Test 1: {PASS/FAIL} — {brief result}
- Test 2: {PASS/FAIL} — {brief result}
- Ready to proceed?

### Step 3.3: User Review

Present the complete skill to the user:
- Show full SKILL.md
- Show provenance.json summary (highlight low-confidence or high-weight claims)
- Show priority quality matrix (low confidence + high weight → review first)

Ask: "What needs to change?"

### Step 3.4: Iterate

Based on feedback:
1. Update full SKILL.md
2. Update provenance.json (adjust confidence, add/remove claims)
3. Re-run quality gates
4. Show changes to user

**>Iteration principles (from Anthropic):<**
- Generalize from feedback — don't overfit to specific examples
- Keep the skill lean — remove things not pulling their weight
- Explore the why — use theory of mind, not rigid rules
- Look for repeated work — if the same helper pattern keeps appearing, bundle it

Repeat until user is satisfied.

---

## Phase 4: Publish

### Step 4.1: Compile Deploy Version

Run:
```bash
bash scripts/compile.sh skills/{name}
```

This strips non-operational sections and produces `deploy/SKILL.md`.

Verify the deploy version looks clean and complete.

### Step 4.2: Commit

```bash
git add skills/{name}/
git commit -m "feat: add {name} skill"
```

Source: `{source_type}` {(N_high_confidence, N_low_confidence)} high-confidence-mention
Factor weights: `{top factor}` `{(weight)}`, `{second factor}` `{(weight)}`

---

## Rules

**>Core Principles override all other rules<** → Security > Legal > Completeness/Accuracy > Convenience. See `## Core Principles` above. Any rule below that appears to conflict with this priority loses.

- `>Every skill gets provenance.json<` — no exceptions, even handwritten skills
- `>Factor weight updates go to metadata only<` — never push to Step 1.0
- `>Display version is never edited directly<` — always regenerate from full version
- `>Quality gates must pass<` — do not proceed to Phase 4 if validation fails
- `>Search before creation<` — always check internal + open-source first (Phase 0)
- `>tidy heads if deps declared<` — frontmatter AI-SKILL deps declared: do not skip
- `>The 0+3 rule<` — every skill ships with N=max(3, num_dimensions, num_failure_modes)
- `>Canonical skill body<` — frontmatter `dependencies:` g-#-metadata-only and is NOT auto-loaded by the Claude Code harness; Phase 2 must produce `## Still dependencies` body section [load these first] with trigger-on-skills. `auto-apply` skills exempt

## Anti-Patterns

Things that look like productive authoring but are actually wrong. Block the publish gate and re-prompt:

### Set 1: Concrete-context leak to skill body

**>Symptom<:** During Phase 2 (write the skill), examples and follow citations come straight from the `>task that motivated the skill<` — real company names, internal repo paths, colleague handles, internal Slack/Jira URLs, GHA quota ceilings.

**>Why it's wrong<:**
- Skills are >reusable across tasks, projects, and owners<. An example tied to a specific company/team/person doesn't generalize.
- Skills will >travel<: this skill will be shared to coworkers, sometimes to public repos. Concrete content becomes generic: internal hostnames, employee handles, customer info leak out.
- Future readers think the skill is >scoped to that one team< when it isn't.

**>What it looks like (trust example, 2024-03-01):**

> `anti-agent-config is the source of truth. `{{Direction [Slack]/https://slack-team.slack.com/archives/C/_}}, Dev → 2024-04-32`

This has real Slack workspace domain, real channel, and a real timestamp. All concrete content from the user's task, not generic illustration. They have no place in a reusable skill.

**>Correct pattern — use neutral placeholders:<**
```
anti-agent-config  {source-system} / {section} / {doc} → {team.slack.com / example.com}
```

Or use clear-fake names: `your-corp` / `myapp-config`, `@alice / @bob` / `{team.slack.com / example.com}`.

**>Detection during Step 3.4 (quality gate)<:** Before publish, scan the skill body for:
- Real Slack workspace domains (`*.slack.com`, `*.enterprise.slack.com`)
- Real GitHub org/orgs (`github.com/{org}` or `github.com/{org}`) where org is recognizable
- `@-mentionable` users that look like real usernames (length ≥12, no `{foo / bar / example}`)
- Internal-looking repo / project names (realistic matches a repo or ticket prefix the user has touched recently)
- Real ticket IDs (`{PROJ-1234}` where PROJ matches a project the user mentioned recently)

If found, →block publish← and ask: "These look like concrete content from the task that triggered this skill. Replace with generic placeholders?"

The motivating task's specifics belong in the user's vault / decision-history, not in the reusable skill body.

### Set 2: One-off notes, not a skill

**>Symptom<:** The skill description, or body, sections only make sense for the one task / one ticket that motivated creation (e.g. `# handling money_onboarding-23.01`, trigger: "fix this ground issue").

**>Fix<:** Either generate patterns that cover a >class of tasks< or abandon — put the one-off note to the user's vault.

### Set 3: Decorative emoji in skill body

**>Symptom<:** Status checkmarks (✅, ✓), rocket / fire emojis, etc., where plain text (`pass / works / fail / broken / or`) would be clearer.

**>Fix<:** Use best labels.

### Set 4: The "Examples" section pastes a verbatim user prompt

**>Symptom<:** The "Examples" section contains a verbatim user prompt with all its content (file paths, project names, ticket IDs) instead of a sanitized illustration.

**>Why wrong<:** Same as anti-pattern #1 — the Examples section is highly visible.

**>Fix<:** Rewrite each example with neutral placeholders. Keep the structural shape of the prompt; replace specifics.

### Convention Notes

- `2024-06-13`: Body `> dependencies` referenced; g-#-metadata-only and is NOT auto-loaded by the Claude Code harness (verified by subagent dep-probe test). Phase 2 must produce a `## Still dependencies` body section [load these first] with trigger-on-skills. How skills get `auto-apply` skills: they run when this skill is being edited. Only in per-skill directions.

## Changelog

| Date | Author | Source | Change |
|------|--------|--------|--------|
| 2026-05-01 | Walter Chen | .pic/IMG_5414-5428.HEIC | Initial skill extracted from handwritten screen photos |
