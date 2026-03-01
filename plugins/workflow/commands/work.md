---
allowed-tools: [Read, Write, MultiEdit, Bash, Grep]
argument-hint: "[continue|checkpoint|switch|--worktree] [args] OR [active|paused|completed|all]"
description: "Work unit management: list, continue, checkpoint, switch, worktrees"
---

# Work Management

Manage work units: list status, continue work, save checkpoints, switch contexts.

**Input**: $ARGUMENTS

## Commands

| Command | Description |
|---------|-------------|
| `/work` | List all work units |
| `/work active` | List only active units |
| `/work continue` | Resume last active unit |
| `/work continue ID` | Resume specific unit |
| `/work checkpoint` | Save current progress |
| `/work checkpoint "msg"` | Save with message |
| `/work switch ID` | Switch to different unit |
| `/work --worktree create ID` | Create git worktree for work unit |
| `/work --worktree list` | Show all active worktrees |
| `/work --worktree remove ID` | Clean up a worktree |

## List Display

```
📋 WORK UNITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 2025-01-01_01_auth    [implementing]  3/5 tasks (60%)
⏸️  2025-01-01_02_api     [paused]        1/4 tasks (25%)
✅ 2024-12-31_01_setup   [completed]     4/4 tasks (100%)
```

## Operations

### Continue
1. Find target unit (last active or specified ID)
2. Load metadata and state from `.claude/work/{id}/`
3. Set as ACTIVE_WORK
4. Display current task and next steps

### Checkpoint
1. Verify active work unit exists
2. Create checkpoint in `{work_unit}/checkpoints/`
3. Record timestamp, message, and current state

### Switch
1. Auto-checkpoint current work (if any)
2. Validate target work unit exists
3. Set new unit as ACTIVE_WORK
4. Load new context

## Work Unit Location

```
.claude/work/
├── ACTIVE_WORK              # Plain text file containing current unit ID (e.g., 2025-01-15_01_topic)
├── 2025-01-01_01_topic/
│   ├── metadata.json        # Status, timestamps
│   ├── requirements.md
│   ├── state.json           # Task tracking
│   └── checkpoints/
└── 2025-01-01_02_other/
```

## Worktree Operations

Git worktrees provide filesystem isolation for parallel work streams. Each worktree is a separate checkout sharing the same `.git` repository.

### Create
1. Read work unit's `metadata.json` for branch name
2. Create worktree outside main repo:
   ```bash
   git worktree add ../{project}-wt-{id} {branch}
   ```
3. Record worktree path in work unit metadata

### List
1. Run `git worktree list` and cross-reference with work unit metadata
2. Display worktree paths, branches, and associated work units

### Remove
1. Verify work is committed on the worktree branch
2. Remove the worktree:
   ```bash
   git worktree remove ../{project}-wt-{id}
   ```
3. Clean stale references: `git worktree prune`

## Integration

- `/explore` creates new work units
- `/plan` generates state.json
- `/next` executes tasks
- `/ship` completes and archives
- `/team` coordinates parallel sessions across worktrees
