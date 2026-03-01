---
allowed-tools: [Read, Write, Bash]
argument-hint: "[--force]"
description: Configure enterprise-managed Claude Code policies for organization-wide deployment
---

# Enterprise Policy Setup

Generate enterprise policy templates for organization-wide Claude Code deployment. Creates managed configuration files that administrators distribute via MDM, config management, or policy repos.

**Input**: $ARGUMENTS

## What It Creates

### Step 1: Create enterprise policy directory

```bash
mkdir -p .claude/policies
```

### Step 2: Generate enterprise CLAUDE.md template

Write `.claude/policies/enterprise-CLAUDE.md` with organization-level rules:

```markdown
# [Organization Name] — Claude Code Policy

## Required Practices
- All code changes must reference a ticket (JIRA, Linear, GitHub Issue)
- Use conventional commits format: type(scope): description
- Never commit secrets, API keys, credentials, or PII
- All PRs require at least one human review before merge

## Coding Standards
- Follow language-specific style guides enforced by CI
- Write tests for all new functionality (minimum 80% coverage for new code)
- Document public APIs and non-obvious logic

## Forbidden Operations
- No force-push to main/master/release branches
- No disabling of pre-commit hooks (--no-verify)
- No sudo or elevated privilege commands
- No direct database modifications in production

## Security Requirements
- Dependencies must be from approved registries only
- No eval(), exec(), or dynamic code execution from user input
- All HTTP endpoints require authentication
- Sensitive data must be encrypted at rest and in transit
```

### Step 3: Generate managed settings.json template

Write `.claude/policies/managed-settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Bash(sudo *)",
      "Bash(rm -rf *)",
      "Bash(rm -r *)",
      "Bash(chmod 777 *)",
      "Bash(git push --force *)",
      "Bash(git push * --force *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "input=$(cat); cmd=$(echo \"$input\" | jq -r '.tool_input.command // empty'); if echo \"$cmd\" | grep -qE '\\-\\-no-verify'; then echo 'POLICY: --no-verify is not allowed by organization policy' >&2; exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

### Step 4: Generate deployment guide

Write `.claude/policies/DEPLOYMENT.md`:

```markdown
# Enterprise Deployment Guide

## Distribution Methods

### MDM (Jamf, Intune)
1. Deploy `enterprise-CLAUDE.md` to `~/.claude/CLAUDE.md` on all developer machines
2. Deploy `managed-settings.json` to `~/.claude/settings.json`

### Configuration Management (Ansible, Chef, Puppet)
1. Include files in your config management playbook
2. Target the `~/.claude/` directory on developer machines

### Git-Based Policy Repo
1. Create a shared repo with these policy files
2. Developers clone and symlink: `ln -s /path/to/policies/enterprise-CLAUDE.md ~/.claude/CLAUDE.md`

## Customization
- Edit `enterprise-CLAUDE.md` for your organization's specific rules
- Edit `managed-settings.json` for permission and hook policies
- Test changes in a non-production environment first
```

### Step 5: Report

Print summary:
- Files created in `.claude/policies/`
- Remind admin to customize templates for their organization
- Point to DEPLOYMENT.md for distribution instructions
- Note that `~/.claude/CLAUDE.md` is loaded for ALL projects on a machine
