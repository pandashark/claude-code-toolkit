---
allowed-tools: [Read, Write, Bash]
argument-hint: "[--monorepo]"
description: Scaffold .claude/rules/ directory with path-scoped rule files
---

# Rules Setup

Create a `.claude/rules/` directory with modular, path-scoped rule files that Claude Code automatically discovers based on the files being edited.

## What It Does

Instead of a monolithic `CLAUDE.md`, individual rule files in `.claude/rules/` are loaded by Claude Code based on glob patterns. Each file uses YAML frontmatter with `globs` (path-scoped) or `alwaysApply: true` (global).

## Installation Steps

### Step 1: Detect project structure

Determine if this is a monorepo or single-repo:

**Monorepo indicators** (any of these):
- `--monorepo` flag was passed
- Directories: `packages/`, `apps/`, `services/`
- Config files: `pnpm-workspace.yaml`, `lerna.json`, `turbo.json`, `nx.json`
- `"workspaces"` key in `package.json`

**Language detection** (check which apply):
- `package.json` or `tsconfig.json` → JavaScript/TypeScript
- `pyproject.toml` or `requirements.txt` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust

### Step 2: Create rules directory

```bash
mkdir -p .claude/rules
```

### Step 3: Create general rules file

Write `.claude/rules/general.md`:

```markdown
---
description: General project rules and conventions
alwaysApply: true
---

- Follow existing code style and patterns in this codebase
- Write tests for new functionality
- Use conventional commits format (feat:, fix:, refactor:, docs:, test:)
- Never commit secrets, API keys, or credentials
- Prefer editing existing files over creating new ones
```

### Step 4: Create language-specific rules

Based on detected languages, create the appropriate rule files.

**Python** — write `.claude/rules/python.md`:
```markdown
---
description: Python code conventions
globs: "**/*.py"
---

- Use type hints on all function signatures
- Prefer pathlib over os.path
- Use dataclasses or Pydantic models over raw dicts for structured data
- Format with ruff, lint with ruff check
```

**JavaScript/TypeScript** — write `.claude/rules/typescript.md`:
```markdown
---
description: TypeScript/JavaScript conventions
globs: "**/*.{ts,tsx,js,jsx}"
---

- Use TypeScript strict mode types — avoid `any`
- Prefer named exports over default exports
- Use async/await over raw promises
- Format with prettier, lint with eslint
```

**Go** — write `.claude/rules/go.md`:
```markdown
---
description: Go code conventions
globs: "**/*.go"
---

- Follow standard Go project layout
- Use table-driven tests
- Handle all errors explicitly — no blank `_` for error returns
- Format with gofmt
```

**Rust** — write `.claude/rules/rust.md`:
```markdown
---
description: Rust code conventions
globs: "**/*.rs"
---

- Use Result/Option types idiomatically — avoid unwrap in library code
- Derive common traits (Debug, Clone) where appropriate
- Write doc comments for public API items
- Format with rustfmt
```

### Step 5: Create monorepo-scoped rules (if applicable)

If monorepo detected, scan for top-level directories under `packages/`, `apps/`, or `services/` and create a scoped rule file for each. Example for a package named `api`:

```markdown
---
description: API package rules
globs: "packages/api/**"
---

- [Add package-specific rules here]
```

Create one rule file per discovered package/app/service with a placeholder body that the user can customize.

### Step 6: Report

Print a summary:
- Whether monorepo or single-repo was detected
- Which language rule files were created
- How many monorepo-scoped rules were generated (if any)
- Remind user that `.claude/rules/` files are automatically discovered by Claude Code — no `CLAUDE.md` changes needed
- Suggest the user customize the generated rules for their specific project conventions
