# Scripts

Utility scripts for Claude Code Toolkit.

## Session History Search

Claude Code captures complete session history in `~/.claude/projects/[project-path]/*.jsonl`. These tools make that data searchable.

### session-db.py (Recommended)

SQLite-indexed search across all sessions. Fast queries over thousands of sessions.

**First time setup**:
```bash
python3 scripts/session-db.py index
# Indexes all sessions (~3 seconds for 2000+ sessions)
```

**Commands**:

```bash
# Search across all projects
session-db.py search "query"

# Filter by project name (partial match)
session-db.py search "backtest" --project ml4t

# Limit to recent days
session-db.py search "authentication" --days 7

# Timeline view - what happened recently
session-db.py timeline --days 2

# File changes
session-db.py files "pattern" --days 7

# Database statistics
session-db.py stats

# Rebuild index (incremental by default)
session-db.py index
session-db.py index --force  # Full rebuild
```

**What gets indexed**:
- Tool calls: Bash commands, file reads/writes/edits, grep searches
- Timestamps for temporal queries
- Project association for cross-project search

**Performance**:
- Index: ~3 seconds for 2000+ sessions (incremental updates <1 second)
- Queries: <30ms
- Database size: ~38MB for 90K+ actions (vs 1.3GB raw JSONL)

### session-index.py

Simpler per-project search without database. Parses JSONL directly.

```bash
# Summary of recent activity
session-index.py /path/to/project

# Search
session-index.py /path/to/project --search "query"

# Timeline view
session-index.py /path/to/project --timeline

# File changes only
session-index.py /path/to/project --files
```

Use this when you only need single-project queries or don't want SQLite.

### session-search.sh

Minimal bash script for quick grep-based search.

```bash
./session-search.sh "query" /path/to/project
./session-search.sh "query" /path/to/project --summaries-only
```

## Other Scripts

### install-git-safe-commit.sh

Installs the `git-safe-commit` wrapper to `~/.local/bin/`.

```bash
./scripts/install-git-safe-commit.sh
```

This wrapper:
- Blocks `--no-verify` flag (no bypassing quality checks)
- Runs pre-commit hooks automatically
- Ensures commits pass linting/formatting/tests

## Use Cases

**"How did we implement X last time?"**
```bash
session-db.py search "JWT authentication" --days 30
```

**"What happened about Y in the last 2 days?"**
```bash
session-db.py search "Y" --days 2
# or
session-db.py timeline --days 2
```

**"Didn't we already do this?"**
```bash
session-db.py search "feature name"
```

**"What files did we change for project Z?"**
```bash
session-db.py files "" --project Z --days 7
```

**"What's the activity across all ml4t sub-projects?"**
```bash
session-db.py search "" --project ml4t --days 7
session-db.py timeline --days 7 --project ml4t
```
