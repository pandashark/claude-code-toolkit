---
allowed-tools: [Read, Write, Bash, Grep, Glob]
argument-hint: "[start|status|merge] [--tasks T1,T2] [--worktrees]"
description: "Coordinate agent teams for parallel multi-session development"
---

# Agent Team Coordination

Break work into parallel streams for multiple Claude Code sessions. Uses git worktrees for filesystem isolation.

**Input**: $ARGUMENTS

## Commands

| Command | Description |
|---------|-------------|
| `/team start` | Assign available tasks to parallel sessions |
| `/team start --tasks T1,T2,T3` | Assign specific tasks |
| `/team start --worktrees` | Also create git worktrees for each session |
| `/team status` | Show team progress across sessions |
| `/team merge` | Reconcile completed work from all sessions |

## Process

### Start

1. Read `state.json` from the active work unit
2. Identify parallelizable tasks from `next_available` (tasks with all dependencies satisfied)
3. If `--tasks` specified, use those; otherwise select all available
4. Create `.claude/work/{id}/team/` directory with:
   - `assignments.json`: Maps tasks to session slots (session-1, session-2, etc.)
   - `status.json`: Tracks per-session progress
5. If `--worktrees` specified, create a git worktree for each session:
   ```bash
   git worktree add ../{project}-wt-{session} -b team/{work-unit}/{session}
   ```
6. Print launch instructions:
   - One terminal command per session
   - Each session should run `/work continue {id}` then `/next --task {assigned-task}`

### Status

1. Read `team/assignments.json` and `team/status.json`
2. If worktrees exist, check each worktree's `state.json` for task completion
3. Display progress table:
   ```
   TEAM STATUS — {work-unit}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   session-1  TASK-002  completed   abc1234
   session-2  TASK-003  in_progress —
   session-3  TASK-004  pending     —
   ```

### Merge

1. Verify all assigned tasks are completed
2. For each worktree session:
   ```bash
   git merge team/{work-unit}/{session} --no-ff
   ```
3. Update main `state.json` with completed task statuses and commit SHAs
4. Clean up worktrees:
   ```bash
   git worktree remove ../{project}-wt-{session}
   git branch -d team/{work-unit}/{session}
   ```
5. Remove `team/` directory from work unit

## Assignments File Format

```json
{
  "created_at": "2026-01-15T10:00:00Z",
  "sessions": {
    "session-1": { "task": "TASK-002", "worktree": "../project-wt-session-1", "branch": "team/unit/session-1" },
    "session-2": { "task": "TASK-003", "worktree": "../project-wt-session-2", "branch": "team/unit/session-2" }
  }
}
```

## Integration

- `/plan` creates tasks and dependencies that `/team` reads
- `/work --worktree` provides low-level worktree operations
- `/next` executes tasks within each session
- `/ship` delivers after `/team merge` reconciles all work
