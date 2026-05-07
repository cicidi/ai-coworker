---
name: coworker-meta-review-request
triggers:
  - find reviewer
  - who should review this
  - draft review request
  - request a review
description: |
  Auto-find the right reviewer based on team.yaml and draft a review request
  message for Slack or GitHub. Use before opening a PR for major changes.
services:
  category: coworker-meta
when_to_use: |
  When user asks who should review this, find a reviewer, or draft a review
  request. Run after implementation is complete, before PR.
when_not_to_use: |
  Skip for trivial PRs that do not need a dedicated reviewer.
version: 1.0.0
---

# Review Request

Auto-selects the best reviewer and drafts a review request message for Slack, Telegram, or Discord.

## Process

### 1. Find Reviewer
```
→ Read team.yaml for team members and their services
→ Read the PR/changes to understand which services are affected
→ Match affected services to team members
→ Exclude: PR author, anyone marked as unavailable
→ Propose: "Best reviewer: {name} — they own {service}. Confirm? (y/n)"
```

### 2. Draft Message
```
Hi {name}! 👋

Could you review this PR when you get a chance?

📋 PR: {PR title}
🔗 {PR URL}
📝 What it does: {1-2 sentence summary}
⏱️ Size: {lines changed} lines
🧪 Tests: {yes/no + coverage note}

No rush — by {suggested deadline} works if that's OK.

Thanks!
```

### 3. Send via Preferred Channel
```
→ Ask: "Send via Slack / Telegram / Discord / GitHub comment?"
→ Use appropriate MCP to send
→ Also post GitHub PR review request via GitHub MCP
```

### 4. Confirm
```
→ "Review request sent to {name} via {channel} ✓"
```
