---
name: mcp-github
description: GitHub MCP — create/search/comment on issues and PRs via official MCP server
aliases: [github]
---

# GitHub MCP

**Package:** `@modelcontextprotocol/server-github`
**Install:** `npm install -g @modelcontextprotocol/server-github`

## Setup

### Required Env Vars
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
```

Token scopes needed: `repo`, `read:org`, `read:user`

### MCP Config (.mcp.json)
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

## Key Capabilities
- Create, read, update, close issues
- Search issues with filters (label, assignee, state, milestone)
- Create PRs, request reviews, merge PRs
- Add comments to issues and PRs
- Read repository file tree and file contents
- Search code across repositories

## Usage Patterns

### Create Issue
```
Use GitHub MCP to create an issue:
- Title: [prefix] {description}
- Body: include context, steps to reproduce, expected behavior
- Labels: bug, enhancement, question, etc.
- Assignee: cicidi
- Repo: {from .local_config.yaml github.repo}
```

### Search Issues
```
Search for open issues related to {topic} in repo {repo}
Filter by: label:{label} assignee:{user} state:open
```

### Create PR
```
Create PR from branch {branch} to main:
- Title: conventional commit style
- Body: reference issue with "Closes #123"
- Request review from: {reviewer from team.yaml}
```

## Guardrails
- Never close issues without human confirmation
- Never merge PRs without human approval
- Always reference an issue number in PR body
