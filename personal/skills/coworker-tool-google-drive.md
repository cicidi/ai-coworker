---
name: coworker-tool-google-drive
triggers:
  - read google doc
  - write to google sheets
  - google drive mcp
  - update google slides
description: |
  Google Drive MCP — read/write Google Docs, Sheets, Slides via official MCP server.
  Requires authentication each session.
services:
  category: coworker-tool
when_to_use: |
  When user wants to read or write Google Docs, Sheets, or Slides. Re-authenticate
  via browser flow each session if needed.
when_not_to_use: |
  false
version: 1.0.0
---

# Google Drive MCP

**Package:** `@modelcontextprotocol/server-gdrive`
**Install:** `npm install -g @modelcontextprotocol/server-gdrive`

## Setup

### Enable Google Drive API
1. Go to https://console.cloud.google.com
2. Create/select project → Enable "Google Drive API"
3. Create OAuth 2.0 credentials (Desktop App type)
4. Download `credentials.json`

### Required Env Vars
```bash
export GDRIVE_CREDENTIALS_PATH="/path/to/credentials.json"
export GDRIVE_TOKEN_PATH="/path/to/token.json"   # created on first auth
```

### MCP Config (.mcp.json)
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GDRIVE_CREDENTIALS_PATH": "${GDRIVE_CREDENTIALS_PATH}",
        "GDRIVE_TOKEN_PATH": "${GDRIVE_TOKEN_PATH}"
      }
    }
  }
}
```

### First-Time Auth
```bash
# Run once to authorize — opens browser for OAuth consent
npx @modelcontextprotocol/server-gdrive auth
```

## Key Capabilities
- Read Google Docs (full content as text)
- Read/write Google Sheets (rows, columns, ranges)
- Search files by name or content
- Create new Google Docs
- List files in Drive or specific folders
- Read Google Slides content

## Usage Patterns

### Read a Document
```
Read Google Doc at URL: {url}
Extract: {specific section or full content}
```

### Search Drive
```
Search Google Drive for files named "{filename}"
or containing "{keyword}"
Return: file name, URL, last modified date
```

### Update Sheet
```
In Google Sheet {url}, update:
- Sheet: {sheet name}
- Range: {A1:B10}
- Values: {data}
```

## Guardrails
- Never share file URLs publicly
- Never expose Drive contents in Slack/Discord messages — share the URL instead
- Re-authenticate via browser if token expires
