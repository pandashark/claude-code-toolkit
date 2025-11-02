# Python Full Template

## Overview

The full setup provides comprehensive enterprise-grade configuration including everything from standard, plus:
- Documentation setup (mkdocs with material theme)
- Security scanning (bandit)
- CI/CD workflows (GitHub Actions)
- Extended testing setup (fixtures, coverage reports)
- Additional development tools
- Release automation setup
- Dependency management configuration

**Best for**: Commercial products, large teams, projects requiring compliance

## Requirements

The full setup requires creating these files based on current best practices:

### 1. pyproject.toml

Include latest versions of:
- ruff, mypy, pytest, pytest-cov, bandit
- mkdocs, mkdocs-material for documentation
- pre-commit for git hooks

### 2. .pre-commit-config.yaml

Configure hooks for:
- ruff (format and lint)
- mypy (type checking)
- bandit (security)
- conventional commits

### 3. Makefile

Extend with targets for:
- install, dev, test, lint, format, type-check
- security, docs, build, clean

### 4. .github/workflows/ci.yml

Create GitHub Actions workflow with:
- Test execution across multiple Python versions
- Linting and type checking
- Security scanning
- Coverage reporting
- Release automation

### 5. mkdocs.yml

Documentation configuration with:
- Material theme
- API documentation
- Tutorials and guides
- Search functionality

### 6. Comprehensive .gitignore

Extended to include:
- All Python artifacts
- IDE configurations
- Documentation build outputs
- CI/CD artifacts

## Declarative Generation Note

In the future, Claude Code will generate these files declaratively based on current best practices. For now, this skill provides the requirements and guidance for manual creation.
