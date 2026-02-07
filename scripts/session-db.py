#!/usr/bin/env python3
"""
Session Database - SQLite index of all Claude Code sessions.

Indexes session data for fast queries across:
- 2000+ sessions
- 1.3GB+ of JSONL data
- Multiple projects and sub-projects

Use cases:
- "What did we do about X across all ml4t projects?"
- "When did we last touch this file?"
- "Didn't we implement this already?"

Usage:
    ./session-db.py index              # Build/update index
    ./session-db.py search "query"     # Search across all sessions
    ./session-db.py search "query" --project ml4t  # Filter by project
    ./session-db.py timeline --days 2  # Recent activity
    ./session-db.py files "pattern"    # Find file changes
"""

import json
import sqlite3
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import argparse

DB_PATH = Path.home() / ".claude/session-index.db"
PROJECTS_DIR = Path.home() / ".claude/projects"

def init_db(conn):
    """Initialize database schema."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            session_id TEXT UNIQUE,
            project TEXT,
            project_path TEXT,
            first_ts TEXT,
            last_ts TEXT,
            action_count INTEGER,
            indexed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            project TEXT,
            timestamp TEXT,
            date TEXT,
            tool TEXT,
            action_type TEXT,
            detail TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        );

        CREATE INDEX IF NOT EXISTS idx_actions_project ON actions(project);
        CREATE INDEX IF NOT EXISTS idx_actions_date ON actions(date);
        CREATE INDEX IF NOT EXISTS idx_actions_tool ON actions(tool);
        CREATE INDEX IF NOT EXISTS idx_actions_type ON actions(action_type);

        -- Full-text search on action details
        CREATE VIRTUAL TABLE IF NOT EXISTS actions_fts USING fts5(
            detail,
            content='actions',
            content_rowid='id'
        );

        -- Triggers to keep FTS in sync
        CREATE TRIGGER IF NOT EXISTS actions_ai AFTER INSERT ON actions BEGIN
            INSERT INTO actions_fts(rowid, detail) VALUES (new.id, new.detail);
        END;

        CREATE TRIGGER IF NOT EXISTS actions_ad AFTER DELETE ON actions BEGIN
            INSERT INTO actions_fts(actions_fts, rowid, detail)
            VALUES('delete', old.id, old.detail);
        END;
    """)

def extract_project_name(claude_dir_name: str) -> tuple:
    """Extract readable project name from Claude's directory format."""
    # -home-user-my-project-subdir -> my-project-subdir
    parts = claude_dir_name.lstrip("-").split("-")
    # Skip home and username
    if len(parts) > 2 and parts[0] == "home":
        parts = parts[2:]
    return "-".join(parts), "/" + claude_dir_name.lstrip("-").replace("-", "/")

def parse_session(session_file: Path) -> list:
    """Parse a session JSONL file into actions."""
    actions = []

    with open(session_file, errors='ignore') as f:
        for line in f:
            try:
                msg = json.loads(line)
                ts_str = msg.get("timestamp")
                if not ts_str:
                    continue

                content = msg.get("message", {}).get("content", [])
                if not isinstance(content, list):
                    continue

                for item in content:
                    if item.get("type") != "tool_use":
                        continue

                    tool_name = item.get("name", "")
                    tool_input = item.get("input", {})

                    action = {
                        "timestamp": ts_str,
                        "date": ts_str[:10],
                        "tool": tool_name,
                    }

                    if tool_name == "Bash":
                        action["detail"] = tool_input.get("command", "")[:500]
                        action["action_type"] = "command"
                    elif tool_name in ("Write", "Edit"):
                        action["detail"] = tool_input.get("file_path", "")
                        action["action_type"] = "file_change"
                    elif tool_name == "Read":
                        action["detail"] = tool_input.get("file_path", "")
                        action["action_type"] = "file_read"
                    elif tool_name == "Grep":
                        pattern = tool_input.get("pattern", "")
                        path = tool_input.get("path", "")
                        action["detail"] = f"{pattern} in {path}"
                        action["action_type"] = "search"
                    elif tool_name == "WebFetch":
                        action["detail"] = tool_input.get("url", "")
                        action["action_type"] = "web"
                    elif tool_name == "Task":
                        action["detail"] = tool_input.get("prompt", "")[:300]
                        action["action_type"] = "agent"
                    else:
                        action["detail"] = str(tool_input)[:200]
                        action["action_type"] = "other"

                    actions.append(action)
            except:
                continue

    return actions

