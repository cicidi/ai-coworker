---
name: coworker-connect-slack
triggers:
  - send slack message
  - post to slack
  - read slack channel
  - slack notification
description: |
  Slack MCP — read/write messages, search channels, send notifications. Use for
  all Slack interactions including team announcements and alerts.
services:
  category: coworker-tool
when_to_use: |
  When user wants to send a Slack message, search channels, or post notifications.
  Check team.yaml for correct channel IDs.
when_not_to_use: |
  false
version: 1.0.0
---

# Slack MCP

**Package:** `@modelcontextprotocol/server-slack`
**Install:** `npm install -g @modelcontextprotocol/server-slack`

## Setup

### Required Env Vars
```bash
export SLACK_BOT_TOKEN="xoxb-..."      # Bot token (sends as app)
export SLACK_USER_TOKEN="xoxp-..."     # User token (sends as you) — optional
```

### Create Slack App
1. Go to https://api.slack.com/apps → Create New App
2. Add Bot Token Scopes:
   - `chat:write`, `channels:read`, `channels:history`
   - `groups:read`, `groups:history`, `im:read`, `im:write`
   - `users:read`, `search:read`, `reactions:write`
3. Install to workspace → copy Bot Token

### MCP Config (.mcp.json)
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

## Key Capabilities
- Send messages to channels or DMs
- Read channel history
- Search messages across workspace
- React to messages with emoji
- List channels and members

## Usage Patterns

### Send Notification
```
Send a Slack message to #{channel}:
"{message}"
Use SLACK_BOT_TOKEN. Do not include sensitive data.
```

### Search Messages
```
Search Slack for messages about {topic} in #{channel}
Return last 10 results with timestamps
```

### DM User
```
Send DM to {username} via Slack:
"{message}"
Look up their Slack ID from team.yaml
```

## Channel Registry
Update with your actual channel IDs:
```yaml
channels:
  general: "C0XXXXXXX"
  dev: "C0XXXXXXX"
```

## Guardrails
- Never send tokens, passwords, or secrets in messages
- Never send PII in public channels
- Always use channel registry — never guess channel IDs
