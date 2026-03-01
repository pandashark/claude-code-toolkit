---
allowed-tools: [Read, Write, Edit, Bash]
argument-hint: "[--all | --security | --formatting | --notifications | --compaction]"
description: Configure Claude Code hooks for security, formatting and quality checks, notifications, and compaction
---

# Hooks Setup

Install hook configurations into a project's `.claude/settings.json` to enforce security rules, auto-format and lint code, send notifications, and preserve state before compaction.

## Available Categories

| Category | Event | What It Does |
|----------|-------|------------|
| **security** | PreToolUse | Blocks dangerous commands (rm -rf /, sudo, chmod 777, force push to main, curl\|sh) |
| **formatting** | PostToolUse | Auto-formats files then runs linters/type checkers (ruff, prettier, gofmt, rustfmt, mypy, tsc) |
| **notifications** | Stop/Notification | Desktop notifications when sessions finish (macOS + Linux) |
| **compaction** | PreCompact | Saves git diff and work unit state before context compaction |

## Installation Steps

### Step 1: Determine which categories to install

Check the argument provided by the user:
- `--all`: Install all 4 categories
- `--security`, `--formatting`, `--notifications`, `--compaction`: Install only that category
- No argument: Ask the user which categories they want (list the table above), allow multiple selections

### Step 2: Read the hook template assets

The templates are shipped with this plugin at `plugins/setup/assets/hooks/` (relative to the toolkit root).

Find the plugin directory by reading `.claude/settings.json` and looking at the `extraKnownMarketplaces` path, then append `setup/assets/hooks/`. Read each selected template JSON file:

- `security.json`
- `formatting.json`
- `notifications.json`
- `compaction.json`

### Step 3: Merge hooks into settings.json

Read the existing `.claude/settings.json` (create it if missing).

For each selected template, merge its `hooks` entries into the existing `hooks` object in settings.json:
- If the event type (e.g., `PreToolUse`) already exists, **append** the new matcher entries to the existing array — do not replace.
- If the event type does not exist, add it.
- **Preserve all other keys** in settings.json (extraKnownMarketplaces, enabledPlugins, statusLine, etc.).

If `.claude/settings.json` doesn't exist, create it with just the merged hooks.

### Step 4: Create hooks directory

```bash
mkdir -p .claude/hooks
```

This prepares the directory for any standalone hook scripts the user may add later.

### Step 5: Verify

Validate the resulting settings.json is valid JSON:
```bash
jq empty .claude/settings.json
```

### Step 6: Report

Print a summary:
- Which hook categories were installed
- Which event types were configured (PreToolUse, PostToolUse, PreCompact, Stop, Notification)
- Note any tool dependencies (ruff, prettier, gofmt, rustfmt, mypy, tsc, jq) — these are optional and hooks degrade gracefully if tools are not installed
- Remind user to restart Claude Code for hooks to take effect
