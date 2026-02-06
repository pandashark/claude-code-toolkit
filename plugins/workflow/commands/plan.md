---
allowed-tools: [Task, Bash, Read, Write, Grep, MultiEdit, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[--from-requirements | --from-issue #123 | description]"
description: "Create implementation plan with ordered tasks and dependencies"
---

# Implementation Planning

Create comprehensive task breakdown from requirements.

**Input**: $ARGUMENTS

## MANDATORY REQUIREMENTS

**Execute ALL steps in order. Do NOT skip steps based on perceived task simplicity.**

- [ ] Step 1: Validate context
- [ ] Step 2: Create feature branch
- [ ] Step 3-5: Analyze and create task breakdown
- [ ] Step 6: Generate output files
- [ ] Step 7: Run context-gathering agents for ALL tasks

**Before declaring "Planning Complete", verify:**
1. Feature branch exists and is checked out
2. `state.json` contains `base_branch` and `work_branch`
3. `context/` directory exists with manifest for each task
4. Each task in `state.json` has `context_manifest` path populated

## Sources

- `--from-requirements`: Use existing requirements.md
- `--from-issue #123`: Plan for GitHub issue
- `description`: Plan from provided text
- *(empty)*: Plan for active work unit

## Process (Execute ALL Steps)

1. **Validate Context**
   - Check for active work unit in `.claude/work/ACTIVE_WORK`
   - Verify `requirements.md` exists
   - Warn if overwriting existing plan

2. **Create Feature Branch** *(REQUIRED)*
   - Check git status for uncommitted changes
   - If dirty: warn user and ask to stash or commit first
   - Record current branch as `base_branch` in metadata.json
   - Extract description from work unit ID (e.g., `2025-01-15_01_user-auth` → `user-auth`)
   - Create and checkout branch: `git checkout -b feature/{description}`
   - Record `work_branch` in metadata.json
   - Example: `feature/user-auth`

3. **Analyze Requirements**
   - Identify core functionality
   - Map integration points
   - Define quality requirements
   - Use Sequential Thinking for complex analysis

4. **Create Task Breakdown**
   - 2-4 hours per task
   - Single responsibility per task
   - Clear acceptance criteria
   - Testable outcomes

5. **Sequence Tasks**
   - Map dependencies (no circular refs)
   - Identify parallel opportunities
   - Define critical path

6. **Generate Outputs**
   - Write `implementation-plan.md` and `state.json`

7. **Gather Context for All Tasks** *(REQUIRED - Do not skip)*
   - Create `context/` directory in work unit
   - For EACH task, invoke context-gathering agent via Task tool:
     ```
     Task(subagent_type="context-gathering", prompt="""
     Task ID: {task_id}
     Title: {task_title}
     Description: {task_description}
     Acceptance Criteria:
     - {criterion_1}
     - {criterion_2}
     Work Unit: .claude/work/{unit}
     """)
     ```
   - Run context gathering for multiple tasks in parallel when possible
   - Each manifest written to: `.claude/work/{unit}/context/TASK-{id}-context.md`
   - Update `state.json` task entries with `context_manifest` path and `context_gathered_at` timestamp

## Task Sizing

| Type | Scope |
|------|-------|
| Foundation | Setup, infrastructure, core architecture |
| Feature | User-facing functionality |
| Integration | External systems, APIs |
| Testing | Test implementation |
| Documentation | Guides, API docs |

## Output Files

**state.json**:
```json
{
  "status": "planning_complete",
  "base_branch": "main",
  "work_branch": "feature/user-auth",
  "current_task": null,
  "tasks": [
    {
      "id": "TASK-001",
      "title": "Setup foundation",
      "type": "foundation",
      "status": "pending",
      "dependencies": [],
      "acceptance_criteria": ["..."],
      "estimated_hours": 3,
      "priority": "high",
      "context_manifest": null,
      "context_gathered_at": null
    }
  ],
  "completed_tasks": [],
  "next_available": ["TASK-001"]
}
```

**Note**: Context fields are populated during planning when the context-gathering agent runs. This ensures all context is gathered upfront before execution begins.

**implementation-plan.md**: Human-readable plan with:
- Project overview and scope
- Technical architecture
- Task execution plan
- Quality assurance strategy

## Completion Checklist

Before reporting "Planning Complete", verify ALL items:

```
[ ] On feature branch (not main/master)
[ ] metadata.json has base_branch and work_branch
[ ] state.json has base_branch and work_branch fields
[ ] context/ directory exists
[ ] Context manifest exists for EACH task
[ ] Each task in state.json has context_manifest path
[ ] Each task in state.json has context_gathered_at timestamp
```

**If any item is missing, complete it before proceeding.**

## Next Steps

After planning completes (including context gathering): Run `/next` to start first task
