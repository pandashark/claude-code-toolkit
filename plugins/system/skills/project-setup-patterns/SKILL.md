# Project Setup Patterns

**Purpose**: Comprehensive templates, configurations, and detection patterns for setting up new projects across multiple languages and frameworks.

**Used by**: `system/commands/setup.md`

**Token Impact**: Extracted ~7,300 tokens from setup command, enabling progressive loading of templates only when needed.

---

## Contents

### Templates

#### Python Templates (`templates/python/`)

**minimal.md** - Basic Python project setup
- Simple pyproject.toml with hatchling
- Minimal gitignore
- Best for: Quick experiments, learning projects

**standard.md** - Production-ready Python setup
- pyproject.toml with dev dependencies (pytest, ruff, mypy)
- Pre-commit configuration
- Makefile with dev commands
- Comprehensive gitignore
- Best for: Real projects, open source packages

**full.md** - Enterprise-grade Python setup
- Everything from standard, plus:
- Documentation setup (mkdocs)
- Security scanning (bandit)
- CI/CD workflows
- Best for: Commercial products, large teams

#### JavaScript Templates (`templates/javascript/`)

**standard.md** - Modern Node.js setup
- package.json with npm scripts
- Jest for testing
- ESLint and Prettier
- TypeScript type definitions
- Best for: Node.js applications, libraries

#### Configuration Patterns (`templates/patterns/`)

**security_hooks.json** - Claude Code security hooks
- PreToolUse: Blocks dangerous commands (rm -rf, sudo, chmod 777)
- PostToolUse: Auto-formats code (ruff, prettier, eslint)
- JSON validation and markdown linting

### Detection Patterns

#### Framework Detection (`detection/`)

**framework_detection.md** - Language and framework detection patterns
- Python: pyproject.toml, setup.py, requirements.txt
- JavaScript: package.json, NPM packages
- Go: go.mod
- Rust: Cargo.toml
- Framework detection (FastAPI, Django, Flask, Next.js, React, Express)
- Test tool detection (pytest, Jest, Mocha)
- Build system detection (Make, etc.)

---

## Usage Patterns

### Loading Templates

Commands should reference templates from this skill:

```bash
# Python minimal setup
# Load: templates/python/minimal.md
# Apply: pyproject.toml and .gitignore

# Python standard setup
# Load: templates/python/standard.md
# Apply: pyproject.toml, .pre-commit-config.yaml, Makefile, .gitignore

# JavaScript setup
# Load: templates/javascript/standard.md
# Apply: package.json, src/index.js, tests/index.test.js
```

### Variable Substitution

All templates use `$PROJECT_NAME` as placeholder. Commands must perform substitution:

```bash
sed -i "s/\$PROJECT_NAME/$PROJECT_NAME/g" pyproject.toml
```

### Security Hooks

Load security hooks configuration:

```bash
# Copy security_hooks.json to .claude/settings.json
cp templates/patterns/security_hooks.json .claude/settings.json
```

### Detection Patterns

Use detection algorithms to auto-identify project type:

```bash
# Detect language
if [ -f "package.json" ]; then
    DETECTED_LANG="JavaScript/TypeScript"
elif [ -f "pyproject.toml" ]; then
    DETECTED_LANG="Python"
fi

# Detect framework
grep -q 'fastapi' pyproject.toml && DETECTED_FRAMEWORK="FastAPI"
```

---

## Directory Structure

```
project-setup-patterns/
├── SKILL.md                              # This file
├── templates/
│   ├── python/
│   │   ├── minimal.md                    # Basic Python setup
│   │   ├── standard.md                   # Production Python setup
│   │   └── full.md                       # Enterprise Python setup
│   ├── javascript/
│   │   └── standard.md                   # Node.js setup
│   └── patterns/
│       └── security_hooks.json           # Security hooks config
└── detection/
    └── framework_detection.md            # Detection patterns
```

---

## Extension Points

### Adding New Language Templates

1. Create `templates/{language}/` directory
2. Add `standard.md` with language-specific configuration
3. Update detection patterns in `detection/framework_detection.md`
4. Update this SKILL.md with new language usage

### Adding New Python Setups

- Add new markdown file to `templates/python/`
- Follow existing pattern with sections for each config file
- Document use case and target audience

### Updating Tool Versions

When tool versions update (pytest, ruff, etc.):
1. Update relevant template files
2. Test with new versions
3. Document breaking changes if any

---

## Design Principles

### Separation of Concerns

- **Commands**: Orchestrate workflow (parse args, create dirs, write files)
- **Skills**: Provide templates and patterns (reference data)
- Commands load templates on-demand, not all upfront

### Progressive Disclosure

- Only load templates actually needed for current setup
- Minimal setup doesn't load standard/full templates
- JavaScript setup doesn't load Python templates

### Declarative Templates

- Templates are data, not executable code
- Commands apply templates to create files
- Variable substitution happens in commands, not templates

### Maintenance Benefits

- Update templates without touching command logic
- Add new languages by adding templates
- Version control templates independently

---

## Token Economics

### Before Extraction (inline)
- All templates embedded in setup.md: ~10,416 tokens
- Loaded on every `/setup` invocation
- Hard to maintain (mixed workflow + data)

### After Extraction (skill-based)
- Command (workflow only): ~2,500 tokens
- Skill (templates): ~7,300 tokens (loaded on-demand)
- Total savings: ~8,000 tokens per invocation
- Easier maintenance: Update templates without touching command

### Loading Strategy
- Command always loads: ~2,500 tokens
- Skill loads progressively: Only needed templates
- Example: `/setup python --minimal` loads ~500 token template, not all 7,300

---

## Testing Checklist

When modifying templates or patterns:

- [ ] Test Python minimal: `/setup python --minimal`
- [ ] Test Python standard: `/setup python --standard`
- [ ] Test Python full: `/setup python --full`
- [ ] Test JavaScript: `/setup javascript`
- [ ] Test existing project: `/setup existing`
- [ ] Test exploration: `/setup explore`
- [ ] Verify token counts with estimate_tokens.py
- [ ] Check variable substitution works ($PROJECT_NAME)
- [ ] Validate security hooks load correctly

---

## Version History

- **v1.0.0** (2025-11-02) - Initial extraction from setup.md
  - Extracted 7,300 tokens of templates and patterns
  - Reduced setup.md from 10,416 to ~2,500 tokens
  - Created skill structure with progressive loading
