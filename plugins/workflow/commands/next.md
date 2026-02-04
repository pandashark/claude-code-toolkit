---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob, TodoWrite]
argument-hint: "[--task ID | --parallel [N|auto] | --preview | --status | --skip-context]"
description: "Execute next task(s) from implementation plan"
---

# Execute Next Task

Execute pending tasks from `.claude/work/ACTIVE_WORK` work unit.

**Arguments**: $ARGUMENTS

## Modes

- `--preview`: List available tasks
- `--status`: Show progress (completed/pending/blocked)
- `--task TASK-ID`: Execute specific task
- `--parallel N`: Execute N independent tasks concurrently
- `--parallel auto`: Execute all independent tasks (max 5)
- `--skip-context`: Skip context-gathering for simple tasks
- *(no args)*: Execute next pending task

## Process

1. **Load State**: Read `ACTIVE_WORK`, verify `state.json` exists with status `planning_complete` or `implementing`

2. **Find Tasks**: Query state.json for pending tasks with satisfied dependencies

3. **Context Gathering** (unless `--skip-context`):
   - Check if context manifest exists at `.claude/work/{unit}/context/TASK-{id}-context.md`
   - If missing, invoke context-gathering agent via Task tool:
     ```
     Task(subagent_type="context-gathering", description="""
     Task ID: {task_id}
     Title: {task_title}
     Description: {task_description}
     Acceptance Criteria:
     - {criterion_1}
     - {criterion_2}
     Work Unit: .claude/work/{unit}
     """)
     ```
   - Wait for agent to complete and verify manifest was created
   - If context gathering fails, report error and do not proceed with task

4. **Execute**:
   - Single task: Work directly on the task (context manifest available for reference)
   - Parallel: Launch Task agents concurrently (single message with multiple Task tool calls)
   - Each task execution should reference its context manifest if one exists

5. **Validate**: Run tests, verify acceptance criteria met

6. **Update State**: Mark task completed in state.json, update `current_task`

7. **Commit**: Create atomic commit with task ID and description

## Context Gathering Details

The context-gathering agent creates a comprehensive context manifest before task execution. This ensures:
- Complete understanding of affected systems
- Documentation of existing patterns and behaviors
- Identification of gotchas and edge cases
- Technical reference for implementation

**When to skip context gathering** (`--skip-context`):
- Simple file edits with clear scope
- Documentation-only changes
- Configuration updates
- Tasks where you already have full context

**Context manifest location**: `.claude/work/{unit}/context/TASK-{id}-context.md`

**Context manifest contents**:
- How the current system works (narrative)
- What needs to change for the task
- Technical reference (files, functions, data structures)
- Gotchas and warnings
- Related tests

## Parallel Execution

For `--parallel`, find independent tasks (no unmet dependencies), launch as concurrent Task agents:
- Context gathering runs for each task before its execution
- Each agent gets: task ID, title, description, acceptance criteria, context manifest path
- Collect results, update state for each
- Handle partial failures gracefully (some succeed, some fail)

## State File Format

```json
{
  "status": "implementing",
  "current_task": "TASK-003",
  "tasks": [
    {"id": "TASK-001", "title": "...", "status": "completed", "dependencies": []},
    {"id": "TASK-002", "title": "...", "status": "pending", "dependencies": ["TASK-001"]}
  ]
}
```

## Error Handling

- No active work unit → "Run /explore first"
- No state.json → "Run /plan first"
- All tasks blocked → Show blocked reasons
- Context gathering fails → Report error, suggest --skip-context if appropriate
- Partial parallel failure → Complete successful tasks, report failures
