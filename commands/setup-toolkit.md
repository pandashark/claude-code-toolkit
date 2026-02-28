---
description: Initialize Claude Code configuration for a new project
temperature: 0.0
---

You are helping set up Claude Code configuration for a project.

# Project Setup Workflow

## Step 1: Detect Project Context

First, examine the current directory to understand the project type:

```bash
pwd
ls -la
```

Look for indicators:
- **Web project**: package.json, Django files (manage.py, settings.py), templates/
- **Python project**: pyproject.toml, setup.py, requirements.txt
- **Quant/Trading**: mentions of trading, strategies, backtesting
- **General**: anything else

## Step 2: Ask User for Configuration

Use AskUserQuestion to determine:

1. **Project type** (affects which plugins to enable):
   - General development (system, workflow, memory, development)
   - Web development (+ web-development)
   - Quantitative/Trading (+ quant)
   - Multiple types (let them select multiple)

2. **MCP servers** (which ones to enable):
   - Chrome DevTools (browser automation, web testing)
   - Serena (semantic code understanding)
   - Context7 (documentation access)
   - All standard servers

3. **Permissions** (optional):
   - Standard (allow common operations)
   - Strict (ask for most operations)
   - Custom (ask user to specify later)

## Step 3: Create Directory Structure

```bash
mkdir -p .claude/hooks
mkdir -p .claude/transitions
```

## Step 4: Create Transition Hook

Create `.claude/hooks/init-transition.sh`:

```bash
cat > .claude/hooks/init-transition.sh << 'HOOK_EOF'
#!/bin/bash
# Initialize hourly transition file for session progress tracking
set -e
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TRANSITIONS_DIR="$PROJECT_ROOT/.claude/transitions"
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)
TODAY_DIR="$TRANSITIONS_DIR/$TODAY"
HOURLY_FILE="$TODAY_DIR/${HOUR}.md"
mkdir -p "$TODAY_DIR"
if [ ! -f "$HOURLY_FILE" ]; then
    echo "# Session Progress: $TODAY ${HOUR}:00" > "$HOURLY_FILE"
    echo "" >> "$HOURLY_FILE"
    echo "---" >> "$HOURLY_FILE"
    echo "" >> "$HOURLY_FILE"
fi
exit 0
HOOK_EOF
chmod +x .claude/hooks/init-transition.sh
```

## Step 4b: Detect Plugin Marketplace Name

Before generating settings.json, read the user's marketplace config to find the correct plugin suffix:

```bash
cat ~/.claude/plugins/known_marketplaces.json
```

Look for the marketplace entry whose `source.path` points to the toolkit's `plugins/` directory (not `claude-plugins-official`). The **key name** of that entry is the marketplace suffix to use in `enabledPlugins`. For example, if the key is `"aai-plugins"`, then plugins are referenced as `system@aai-plugins`, `workflow@aai-plugins`, etc.

Store this as `MARKETPLACE_NAME` for the next step.

## Step 5: Generate settings.json

Create `.claude/settings.json` with the hook configured:

**Base structure** (all projects) - use absolute path for hook, and the detected MARKETPLACE_NAME as the plugin suffix:
```json
{
  "enabledPlugins": {
    "system@MARKETPLACE_NAME": true,
    "workflow@MARKETPLACE_NAME": true,
    "memory@MARKETPLACE_NAME": true,
    "development@MARKETPLACE_NAME": true,
    "transition@MARKETPLACE_NAME": true
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "ABSOLUTE_PATH_TO_PROJECT/.claude/hooks/init-transition.sh"
          }
        ]
      }
    ]
  }
}
```

**Important**: Replace `ABSOLUTE_PATH_TO_PROJECT` with the actual project path (use `pwd` to get it).

**Add plugins based on project type** (using the detected MARKETPLACE_NAME):
- Web: `"web-development@MARKETPLACE_NAME": true`
- Quant: `"quant@MARKETPLACE_NAME": true`

**Add permissions** (if requested):
- Standard Python permissions for Python projects
- Web testing permissions for web projects

## Step 6: Generate .mcp.json

Create `.mcp.json` at project root with requested MCP servers:

**Standard configuration**:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    },
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

**Note**: Serena is a Python-based MCP server and requires `uvx` (not `npx`). Verify `uvx` is installed (`which uvx`) before including it.

**For projects with nvm** (check if ~/.nvm exists):
Use absolute npx path for the npx-based servers: `~/.nvm/versions/node/<VERSION>/bin/npx`

## Step 7: Create Optional Files

Based on project type, optionally create:

**For all projects** - `.claude/README.md`:
```markdown
# Claude Code Configuration

This project is configured with Claude Code support.

## Enabled Plugins
[list enabled plugins]

## Available Commands
Run `/help` to see available commands.

## MCP Servers
[list configured MCP servers]
```

## Step 8: Summary

Show user what was created:
```bash
ls -la .claude/
test -f .mcp.json && echo ".mcp.json created" || echo "No .mcp.json"
```

Print summary:
- ✅ Files created
- 📦 Enabled plugins
- 🔧 Configured MCP servers
- 📝 Next steps

# Plugin Configurations Reference

## Available Plugins

**Core** (recommended for all projects):
- `system@MARKETPLACE_NAME` - Audit, cleanup, setup, status
- `workflow@MARKETPLACE_NAME` - Explore, plan, next, ship
- `memory@MARKETPLACE_NAME` - Handoff, memory management
- `development@MARKETPLACE_NAME` - Analyze, review, test, fix, run, git

**Domain-specific**:
- `web-development@MARKETPLACE_NAME` - Django + Tailwind CSS workflows
- `quant@MARKETPLACE_NAME` - Quantitative finance workflows
- `reports@MARKETPLACE_NAME` - Professional report generation
- `marketing@MARKETPLACE_NAME` - Content marketing

**ML3T** (for ML4T book work):
- `ml3t-researcher@MARKETPLACE_NAME` - Academic research with paper search
- `ml3t-coauthor@MARKETPLACE_NAME` - Book co-authoring

## Standard MCP Servers

- `chrome-devtools` - Browser automation (26 tools)
- `serena` - Semantic code understanding (70-90% token reduction)
- `context7` - Up-to-date library documentation

## Permission Templates

### Standard Python Development
```json
"permissions": {
  "allow": [
    "Bash(pytest:*)",
    "Bash(ruff:*)",
    "Bash(mypy:*)",
    "Bash(git:*)",
    "Bash(python:*)",
    "Read(*.py)",
    "Read(*.md)",
    "Write(src/**/*.py)",
    "Write(tests/**/*.py)",
    "Edit(src/**/*.py)",
    "Edit(tests/**/*.py)"
  ],
  "deny": [
    "Bash(rm -rf:*)",
    "Bash(sudo:*)"
  ]
}
```

### Web Development
Add to allow list:
```json
"Read(*.html)",
"Read(*.css)",
"Read(*.js)",
"Bash(npm:*)",
"Bash(npx:*)",
"mcp__chrome-devtools__*"
```

# Examples

## Example 1: Simple Python Project
User wants: general development
Result: system, workflow, memory, development plugins + standard MCP

## Example 2: Django Web App
User wants: web development
Result: core plugins + web-development plugin + chrome-devtools MCP

## Example 3: Trading Dashboard
User wants: web + quant
Result: core plugins + web-development + quant + all MCP servers

# Important Notes

1. **Always create .mcp.json at project root** (not in .claude/)
2. **Plugin marketplace path** must point to your local clone of this toolkit's `plugins/` directory
3. **Ask before overwriting** existing configuration
4. **Be interactive** - let user customize before creating files
5. **Show summary** of what was created
