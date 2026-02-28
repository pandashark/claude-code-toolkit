# Workflow Plugin

Structured development workflow for systematic task completion - explore, plan, implement, and deliver.

## Overview

The Workflow plugin provides a proven 4-phase development methodology for Claude Code. It guides you from initial requirements exploration through systematic planning, task execution, and final delivery. This workflow ensures thorough analysis, organized implementation, and quality delivery.

### Relationship to Claude's Built-in Plan Mode

Claude Code includes a built-in `EnterPlanMode` that provides enhanced reasoning for planning. **Our workflow complements it**:

| Feature | Built-in Plan Mode | Our Workflow |
|---------|-------------------|--------------|
| **Storage** | Global `~/.claude/plans/` | Project-local `.claude/work/` |
| **Naming** | Auto-generated (`zany-cooking-wombat`) | Date-based (`2025-11-27_01_feature`) |
| **Execution** | Implements entire plan at once | Incremental via `/next` |
| **State tracking** | None | `state.json` with task progress |
| **Session resume** | Cannot resume mid-plan | Work units persist across handoffs |
| **Parallel execution** | No | `/next --parallel 3` |

**Best practice**: Use Claude's built-in plan mode *during* `/explore` or `/plan` for enhanced reasoning, while our workflow handles project-local storage and incremental execution. The two work together—you get better planning *and* better organization.

## The 4-Phase Workflow

```
/explore → /plan → /next (repeat) → /ship
   ↓         ↓          ↓             ↓
Analyze   Design   Implement      Deliver
```

### Phase 1: Explore
Understand requirements, analyze codebase, identify constraints and opportunities.

### Phase 2: Plan
Create detailed implementation plan with ordered tasks, dependencies, and acceptance criteria.

### Phase 3: Execute
Implement tasks one at a time with /next, completing the plan systematically.

### Phase 4: Deliver
Ship completed work with validation, documentation, and quality assurance.

## Commands

### `/explore [source] [--work-unit ID]`
Explore requirements and codebase with systematic analysis before planning. This is Anthropic's recommended first step for any significant task.