def index_sessions(conn, force=False, project_filter=None):
    """Index all sessions into the database."""
    cursor = conn.cursor()

    # Get already indexed sessions
    cursor.execute("SELECT session_id, indexed_at FROM sessions")
    indexed = {row[0]: row[1] for row in cursor.fetchall()}

    stats = {"new": 0, "updated": 0, "skipped": 0, "actions": 0}

    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        project_name, project_path = extract_project_name(project_dir.name)

        # Filter by project if specified
        if project_filter and project_filter.lower() not in project_name.lower():
            continue

        for session_file in project_dir.glob("*.jsonl"):
            session_id = session_file.stem
            file_mtime = datetime.fromtimestamp(session_file.stat().st_mtime).isoformat()

            # Skip if already indexed and file hasn't changed
            if session_id in indexed and not force:
                if indexed[session_id] >= file_mtime:
                    stats["skipped"] += 1
                    continue

            # Parse session
            actions = parse_session(session_file)
            if not actions:
                continue

            # Delete old data if updating
            if session_id in indexed:
                cursor.execute("DELETE FROM actions WHERE session_id = ?", (session_id,))
                cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
                stats["updated"] += 1
            else:
                stats["new"] += 1

            # Insert session metadata
            cursor.execute("""
                INSERT INTO sessions (session_id, project, project_path,
                                     first_ts, last_ts, action_count, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                project_name,
                project_path,
                actions[0]["timestamp"],
                actions[-1]["timestamp"],
                len(actions),
                datetime.now().isoformat()
            ))

            # Insert actions
            for action in actions:
                cursor.execute("""
                    INSERT INTO actions (session_id, project, timestamp, date,
                                        tool, action_type, detail)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    project_name,
                    action["timestamp"],
                    action["date"],
                    action["tool"],
                    action["action_type"],
                    action["detail"]
                ))
                stats["actions"] += 1

    conn.commit()
    return stats

def search(conn, query: str, project: str = None, days: int = None, limit: int = 50):
    """Search actions using full-text search."""
    cursor = conn.cursor()

    # Escape special FTS5 characters and wrap in quotes for literal search
    safe_query = '"' + query.replace('"', '""') + '"'

    sql = """
        SELECT a.date, a.timestamp, a.project, a.tool, a.action_type, a.detail
        FROM actions a
        JOIN actions_fts fts ON a.id = fts.rowid
        WHERE actions_fts MATCH ?
    """
    params = [safe_query]

    if project:
        sql += " AND a.project LIKE ?"
        params.append(f"%{project}%")

    if days:
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        sql += " AND a.date >= ?"
        params.append(since)

    sql += " ORDER BY a.timestamp DESC LIMIT ?"
    params.append(limit)

    cursor.execute(sql, params)
    return cursor.fetchall()

def timeline(conn, days: int = 2, project: str = None):
    """Show timeline of recent activity."""
    cursor = conn.cursor()
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    sql = """
        SELECT date, project, tool, COUNT(*) as count
        FROM actions
        WHERE date >= ?
    """
    params = [since]

    if project:
        sql += " AND project LIKE ?"
        params.append(f"%{project}%")

    sql += " GROUP BY date, project, tool ORDER BY date DESC, count DESC"

    cursor.execute(sql, params)
    return cursor.fetchall()

def file_changes(conn, pattern: str = None, days: int = 7, limit: int = 50):
    """Find file changes matching pattern."""
    cursor = conn.cursor()
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    sql = """
        SELECT date, project, tool, detail
        FROM actions
        WHERE action_type = 'file_change' AND date >= ?
    """
    params = [since]

    if pattern:
        sql += " AND detail LIKE ?"
        params.append(f"%{pattern}%")

    sql += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    cursor.execute(sql, params)
    return cursor.fetchall()

