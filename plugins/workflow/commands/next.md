---
allowed-tools: [Task, Bash, Read, Write, Edit, MultiEdit, Grep, Glob, TodoWrite, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols, mcp__serena__replace_symbol_body]
argument-hint: "[--task ID | --parallel [N|auto] | --preview | --status | --no-review]"
description: "Execute next task(s) with automated review, fix, and test cycle"
---

# Execute Next Task

Execute pending tasks from `.claude/work/ACTIVE_WORK` work unit, then automatically review, fix, and test before committing.

**Arguments**: $ARGUMENTS

## Modes

- `--preview`: List available tasks
- `--status`: Show progress (completed/pending/blocked)
- `--task TASK-ID`: Execute specific task
- `--parallel N`: Execute N independent tasks concurrently
- `--parallel auto`: Execute all independent tasks (max 5)
- `--no-review`: Skip the review-fix-test cycle (commit immediately after validation)
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

6. **Review** *(skip with `--no-review`)*:
   - Invoke `/development:review` on all files changed by this task
   - Focus on: bugs, design issues, dead code, quality, performance
   - Capture review output for the fix step

7. **Fix** *(skip with `--no-review`)*:
   - Invoke `/development:fix all` to apply fixes from the review
   - Addresses critical issues first, then important, then minor
   - Re-run tests after fixes to ensure nothing broke

8. **Test** *(skip with `--no-review`)*:
   - Invoke `/development:test tdd` for full TDD validation
   - RED-GREEN-REFACTOR cycle for any gaps found
   - Verify coverage >= 80% threshold
   - All tests must pass before proceeding to commit

9. **Update State**: Mark task completed in state.json, update `current_task`

10. **Commit Task**:
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

## Quality Gate (Review-Fix-Test)

The automated quality gate between implementation and commit ensures every task is:

1. **Reviewed** — catches bugs, design flaws, and dead code before they land
2. **Fixed** — applies all actionable fixes from the review automatically
3. **Tested** — validates with TDD discipline (coverage, edge cases, regressions)

If the cycle reveals issues that cannot be auto-fixed:
- Report the issues clearly
- Keep the task as `in_progress`
- Do NOT commit broken or unreviewed code

Use `--no-review` to skip the quality gate when speed matters more than thoroughness (e.g., docs-only changes, trivial fixes).

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
- Each agent runs its own review-fix-test cycle before reporting completion (unless `--no-review`)
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
- Review finds unfixable critical issues → Keep task `in_progress`, report findings
- Test coverage below 80% after fix cycle → Keep task `in_progress`, report gaps
