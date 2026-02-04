# Sample CLAUDE.md

Copy this to `~/.claude/CLAUDE.md` and customize for your workflow.

---

# My Claude Code Setup

## Quick Reference

## Workflow Requirement

**For non-trivial tasks, ALWAYS use the planning workflow before implementing.**

Run `/plan` BEFORE writing code when:
- The task affects multiple files or systems
- You're working in unfamiliar codebase areas
- The requirements are unclear or complex
- The work may span multiple sessions

Skip planning ONLY for trivial changes:
- Single-line typo fixes
- Documentation-only updates
- Simple configuration tweaks

When in doubt, plan first.

**Workflow**: `/workflow:explore` -> `/workflow:plan` -> `/workflow:next` -> `/workflow:ship`

**Common Commands**:
- `/system:status` - Check project state
- `/development:analyze` - Understand codebase
- `/development:review` - Code review
- `/memory:handoff` - Session handoff

## Project Preferences

- Prefer simple solutions over clever ones
- Run tests before committing
- Use conventional commits

## Context Management

Check context usage: `/context`
- <70%: Continue normally
- 70-80%: Plan handoff at next milestone
- >80%: Create handoff now

## Git Workflow

Use `git safe-commit` or standard git commands.
Commit early, commit often.

---

*Customize this file with your preferences, project context, and workflow notes.*
