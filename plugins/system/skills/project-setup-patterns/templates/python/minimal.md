# Python Minimal Template

## pyproject.toml

```toml
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Python package"
requires-python = ">=3.9"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## .gitignore

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
venv/
.venv/
*.log
.DS_Store
```

## Usage

This minimal setup provides:
- Basic `pyproject.toml` with project metadata
- Minimal `.gitignore` for Python projects
- Simple project structure (`src/`, `tests/`, `docs/`)
- Build system configuration (hatchling)

**Best for**: Quick experiments, learning projects, temporary code
