---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob]
argument-hint: "[--preview | --pr [--squash] | --merge [--squash] | --deploy]"
description: "Deliver completed work with validation and documentation"
---

# Work Delivery

Validate, document, and deliver completed work.

**Options**: $ARGUMENTS

## Modes

- `--preview`: Show what would be delivered (no changes)
- `--pr`: Create pull request to base branch
- `--pr --squash`: Create PR with recommendation to squash on merge
- `--merge`: Merge work branch directly to base branch (keeps task commits)
- `--merge --squash`: Squash all task commits into single commit, then merge
- `--deploy`: Prepare for production deployment

## Process

1. **Readiness Check**
   - Find active work unit
   - Verify all tasks completed
   - Read `base_branch` and `work_branch` from state.json
   - Check git status (must be clean - all tasks should be committed)
   - Verify on correct work branch

2. **Quality Validation**
   - Run test suite (>80% coverage required)
   - Execute linting/type checking
   - Security scan
   - Build verification

3. **Generate Summary**
   - Write `COMPLETION_SUMMARY.md` in work unit directory
   - Content: tasks completed, key decisions, what was delivered
   - Commit to work branch

4. **Execute Delivery**

   **For `--pr`:**
   - Push work branch to remote: `git push -u origin {work_branch}`
   - Create PR via `gh pr create`:
     - Base: `{base_branch}`
     - Title: Work unit title or first task title
     - Body: Summary of all tasks completed, link to implementation plan
   - If `--squash`: Add note in PR description recommending squash merge

   **For `--merge`:**
   - Checkout base branch: `git checkout {base_branch}`
   - Pull latest: `git pull origin {base_branch}`
   - If `--squash`:
     - Squash merge: `git merge --squash {work_branch}`
     - Create single commit with summary of all tasks
   - Else:
     - Regular merge: `git merge {work_branch}` (preserves task commits)
   - Delete work branch: `git branch -d {work_branch}`

   **For `--deploy`:**
   - Final validation, env config, monitoring setup

5. **Memory Reflection**
   - Analyze work unit for learnings
   - Prompt for `/memory-update` to capture:
     - Decisions made
     - Lessons learned
     - New conventions
     - Dependencies added

6. **Archive Work Unit**
   - Update status to completed
   - Record delivery method
   - Move to archives

## Quality Gates

All must pass:
- ✅ Tests pass with >80% coverage
- ✅ No critical lint/security issues
- ✅ Documentation complete
- ✅ Build successful

## Commit Formats

**Task commits** (created by `/next`):
```
feat: Add password hashing to User model

Implemented bcrypt hashing for user passwords with configurable rounds.

Work: 2025-01-15_01_user-auth | Task: TASK-001
Acceptance criteria:
- Passwords hashed before storage
- Existing passwords can be verified
```

**Squash commit** (created by `/ship --merge --squash`):
```
feat|fix|docs: {work unit title}

Implemented:
- TASK-001: {title}
- TASK-002: {title}
- TASK-003: {title}

{Summary of changes}
```

## Branch Cleanup

After successful delivery:
- `--pr`: Work branch remains until PR is merged (remote handles cleanup)
- `--merge`: Work branch deleted locally after merge
- Optionally delete remote work branch: `git push origin --delete {work_branch}`
