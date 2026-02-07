---
name: sandboxing
description: Claude Code sandboxing configuration for macOS (Seatbelt) and Linux (bubblewrap). Covers platform detection, enablement, sandbox profiles, and troubleshooting. Reduces permission prompts by ~84%.
---

# Sandboxing Configuration

**Purpose**: Guide Claude Code sandbox setup for native OS-level sandboxing.

**Used by**: `/setup:existing`, project initialization workflows

**Token Impact**: ~800 tokens of sandboxing guidance, loaded on demand when sandboxing setup is needed.

---

## Quick Reference

**When to use**: Setting up a new project, reducing permission prompts, hardening CI environments.

**Common triggers**: "too many permission prompts", "sandbox setup", "restrict file access", "secure Claude Code".

**Benefits**: ~84% reduction in permission prompts. Claude can pre-approve operations within sandbox boundaries.

---

## 1. Platform Detection

Detect which sandboxing backend is available:

```bash
SANDBOX_PLATFORM=""
SANDBOX_AVAILABLE=false

case "$(uname)" in
  Darwin)
    SANDBOX_PLATFORM="macos-seatbelt"
    command -v sandbox-exec >/dev/null 2>&1 && SANDBOX_AVAILABLE=true
    ;;
  Linux)
    SANDBOX_PLATFORM="linux-bubblewrap"
    command -v bwrap >/dev/null 2>&1 && SANDBOX_AVAILABLE=true
    ;;
esac
```

- **macOS**: Seatbelt (`sandbox-exec`) is built-in since macOS Leopard. Always available.
- **Linux**: bubblewrap (`bwrap`) must be installed. Install with `apt install bubblewrap` (Debian/Ubuntu), `dnf install bubblewrap` (Fedora), or `pacman -S bubblewrap` (Arch).

---

## 2. Enabling Sandboxing

Claude Code sandboxing is configured in `.claude/settings.json`. Add at the project level:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npx *)",
      "Read",
      "Write(.claude/**)",
      "Write(src/**)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(sudo *)"
    ]
  }
}
```

Key configuration options:
- **`allow`**: Pre-approve specific tool patterns. Reduces prompts for known-safe operations.
- **`deny`**: Block dangerous patterns. Overrides allow rules.
- Tool patterns use glob syntax: `Bash(npm run *)` matches any npm run command.
- `Read` without a pattern allows reading any file in the project.
- `Write(src/**)` restricts writes to the `src/` directory tree.

---

## 3. Sandbox Profiles

### Development Profile (Permissive)

For day-to-day development. Allows most operations within the project:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(npm *)",
      "Bash(npx *)",
      "Bash(git *)",
      "Bash(python *)",
      "Bash(pip *)",
      "Write(src/**)",
      "Write(tests/**)",
      "Write(.claude/**)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(sudo *)",
      "Bash(chmod 777 *)"
    ]
  }
}
```

### CI/CD Profile (Restricted)

For automated environments. Tighter restrictions:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(npm run test)",
      "Bash(npm run lint)",
      "Bash(npm run build)"
    ],
    "deny": [
      "Bash(rm *)",
      "Bash(sudo *)",
      "Bash(git push *)",
      "Bash(npm publish *)",
      "Write"
    ]
  }
}
```

### Audit Profile (Read-Only)

For code review and analysis. No writes allowed:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(wc *)"
    ],
    "deny": [
      "Write",
      "Bash"
    ]
  }
}
```

---

## 4. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "permission denied" on file write | File outside allowed write paths | Add path to `allow` list or widen glob |
| "operation not permitted" on bash | Command not in allow patterns | Add specific command pattern to `allow` |
| Too many prompts despite config | Settings not loaded | Restart Claude Code after editing settings.json |
| bwrap not found (Linux) | bubblewrap not installed | `apt install bubblewrap` or equivalent |
| Sandbox has no effect (macOS) | sandbox-exec issue | Check `sandbox-exec -n no-network true` works |

---

## 5. Best Practices

- Start with the **development profile** and tighten as needed
- Use **specific glob patterns** rather than blanket allows (`Write(src/**)` not `Write`)
- Always **deny dangerous operations** explicitly, even with narrow allows
- Keep **CI profiles strict** -- only allow the exact commands your pipeline needs
- Test sandbox config changes by running Claude Code and verifying prompt behavior
- If sandboxing is unavailable, hooks provide an alternative safety layer (see `/setup:hooks`)