def stats(conn):
    """Show database statistics."""
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sessions")
    sessions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM actions")
    actions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT project, COUNT(*) as count
        FROM sessions
        GROUP BY project
        ORDER BY count DESC
        LIMIT 15
    """)
    by_project = cursor.fetchall()

    cursor.execute("""
        SELECT tool, COUNT(*) as count
        FROM actions
        GROUP BY tool
        ORDER BY count DESC
        LIMIT 10
    """)
    by_tool = cursor.fetchall()

    cursor.execute("SELECT MIN(date), MAX(date) FROM actions")
    date_range = cursor.fetchone()

    return {
        "sessions": sessions,
        "actions": actions,
        "by_project": by_project,
        "by_tool": by_tool,
        "date_range": date_range,
    }

def main():
    parser = argparse.ArgumentParser(description="Session history database")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Index command
    index_parser = subparsers.add_parser("index", help="Build/update index")
    index_parser.add_argument("--force", action="store_true", help="Force full reindex")
    index_parser.add_argument("--project", help="Filter by project name")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search sessions")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--project", help="Filter by project")
    search_parser.add_argument("--days", type=int, help="Limit to last N days")
    search_parser.add_argument("--limit", type=int, default=30, help="Max results")

    # Timeline command
    timeline_parser = subparsers.add_parser("timeline", help="Show recent activity")
    timeline_parser.add_argument("--days", type=int, default=2, help="Days to show")
    timeline_parser.add_argument("--project", help="Filter by project")

    # Files command
    files_parser = subparsers.add_parser("files", help="Find file changes")
    files_parser.add_argument("pattern", nargs="?", help="File path pattern")
    files_parser.add_argument("--days", type=int, default=7, help="Days to search")

    # Stats command
    subparsers.add_parser("stats", help="Show database statistics")

    args = parser.parse_args()

    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    if args.command == "index":
        print(f"Indexing sessions from {PROJECTS_DIR}...")
        result = index_sessions(conn, args.force, args.project)
        print(f"Done: {result['new']} new, {result['updated']} updated, "
              f"{result['skipped']} skipped, {result['actions']} actions indexed")

    elif args.command == "search":
        results = search(conn, args.query, args.project, args.days, args.limit)
        print(f"=== Search: '{args.query}' ({len(results)} results) ===\n")
        for row in results:
            date, ts, project, tool, atype, detail = row
            proj_short = project[:20] if len(project) > 20 else project
            print(f"{date} | {proj_short:20} | {tool:8} | {detail[:60]}")

    elif args.command == "timeline":
        results = timeline(conn, args.days, args.project)
        print(f"=== Timeline (last {args.days} days) ===\n")
        current_date = None
        for row in results:
            date, project, tool, count = row
            if date != current_date:
                print(f"\n--- {date} ---")
                current_date = date
            proj_short = project[:25] if len(project) > 25 else project
            print(f"  {proj_short:25} | {tool:8} | {count:4} actions")

    elif args.command == "files":
        results = file_changes(conn, args.pattern, args.days)
        print(f"=== File Changes ({len(results)} results) ===\n")
        for row in results:
            date, project, tool, detail = row
            proj_short = project[:15] if len(project) > 15 else project
            print(f"{date} | {proj_short:15} | {tool:5} | {detail}")

    elif args.command == "stats":
        s = stats(conn)
        print(f"=== Session Database Stats ===")
        print(f"Sessions: {s['sessions']}")
        print(f"Actions: {s['actions']}")
        print(f"Date range: {s['date_range'][0]} to {s['date_range'][1]}")
        print(f"\n--- Sessions by Project ---")
        for proj, count in s['by_project']:
            print(f"  {count:4} | {proj}")
        print(f"\n--- Actions by Tool ---")
        for tool, count in s['by_tool']:
            print(f"  {count:6} | {tool}")

    else:
        parser.print_help()

    conn.close()

if __name__ == "__main__":
    main()