**What it does**:
- Analyzes requirements from multiple sources (@file, #issue, description, or interactive)
- Explores relevant codebase areas to understand context
- Identifies constraints, dependencies, and risks
- Documents findings for planning phase
- Creates work unit for tracking

**Usage**:
```bash
/explore                                    # Interactive exploration
/explore "Add user authentication"          # From description
/explore @requirements.md                   # From requirements doc
/explore #123                               # From GitHub issue
/explore --work-unit 001                    # Use existing work unit
```

**Thoroughness Levels**:
- `quick`: Basic search and analysis (5-10 minutes)
- `medium`: Moderate exploration with multiple angles (15-25 minutes)
- `very thorough`: Comprehensive analysis across codebase (30-45 minutes)

**Output**:
- `exploration.md`: Detailed findings and analysis
- `metadata.json`: Work unit tracking information

**When to use**:
- ✅ Starting any non-trivial feature or bug fix
- ✅ Unclear requirements that need investigation
- ✅ Unfamiliar codebase areas
- ✅ Complex changes with many dependencies

**When to skip**:
- ❌ Trivial changes (typo fixes, simple updates)
- ❌ Very clear requirements in familiar code
- ❌ Quick experiments or spikes

### `/plan [--from-requirements | --from-issue #123 | description]`
Create detailed implementation plan with ordered tasks and dependencies using structured reasoning.

**What it does**:
- Reviews exploration findings (or analyzes requirements directly)
- **Creates feature branch** (`work/{unit-id}`) from current branch
- Breaks work into ordered, manageable tasks
- Identifies dependencies and sequencing
- Defines acceptance criteria for each task
- Creates task tracking state file
- **Gathers context for all tasks** (via context-gathering agent)

**Usage**:
```bash
/plan                                       # From latest /explore
/plan --from-requirements @specs.md         # From requirements doc
/plan --from-issue #123                     # From GitHub issue
/plan "Implement OAuth login"               # From description
```

**Plan Structure**:
- **Tasks**: Ordered list with IDs, descriptions, dependencies
- **Dependencies**: Task relationships and sequencing
- **Acceptance Criteria**: How to verify completion
- **Risks**: Potential issues and mitigation strategies
- **Estimates**: Rough time/complexity estimates

**Output**:
- `implementation-plan.md`: Complete task breakdown
- `state.json`: Task tracking state (pending, in_progress, completed)
- `context/TASK-{id}-context.md`: Context manifests for each task
- Git branch: `feature/{description}` (e.g., `feature/user-auth`)

**When to use**:
- ✅ After /explore for complex work
- ✅ Multi-step features requiring coordination
- ✅ Changes affecting multiple files/systems
- ✅ Work that will span multiple sessions

**When to skip**:
- ❌ Single-file, single-function changes
- ❌ Immediate fixes that are obvious
- ❌ Exploratory work without clear endpoint

### `/next [--task TASK-ID | --preview | --status]`
Execute the next available task from the implementation plan.

**What it does**:
- Loads implementation plan and current state
- Identifies next task based on dependencies
- Loads the task's pre-generated context manifest
- Executes the task completely
- **Commits completed task** with task ID in message
- Updates state.json automatically
- Moves to next task when ready

**Usage**:
```bash
/next                                       # Execute next available task
/next --preview                             # Show what's next without executing
/next --status                              # Show plan progress
/next --task TASK-005                       # Execute specific task
/next --parallel auto                       # Execute independent tasks in parallel
```

**Task Execution Flow**:
1. Load plan and check dependencies
2. Display current task details
3. Load context manifest (created during `/plan`)
4. Execute implementation with context manifest available
5. Verify completion against acceptance criteria
6. **Commit task**: conventional commit with work unit + task reference in body
7. Update state.json (pending → in_progress → completed)
8. Show progress and next task

#### Context Manifests

Context manifests are created during `/plan` by the context-gathering agent. Each task has a pre-generated manifest containing:
- Complete understanding of affected code paths
- Knowledge of integration points and dependencies
- Awareness of error handling and edge cases
- Technical reference details (signatures, schemas, configs)

**Context manifest location**: `.claude/work/{unit}/context/TASK-{id}-context.md`

**States**:
- `pending`: Not yet started
- `in_progress`: Currently working on
- `completed`: Finished and verified
- `blocked`: Waiting on dependencies

**When to use**:
- ✅ Systematic implementation of planned work
- ✅ Multiple tasks that should be done in order
- ✅ Work that needs tracking across sessions
- ✅ Complex features with many steps

**Tips**:
- Run `/next --status` frequently to see progress
- Use `/next --preview` before starting if unsure
- Tasks complete in dependency order automatically

### `/ship [--preview | --pr | --merge] [--squash]`
Deliver completed work with validation and comprehensive documentation.

**What it does**:
- Reviews completed implementation plan
- Validates all acceptance criteria met
- Runs tests and quality checks
- Creates comprehensive documentation
- **Merges or creates PR** to base branch
- Produces delivery summary

**Usage**:
```bash
/ship --preview                             # Preview what will be delivered
/ship --pr                                  # Create pull request (keeps task commits)
/ship --pr --squash                         # Create PR with squash recommendation
/ship --merge                               # Merge to base branch (keeps task commits)
/ship --merge --squash                      # Squash all tasks into single commit, merge
/ship --deploy                              # Prepare for deployment
```

**Delivery Checklist**:
- ✅ All planned tasks completed
- ✅ Tests passing
- ✅ Code reviewed (self or automated)
- ✅ Documentation updated
- ✅ Breaking changes documented
- ✅ Migration guides (if needed)

**Output**:
- `COMPLETION_SUMMARY.md`: What was delivered and how to use it
- Git commit or pull request (if requested)
- Test results and quality metrics
- Deployment instructions (if applicable)

**When to use**:
- ✅ Implementation plan complete
- ✅ Feature ready for review/merge
- ✅ All acceptance criteria met
- ✅ Quality checks passed

**Options**:
- `--preview`: See what will be shipped without doing it
- `--pr`: Create GitHub pull request to base branch
- `--merge`: Merge work branch directly to base branch
- `--squash`: Combine all task commits into single commit (use with --pr or --merge)
- `--deploy`: Include deployment checklist and instructions

### `/work [subcommand] [args]`
Unified work management - list units, continue work, save checkpoints, and switch contexts.

**What it does**:
- Lists active, paused, and completed work units
- Continues work from previous sessions
- Creates checkpoints for context switching
- Switches between parallel work streams

**Usage**:
```bash
/work                                      # List all work units
/work continue                             # Resume last active work unit
/work checkpoint "Switching to bug fix"    # Save checkpoint before context switch
/work switch 002                           # Switch to work unit 002
/work active                               # Show only active work units
/work completed                            # Show completed work units
```

**When to use**:
- ✅ Managing multiple parallel work streams
- ✅ Context switching between tasks
- ✅ Resuming work after interruptions
- ✅ Tracking work unit status

### `/spike [topic] [timebox]`
Time-boxed exploration in isolated branch for investigating uncertain approaches.

**What it does**:
- Creates isolated git branch for experimentation
- Time-boxes exploration (default: 2 hours)
- Documents findings and recommendations
- Easy to merge or discard results

**Usage**:
```bash
/spike "GraphQL vs REST API" 2h            # 2-hour spike
/spike "Redis caching strategy" 1h         # 1-hour spike
/spike "New authentication library"        # Default 2-hour spike
```

**Output**:
- Isolated git branch (`spike/topic-name`)
- Findings document with recommendations
- Code examples (if applicable)
- Decision: proceed, modify, or abandon

**When to use**:
- ✅ High uncertainty in approach
- ✅ Need to compare multiple solutions
- ✅ Investigating new libraries or patterns
- ✅ Risk mitigation before committing to design

**Benefits**:
- Isolated from main work (git branch)
- Time-boxed to prevent rabbit holes
- Documented findings for future reference
- Easy to discard if approach doesn't work

## Git Workflow

The workflow plugin integrates git operations throughout the development lifecycle:

```
/plan                    /next (×N)                    /ship
   │                         │                            │
   ▼                         ▼                            ▼
Create branch ──────► Commit per task ──────► PR or merge to base
work/{unit-id}        TASK-001: ...                      │
                      TASK-002: ...              ┌───────┴───────┐
                      TASK-003: ...              ▼               ▼
                                            Keep commits    Squash all
```

**Branch naming**: `feature/{description}` (e.g., `feature/user-auth`)

**Task commits**: Each `/next` creates an atomic commit using conventional commits:
```
feat: Add password hashing to User model

Implemented bcrypt hashing for user passwords with configurable rounds.

Work: 2025-01-15_01_user-auth | Task: TASK-001
Acceptance criteria:
- Passwords hashed before storage
- Existing passwords can be verified
```

**Delivery options**:
- `--pr`: Push branch, create PR (reviewers merge with their preferred strategy)
- `--merge`: Merge locally (keeps task commit history)
- `--merge --squash`: Combine all tasks into single commit, then merge

## Complete Workflow Example

### Example: Adding User Authentication

```bash
# Phase 1: Explore (on main branch)
/explore "Add JWT-based authentication to API"
# Output: exploration.md with findings

# Phase 2: Plan
/plan
# Creates branch: feature/jwt-auth
# Output: implementation-plan.md with 6 tasks
# Output: context manifests for each task

# Phase 3: Execute
/next --status
# Shows: TASK-001 ready, others pending

/next
# Implements TASK-001
# Commits: "feat: Add password hashing to User model"

/next
# Implements TASK-002
# Commits: "feat: Create JWT token generation utilities"

/next
# ... continues through all tasks
# Each task = one commit on work branch

# Phase 4: Deliver
/ship --pr
# Pushes feature/jwt-auth to origin
# Creates PR to main with:
# - Summary of 6 completed tasks
# - Test results (all passing)
# - Link to implementation plan
```

**Alternative delivery** (local merge with squash):
```bash
/ship --merge --squash
# Squashes all 6 task commits into one
# Merges to main
# Deletes work branch
```

## Integration with Other Plugins

### System Plugin
- Uses `/status` to show plan progress
- Uses `/setup` for project initialization
- Uses `/audit` for framework compliance

### Agents Plugin
- Uses `/agent` for specialized exploration and analysis
- Uses `/serena` for semantic code understanding

### Development Plugin
- `/test` runs during /ship validation
- `/review` provides code quality feedback
- `/fix` helps resolve issues found during execution

### Memory Plugin
- Auto-loads memory context via @imports
- Preserves decisions in `decisions.md`
- Documents lessons in `lessons_learned.md`

### Git Plugin
- `/ship --commit` uses `/git commit`
- `/ship --pr` uses `/git pr`
- Automatic commit message generation

## Agents

### Context-Gathering Agent

The workflow plugin includes a **context-gathering agent** that runs automatically during `/plan`. This agent creates comprehensive "Context Manifests" for all tasks upfront.

**What it does**:
- Researches codebase to understand affected systems
- Documents "How it currently works" with narrative explanations
- Identifies "What needs to change" for the specific task
- Provides technical reference (signatures, schemas, configs)
- Lists gotchas, warnings, and edge cases

**Context Manifest Structure**:
```markdown
## Context Manifest

### How This Currently Works
[Narrative explanation of current system behavior]

### What Needs to Change for This Task
[Specific modifications needed]

### Technical Reference
- Key files and their purposes
- Function signatures
- Data structures
- Configuration requirements

### Gotchas and Warnings
- Edge cases to handle
- Performance considerations
```

**Benefits**:
- Prevents implementation errors from missing context
- All context gathered upfront during planning
- Each task has targeted, specific context
- Reduces back-and-forth during implementation

## Work Unit Structure

The workflow creates and maintains this structure:

```
.claude/work/[work-unit]/
├── metadata.json              # Work unit metadata
├── exploration.md             # /explore findings
├── implementation-plan.md     # /plan task breakdown
├── state.json                 # /next task tracking (includes git info)
├── context/                   # Per-task context manifests
│   ├── TASK-001-context.md
│   ├── TASK-002-context.md
│   └── ...
└── COMPLETION_SUMMARY.md      # /ship delivery summary
```

**state.json** includes git tracking:
```json
{
  "status": "implementing",
  "base_branch": "main",
  "work_branch": "feature/user-auth",
  "tasks": [
    {"id": "TASK-001", "status": "completed", "commit_sha": "abc123..."},
    {"id": "TASK-002", "status": "in_progress", "commit_sha": null}
  ]
}
```

## Configuration

### Exploration Defaults (`.claude/config.json`)
```json
{
  "workflow": {
    "explore": {
      "defaultThoroughness": "medium",
      "autoCreateWorkUnit": true,
      "explorationAgent": "Explore"
    }
  }
}
```

### Planning Defaults
```json
{
  "workflow": {
    "plan": {
      "useSequentialThinking": true,
      "includeTestTasks": true,
      "includeDocTasks": true
    }
  }
}
```

### Delivery Defaults
```json
{
  "workflow": {
    "ship": {
      "requireTests": true,
      "requireDocs": true,
      "autoCommit": false,
      "autoPR": false
    }
  }
}
```

## Dependencies

### Required Plugins
- **claude-code-system** (^1.0.0): System status and configuration
- **claude-code-memory** (^1.0.0): Memory context loading

### Optional MCP Tools
- **Sequential Thinking**: Enhanced planning and exploration analysis
- **Serena**: Semantic code understanding for exploration
- **Firecrawl**: Web research for requirements gathering

**Graceful Degradation**: All commands work without MCP tools.

## Best Practices

### When to Use Full Workflow

✅ **Use /explore → /plan → /next → /ship for**:
- Multi-file features
- Unfamiliar codebase areas
- Complex business logic
- Work spanning multiple sessions
- Team collaboration (plan serves as spec)

### When to Skip Workflow

❌ **Skip workflow for**:
- Single-line fixes
- Documentation updates
- Typo corrections
- Configuration tweaks
- Quick experiments

### Workflow Variations

**Quick Mode** (skip /explore):
```bash
/plan "Simple, clear task"
/next
/ship --commit
```

**Investigation Mode** (explore only):
```bash
/explore "Complex problem"
# Review findings, decide approach
# May not lead to implementation
```

**Iterative Mode** (re-plan as you learn):
```bash
/explore
/plan
/next
# Discover new requirements
/plan --update  # Adjust plan
/next
/ship
```

## Troubleshooting

### /explore finds nothing
- Broaden search terms
- Use `very thorough` mode
- Manually specify file patterns to search
- Check if you're in correct directory

### /plan creates too many tasks
- Tasks should be 30min - 2hr each
- Merge small tasks
- Use subtasks in descriptions

### /next shows "no tasks available"
- Run `/next --status` to check dependencies
- Tasks may be blocked waiting on others
- Check `state.json` for task states

### /ship validation fails
- Review acceptance criteria in plan
- Run tests manually: `/test`
- Check code quality: `/review`
- Fix issues: `/fix`

## Metrics and Success

The workflow tracks:
- **Exploration time**: How long /explore takes
- **Task completion rate**: Completed vs. total tasks
- **Plan accuracy**: How often plan matches reality
- **Quality metrics**: Test coverage, review feedback

View with:
```bash
/status verbose
/performance
```

## Examples

See `examples/` directory for complete workflow examples:
- `examples/feature-development/` - Full feature workflow
- `examples/bug-fix/` - Systematic bug resolution
- `examples/refactoring/` - Code improvement workflow

## Support

- **Documentation**: [Workflow Guide](../../docs/guides/workflow.md)
- **Issues**: [GitHub Issues](https://github.com/applied-artificial-intelligence/claude-code-toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/applied-artificial-intelligence/claude-code-toolkit/discussions)

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

**Version**: 1.0.0
**Category**: Workflow
**Dependencies**: core (^1.0.0), memory (^1.0.0)
**MCP Tools**: Optional (sequential-thinking, serena, firecrawl)
