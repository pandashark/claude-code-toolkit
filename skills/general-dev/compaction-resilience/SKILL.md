---
name: compaction-resilience
description: Context preservation strategies and native skills alignment for Claude Code. Covers compaction hooks, file-based persistence patterns, transition files, and .claude/skills/ directory structure. Use when setting up session continuity, configuring compaction hooks, creating skills, or losing context to auto-compact. Prevents context loss, broken session handoffs, and skill discovery failures.
---

# Compaction Resilience & Skills Alignment

Strategies for preserving critical context when Claude Code auto-compacts conversation history, and guidance for aligning with the native `.claude/skills/` directory format.

---

## Quick Reference

**When to use this skill:**
- Setting up a new project for session continuity
- Context is being lost during long sessions (20+ compaction events/day is common)
- Creating or installing skills for Claude Code discovery
- Debugging why a skill is not being loaded

**Common triggers:** "context lost", "auto-compact", "session handoff", "skill not found", "preserve state", "compaction hook"

---

## Part 1: Why Compaction Happens

Claude Code auto-compacts when the conversation approaches the context window limit. The system summarizes older turns to free space, but detail is inevitably lost. In a typical development session:
- Compaction can trigger 20+ times per day
- Each compaction loses task-specific details (file paths, decisions, partial progress)
- Without mitigation, Claude "forgets" what it was working on

The solution: **persist critical state to files** that survive compaction.

---

## Part 2: File-Based Persistence Patterns

### Transition Files (Recommended)
Write progress to `.claude/transitions/YYYY-MM-DD/HHMMSS.md` hourly or at 70% context usage:
- Current task and status
- Key decisions made
- Next steps
- Install via `/setup:transitions`

### Work Unit State
The `.claude/work/{id}/state.json` file tracks task progress, dependencies, and completion status. This persists through compaction automatically since it is written to disk.

### Memory Files
Use `.claude/memory/` for persistent project knowledge (conventions, architecture decisions, dependency notes). Claude reads these at session start.

### CLAUDE.md
The project root `CLAUDE.md` is always loaded into context. Keep critical instructions here -- they survive any compaction or `/clear`.

---

## Part 3: Compaction Hooks

A PreCompact hook runs automatically before each compaction event, saving state to disk.

### Installing the Hook

Use `/setup:hooks --compaction` to install the compaction hook template. This creates a PreCompact hook that:
- Snapshots `git diff --stat HEAD` to `.claude/compaction-snapshots/`
- Copies active work unit `state.json` to the snapshot directory
- Timestamps each snapshot for traceability

The hook template is at `plugins/setup/assets/hooks/compaction.json`.

### Manual Configuration

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "dir=.claude/compaction-snapshots; mkdir -p $dir; ts=$(date -u +%Y%m%dT%H%M%SZ); git diff --stat HEAD > $dir/$ts-diff.txt"
          }
        ]
      }
    ]
  }
}
```

---

## Part 4: The 70% Rule

Proactively hand off before compaction forces it:

1. At ~70% context usage, run `/transition:handoff`
2. This creates a structured handoff document with session focus, decisions, and next steps
3. After `/clear`, run `/transition:continue` to load the handoff
4. The new session starts with full context of where you left off

This is more reliable than waiting for auto-compaction because you control what gets preserved.

---

## Part 5: Native `.claude/skills/` Alignment

### Directory Structure

Claude Code discovers skills in two locations:
```
~/.claude/skills/       # User-level (all projects)
.claude/skills/         # Project-level (one project)
```

Each skill is a directory containing `SKILL.md`:
```
.claude/skills/
  my-skill/
    SKILL.md            # Required: frontmatter + content
```

### YAML Frontmatter Requirements

```yaml
---
name: my-skill
description: Single-line description of what this skill covers, when to use it, and what it prevents.
---
```

- `name`: kebab-case, matches directory name
- `description`: single line -- this is all Claude sees at startup (~100 tokens)

### Progressive Disclosure

- **Tier 1 (startup)**: Only `name` and `description` are loaded (~100 tokens per skill)
- **Tier 2 (on-demand)**: Full SKILL.md content loads when Claude determines relevance (10-20KB)

### Project vs User Level

| Location | Scope | Use when |
|----------|-------|----------|
| `.claude/skills/` | This project only | Project-specific patterns |
| `~/.claude/skills/` | All projects | General expertise (auth, Docker, SQL) |

### Installing Toolkit Skills

Copy or symlink from this toolkit:
```bash
# Copy (standalone)
cp -r skills/general-dev/my-skill ~/.claude/skills/

# Symlink (stays in sync with toolkit updates)
ln -s /path/to/toolkit/skills/general-dev/my-skill ~/.claude/skills/my-skill
```

---

## Quick Checklist

**Compaction Resilience:**
- [ ] Transition files configured (`/setup:transitions`)
- [ ] Compaction hook installed (`/setup:hooks --compaction`)
- [ ] Work unit state tracked in `.claude/work/`
- [ ] Critical instructions in `CLAUDE.md`
- [ ] Handoff at 70% context (`/transition:handoff`)

**Skills Alignment:**
- [ ] Skills in `name/SKILL.md` directory structure
- [ ] YAML frontmatter with `name` and `description`
- [ ] Description is a single informative line
- [ ] Installed to `.claude/skills/` or `~/.claude/skills/`
