---
name: coworker-bug-sleuth
triggers:
  - investigate this ticket
  - oncall investigation
  - deep dive into issue
  - follow every lead
description: |
  Deep investigation of tickets, logs, or on-call issues. Follows every lead
  autonomously. Best for incidents, alert investigations, and deep dives.
services:
  category: coworker-debug
when_to_use: |
  When user is on-call, has an incident, or asks to deeply investigate a ticket
  or log file. Follows every lead until root cause is found or exhausted.
when_not_to_use: |
  For simple known bugs use coworker-debug-issue-debug instead.
version: 1.0.0
---

# Issue Investigate

Deep, autonomous investigation of a problem. Follows every lead until root cause is found.

## When to Use
- On-call incident investigation
- "Why is this slow?" performance issues
- "Why did this fail in prod but not staging?" environment issues
- Complex multi-service issues
- Historical analysis ("when did this start?")

## Process

### 1. Define the Problem
```
→ What is observable? (error rate, latency, wrong data)
→ When did it start?
→ What changed recently? (deploys, config changes, data volume)
→ Who/what is affected? (all users, specific endpoint, specific region)
```

### 2. Build Investigation Plan
```
→ List all data sources to check:
  - GitHub Issues / PRs (recent changes)
  - Logs (via Splunk/Datadog MCP if available, else grep)
  - Code (git blame, git log)
  - Metrics / dashboards
  - Recent deployments
→ Prioritize by likelihood of relevance
```

### 3. Investigate Autonomously
```
→ Check each data source
→ For each finding: is it relevant? Does it lead to another lead?
→ Follow chains: finding → hypothesis → evidence → conclusion
→ Do NOT stop at first finding — verify it's the ROOT cause
```

### 4. Build Timeline
```
[timestamp] Event: {description}
[timestamp] Event: {description}
...
[timestamp] ← Root cause likely here
```

### 5. Report
```markdown
## Investigation Report

**Problem:** {description}
**Duration:** {start} → {end or ongoing}
**Impact:** {what/who was affected}

## Root Cause
{precise description}

## Evidence
1. {evidence item}
2. {evidence item}

## Timeline
{timeline}

## Fix
{what to do}

## Prevention
{how to prevent recurrence}
```

### 6. Create Issue + Fix
```
→ Create GitHub Issue with report
→ Proceed with fix (quick-task or full pipeline)
```
