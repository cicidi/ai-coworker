---
name: coworker-self-init
triggers:
  - setup coworker
  - initialize ai coworker
  - set up for new project
  - install coworker
description: |
  5-step interactive setup — scan project, generate CLAUDE.md, detect identity,
  create local config, install hooks. Run once per new project or machine.
services:
  category: coworker-meta
when_to_use: |
  When starting on a new project or machine. When user asks to "set up the
  AI coworker", "initialize coworker", or "install skills".
when_not_to_use: |
  Skip if coworker is already set up and .local_config.yaml exists.
version: 1.0.0
---

# Setup Coworker

Run the 5-step interactive setup to initialize the AI coworker for a new project.

## Steps

### Step 1 — Identity Detection
```
→ Run `whoami` to get system username
→ Get project name from current folder name
→ Confirm: "Detected identity: {user} working on {project}. Correct?"
```

### Step 2 — Repo Check
```
→ Check if ai-coworker repo is cloned locally
→ If no: guide through: git clone + upstream remote setup
→ If yes: validate path exists and upstream is set
```

### Step 3 — Role Selection
```
→ Ask: "What's your role? (backend / frontend / architect / pm — multi-select)"
→ Copy team-common + role-specific skills to IDE config directory
```

### Step 4 — IDE Detection
```
→ Auto-detect: Claude Code, Cursor, OpenCode, Gemini CLI
→ If not found: "Which IDE are you using?"
→ Install skills to appropriate location for each detected IDE:
   - Claude Code: .claude/commands/
   - Cursor: .cursor/rules/
   - OpenCode: ~/.config/opencode/skills/skill-factory/personal-skills/
   - Gemini CLI: .gemini/
```

### Step 5 — MCP Tool Setup
```
→ For each integration (GitHub, Slack, Telegram, Discord, Google Drive):
  → Check if already installed
  → If not: "Install {tool}? (y/n)"
  → Auto-install via npm/uvx if possible
  → Prompt for required env vars (tokens) if needed
→ Verify: "Setup complete! ✓"
```

## Output
- `.local_config.yaml` created in project root (gitignored)
- Skills installed to all detected IDEs
- MCP servers configured in `.mcp.json`
- CLAUDE.md symlinked for Cursor/OpenCode/Gemini
