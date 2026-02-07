---
allowed-tools: [Read, Write, Edit, Bash]
argument-hint: "[--all | --pr-review | --issue-triage | --code-changes]"
description: Scaffold GitHub Actions workflows for Claude Code CI (PR review, issue triage, code changes)
---

# CI Setup

Install GitHub Actions workflow templates that integrate Claude Code into your CI/CD pipeline for automated PR reviews, issue triage, and code changes.

## Available Workflows

| Workflow | File | Trigger | What It Does |
|----------|------|---------|-------------|
| **PR Review** | `claude-pr-review.yml` | `pull_request`, `issue_comment` (@claude) | Reviews PRs for bugs, security issues, and code quality |
| **Issue Triage** | `claude-issue-triage.yml` | `issues` (opened) | Analyzes new issues, suggests relevant files and approach |
| **Code Changes** | `claude-code-changes.yml` | `issue_comment` (@claude) | Makes code changes and opens PRs from issue comments |

## Installation Steps

### Step 1: Determine which workflows to install

Check the argument provided by the user:
- `--all`: Install all 3 workflows
- `--pr-review`, `--issue-triage`, `--code-changes`: Install only that workflow
- No argument: Ask the user which workflows they want (list the table above), allow multiple selections

### Step 2: Check prerequisites

```bash
[ -d ".git" ] && echo "Git repo: yes" || echo "Warning: not a git repository"
```

If `.github/workflows/` doesn't exist, create it:
```bash
mkdir -p .github/workflows
```

Check for existing Claude workflows to avoid duplicates. If any of the target filenames already exist, warn the user and ask before overwriting.

### Step 3: Read the workflow templates

The templates are shipped with this plugin at `plugins/setup/assets/ci/` (relative to the toolkit root).

Find the plugin directory by reading `.claude/settings.json` and looking at the `extraKnownMarketplaces` path, then append `setup/assets/ci/`. Read each selected template YAML file.

### Step 4: Write workflows to target project

For each selected workflow, write the template file to `.github/workflows/` in the target project. The files should be exact copies of the templates.

### Step 5: Verify

Validate that the written workflow files exist and are not empty:
```bash
ls -la .github/workflows/claude-*.yml
```

### Step 6: Report

Print a summary:
- Which workflows were installed
- Remind user to add `ANTHROPIC_API_KEY` to GitHub repository secrets: Settings > Secrets and variables > Actions > New repository secret
- Note that the `claude-pr-review` workflow responds to `@claude` comments on PRs
- Note that the `claude-code-changes` workflow responds to `@claude` comments on issues
- Suggest customizing the `direct_prompt` and `model` fields in each workflow
