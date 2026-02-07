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

## Step 5: Generate settings.json

Create `.claude/settings.json` with the hook configured:

**Base structure** (all projects) - use absolute path for hook:
```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "/path/to/claude-code-toolkit/plugins"
      }
    }
  },
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "transition@local": true
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

**Add plugins based on project type**:
- Web: `"web-development@local": true`
- Quant: `"quant@local": true`

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
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-serena"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-context7"]
    }
  }
}
```

**For projects with nvm** (check if ~/.nvm exists):
Use absolute npx path: `~/.nvm/versions/node/<VERSION>/bin/npx`

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
- `system@local` - Audit, cleanup, setup, status
- `workflow@local` - Explore, plan, next, ship
- `memory@local` - Handoff, memory management
- `development@local` - Analyze, review, test, fix, run, git

**Domain-specific**:
- `web-development@local` - Django + Tailwind CSS workflows
- `quant@local` - Quantitative finance workflows
- `reports@local` - Professional report generation
- `marketing@local` - Content marketing

**ML3T** (for ML4T book work):
- `ml3t-researcher@local` - Academic research with paper search
- `ml3t-coauthor@local` - Book co-authoring

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
