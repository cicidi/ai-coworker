---
name: setup-coworker
description: 5-step interactive setup — scan project, generate CLAUDE.md, detect identity, create local config, install hooks
aliases: [setup]
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
   - OpenCode: .opencode/instructions/
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
