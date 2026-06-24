---
name: connect-discord
description: Discord MCP — send messages, read channels, manage notifications via Discord bot
aliases: [discord]
---

# Discord MCP

**GitHub:** `https://github.com/v-3/discordmcp`
**Install:** `npx discordmcp` or clone and run locally

## Setup

### Create Discord Bot
1. Go to https://discord.com/developers/applications → New Application
2. Bot tab → Add Bot → copy Token
3. OAuth2 → URL Generator → select `bot` scope + permissions:
   - `Send Messages`, `Read Message History`, `View Channels`
4. Invite bot to your server using generated URL

### Required Env Vars
```bash
export DISCORD_TOKEN="your_bot_token"
export DISCORD_GUILD_ID="your_server_id"   # Right-click server → Copy ID
```

### MCP Config (.mcp.json)
```json
{
  "mcpServers": {
    "discord": {
      "command": "npx",
      "args": ["-y", "discordmcp"],
      "env": {
        "DISCORD_TOKEN": "${DISCORD_TOKEN}",
        "DISCORD_GUILD_ID": "${DISCORD_GUILD_ID}"
      }
    }
  }
}
```

## Key Capabilities
- Send messages to any channel in your server
- Read channel history
- List channels and members
- Send DMs to users
- Post embeds with rich formatting

## Usage Patterns

### Send to Channel
```
Send Discord message to #{channel-name}:
"{message}"
Use DISCORD_TOKEN. Look up channel ID from server.
```

### Notification Embed
```
Send Discord embed notification:
- Title: {title}
- Description: {description}
- Color: green (success) / red (error) / yellow (warning)
- Channel: #notifications
```

## Channel Registry
Update with your actual channel IDs:
```yaml
channels:
  general: "1234567890"
  dev: "1234567890"
  alerts: "1234567890"
```

## Guardrails
- Never send tokens, passwords, or secrets
- Never send PII in public channels
- Always use channel IDs from registry — never guess
