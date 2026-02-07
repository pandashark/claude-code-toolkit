---
allowed-tools: [Read, Write, Edit, Bash]
argument-hint: ""
description: Configure Claude Code statusline to show context usage, model, and git info
---

# Statusline Setup

Install a 2-line colored statusline that shows context usage, model name, project name, and git info.

## What It Does

Displays a live status bar below the Claude Code prompt:
```
████████░░ 78.3% (156k/200k) | opus 4.6
my-project | ✎ 3 ↑2 | 󰘬 feature/my-branch
```

- **Context bar**: Green (<50%), orange (50-80%), red (>=80%) with token counts
- **Model**: Extracted from model ID (opus/sonnet/haiku + version)
- **Git**: Branch name, ahead/behind upstream, edited file count

## Installation Steps

### Step 1: Find the statusline.js asset

The asset is shipped with this plugin at `plugins/setup/assets/statusline.js` (relative to the toolkit root).

Use the Read tool to read the statusline.js asset from this plugin's directory. The plugin directory can be found by looking at the `extraKnownMarketplaces` path in `.claude/settings.json`, then appending `setup/assets/statusline.js`. If you cannot determine the plugin path, read it from the known location in the marketplace configuration.

### Step 2: Create .claude/statusline.js

Ensure the `.claude/` directory exists, then use the Write tool to create `.claude/statusline.js` with the content from the asset. The file should be an exact copy.

After writing, make it executable:
```bash
chmod +x .claude/statusline.js
```

### Step 3: Configure settings.json

Read the existing `.claude/settings.json` file (create it if it doesn't exist).

Add or update the `statusLine` key:
```json
"statusLine": {
  "type": "command",
  "command": "cat | node .claude/statusline.js"
}
```

**Important**: Preserve all other existing keys in settings.json. Only add/update the `statusLine` entry.

If `.claude/settings.json` doesn't exist, create it with just the statusLine config:
```json
{
  "statusLine": {
    "type": "command",
    "command": "cat | node .claude/statusline.js"
  }
}
```

### Step 4: Verify

```bash
echo '{"model":{"id":"claude-opus-4-6","display_name":"Claude Opus 4.6"},"context_window":{"used_percentage":25,"total_input_tokens":50000,"context_window_size":200000}}' | node .claude/statusline.js
```

### Step 5: Report

Print a summary of what was configured:
- Whether statusline.js was created or updated
- Whether settings.json was created or updated
- Remind user to restart Claude Code to see the statusline
