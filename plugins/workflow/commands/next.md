---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob, TodoWrite]
argument-hint: "[--task ID | --parallel [N|auto] | --preview | --status]"
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
- *(no args)*: Execute next pending task

## Process

1. **Load State**: Read `ACTIVE_WORK`, verify `state.json` exists with status `planning_complete` or `implementing`

2. **Find Tasks**: Query state.json for pending tasks with satisfied dependencies

3. **Load Context**: Read the task's context manifest from `.claude/work/{unit}/context/TASK-{id}-context.md`
   - Context manifests are created during `/plan`, so they should already exist
   - If manifest is missing, warn but continue (task may be simple enough to proceed)

4. **Execute**:
   - Single task: Work directly on the task using the context manifest for reference
   - Parallel: Launch Task agents concurrently (single message with multiple Task tool calls)
   - Each task execution should reference its context manifest

5. **Validate**: Run tests, verify acceptance criteria met

6. **Update State**: Mark task completed in state.json, update `current_task`

7. **Commit Task**:
   - Stage all changes related to the task: `git add -A`
   - Create atomic commit using conventional commit format:
     ```
     git commit -m "feat|fix|refactor: {task_title}

     {task_description}

     Work: {work_unit_id} | Task: {task_id}
     Acceptance criteria:
     - {criterion_1}
     - {criterion_2}"
     ```
   - Choose commit type based on task type:
     - `feat:` for new features
     - `fix:` for bug fixes
     - `refactor:` for code restructuring
     - `docs:` for documentation
     - `test:` for test additions
   - If commit fails (e.g., pre-commit hooks), report error and keep task as `in_progress`
   - On success, record commit SHA in state.json for the task

## Context Manifests

Context manifests are created during `/plan` by the context-gathering agent. Each task has a pre-generated manifest at `.claude/work/{unit}/context/TASK-{id}-context.md` containing:
- How the current system works (narrative)
- What needs to change for the task
- Technical reference (files, functions, data structures)
- Gotchas and warnings
- Related tests

## Parallel Execution

For `--parallel`, find independent tasks (no unmet dependencies), launch as concurrent Task agents:
- Each agent gets: task ID, title, description, acceptance criteria, context manifest path
- Collect results, update state for each
- Handle partial failures gracefully (some succeed, some fail)

## State File Format

```json
{
  "status": "implementing",
  "base_branch": "main",
  "work_branch": "feature/user-auth",
  "current_task": "TASK-003",
  "tasks": [
    {"id": "TASK-001", "title": "...", "status": "completed", "dependencies": [], "commit_sha": "abc123"},
    {"id": "TASK-002", "title": "...", "status": "pending", "dependencies": ["TASK-001"], "commit_sha": null}
  ]
}
```

## Error Handling

- No active work unit → "Run /explore first"
- No state.json → "Run /plan first"
- All tasks blocked → Show blocked reasons
- Missing context manifest → Warn and continue, or suggest re-running /plan
- Partial parallel failure → Complete successful tasks, report failures
