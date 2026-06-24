---
name: connect-telegram
description: Telegram MCP — send messages and notifications via Telegram bot
aliases: [telegram]
---

# Telegram MCP

**GitHub:** `https://github.com/chigwell/telegram-mcp`
**Install:** `uvx telegram-mcp` or `pip install telegram-mcp`

## Setup

### Create Telegram Bot
1. Open Telegram → search `@BotFather`
2. Send `/newbot` → follow prompts → copy the token
3. Get your Chat ID: message `@userinfobot` or use `https://api.telegram.org/bot{TOKEN}/getUpdates`

### Required Env Vars
```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
export TELEGRAM_CHAT_ID="your_chat_id"       # your personal chat ID
```

### MCP Config (.mcp.json)
```json
{
  "mcpServers": {
    "telegram": {
      "command": "uvx",
      "args": ["telegram-mcp"],
      "env": {
        "TELEGRAM_BOT_TOKEN": "${TELEGRAM_BOT_TOKEN}",
        "TELEGRAM_CHAT_ID": "${TELEGRAM_CHAT_ID}"
      }
    }
  }
}
```

## Key Capabilities
- Send text messages to your personal chat
- Send formatted messages (Markdown/HTML)
- Send notifications for build completions, alerts, reminders
- Read recent messages from bot chat

## Usage Patterns

### Send Notification
```
Send a Telegram notification to cicidi:
"✅ {task} completed — {summary}"
Use TELEGRAM_CHAT_ID from env vars.
```

### Alert
```
Send urgent Telegram alert:
"🚨 {alert message}"
```

### Build Complete Notification
```
After long-running task completes, send:
"✅ Done: {task name}
Result: {success/failure}
Details: {brief summary}"
```

## Guardrails
- Never send tokens, passwords, or secrets
- Never send PII
- Use for notifications and alerts — not for code output
