#!/usr/bin/env python3
"""
Session Indexer - Create searchable action log from Claude Code sessions.

Creates a compact, searchable index of all actions:
- What was done (tool calls, file changes)
- When it was done (timestamps)
- Why it was done (surrounding context)

Usage:
    ./session-index.py [project-path] [--days N] [--rebuild]
    ./session-index.py --search "query" [--since 2d]
"""

import json
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import argparse

def get_session_dir(project_path: str) -> Path:
    """Convert project path to Claude's session directory."""
    project_path = Path(project_path).resolve()
    claude_name = "-" + str(project_path).lstrip("/").replace("/", "-")
    return Path.home() / ".claude/projects" / claude_name

def extract_actions(session_file: Path, since: datetime = None) -> list:
    """Extract actions from a session file."""
    actions = []

    with open(session_file) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        try:
            msg = json.loads(line)
            ts_str = msg.get("timestamp")
            if not ts_str:
                continue

            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            if since and ts < since:
                continue

            msg_type = msg.get("type")
            content = msg.get("message", {}).get("content", [])

            # Extract tool uses
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "tool_use":
                        tool_name = item.get("name")
                        tool_input = item.get("input", {})

                        action = {
                            "timestamp": ts_str,
                            "date": ts.strftime("%Y-%m-%d"),
                            "time": ts.strftime("%H:%M"),
                            "tool": tool_name,
                        }

                        if tool_name == "Bash":
                            cmd = tool_input.get("command", "")
                            action["detail"] = cmd[:200]
                            action["type"] = "command"
                        elif tool_name in ("Write", "Edit"):
                            action["detail"] = tool_input.get("file_path", "")
                            action["type"] = "file_change"
                        elif tool_name == "Read":
                            action["detail"] = tool_input.get("file_path", "")
                            action["type"] = "file_read"
                        elif tool_name == "WebFetch":
                            action["detail"] = tool_input.get("url", "")
                            action["type"] = "web"
                        elif tool_name == "Grep":
                            action["detail"] = f"pattern: {tool_input.get('pattern', '')}"
                            action["type"] = "search"
                        else:
                            action["detail"] = str(tool_input)[:100]
                            action["type"] = "other"

                        actions.append(action)

            # Extract summaries
            if msg_type == "summary":
                actions.append({
                    "timestamp": ts_str if ts_str else "",
                    "date": ts.strftime("%Y-%m-%d") if ts_str else "unknown",
                    "time": ts.strftime("%H:%M") if ts_str else "",
                    "tool": "summary",
                    "type": "summary",
                    "detail": msg.get("summary", ""),
                })

        except Exception as e:
            continue

    return actions

def build_index(project_path: str, days: int = 7) -> dict:
    """Build action index for project."""
    session_dir = get_session_dir(project_path)

    if not session_dir.exists():
        print(f"No sessions found: {session_dir}")
        return {}

    since = datetime.now().astimezone() - timedelta(days=days)

    all_actions = []
    files_touched = defaultdict(list)
    commands_run = []
    summaries = []

    for session_file in sorted(session_dir.glob("*.jsonl"),
                                key=lambda f: f.stat().st_mtime,
                                reverse=True):
        actions = extract_actions(session_file, since)
        all_actions.extend(actions)

        for action in actions:
            if action["type"] == "file_change":
                files_touched[action["detail"]].append(action)
            elif action["type"] == "command":
                commands_run.append(action)
            elif action["type"] == "summary":
                summaries.append(action)

    return {
        "project": project_path,
        "indexed_at": datetime.now().isoformat(),
        "since": since.isoformat(),
        "total_actions": len(all_actions),
        "files_touched": dict(files_touched),
        "commands_run": commands_run,
        "summaries": summaries,
        "all_actions": all_actions,
    }

def search_index(index: dict, query: str, since_days: int = None) -> list:
    """Search the index for matching actions."""
    results = []
    query_lower = query.lower()

    since = None
    if since_days:
        since = datetime.now().astimezone() - timedelta(days=since_days)

    for action in index.get("all_actions", []):
        # Filter by time if specified
        if since and action.get("timestamp"):
            try:
                action_time = datetime.fromisoformat(
                    action["timestamp"].replace("Z", "+00:00"))
                if action_time < since:
                    continue
            except:
                pass

        # Search in detail and type
        detail = action.get("detail", "").lower()
        if query_lower in detail:
            results.append(action)

    return results

def group_by_day(actions: list) -> dict:
    """Group actions by day."""
    by_day = defaultdict(list)
    for a in actions:
        day = a.get("date", "unknown")
        by_day[day].append(a)
    return dict(by_day)

def print_summary(index: dict):
    """Print a summary of the index."""
    print(f"=== Session Index ===")
    print(f"Project: {index['project']}")
    print(f"Since: {index['since'][:10]}")
    print(f"Total actions: {index['total_actions']}")
    print(f"Files touched: {len(index['files_touched'])}")
    print(f"Commands run: {len(index['commands_run'])}")
    print()

    # Group by day
    by_day = group_by_day(index["all_actions"])
    print("--- Activity by Day ---")
    for day in sorted(by_day.keys(), reverse=True)[:5]:
        actions = by_day[day]
        files = len([a for a in actions if a["type"] == "file_change"])
        cmds = len([a for a in actions if a["type"] == "command"])
        print(f"  {day}: {len(actions)} actions ({files} file changes, {cmds} commands)")
    print()

    # Recently changed files
    print("--- Recently Changed Files ---")
    recent_files = sorted(
        index["files_touched"].items(),
        key=lambda x: max(a["timestamp"] for a in x[1]) if x[1] else "",
        reverse=True
    )[:10]
    for filepath, actions in recent_files:
        print(f"  {len(actions)}x | {filepath}")
    print()

    # Recent commands (deduplicated)
    print("--- Recent Commands ---")
    seen = set()
    for cmd in reversed(index["commands_run"][-30:]):
        detail = cmd["detail"][:60]
        if detail not in seen:
            print(f"  {cmd['date']} {cmd['time']} | {detail}")
            seen.add(detail)
            if len(seen) >= 10:
                break

def print_timeline(index: dict, since_days: int = 2):
    """Print timeline of actions for last N days."""
    since = datetime.now().astimezone() - timedelta(days=since_days)

    print(f"=== Timeline (last {since_days} days) ===")

    by_day = group_by_day(index["all_actions"])
    for day in sorted(by_day.keys(), reverse=True):
        try:
            day_date = datetime.strptime(day, "%Y-%m-%d")
            if day_date.date() < since.date():
                continue
        except:
            continue

        print(f"\n--- {day} ---")
        actions = by_day[day]

        # Group by hour
        by_hour = defaultdict(list)
        for a in actions:
            hour = a.get("time", "??:??")[:2] + ":00"
            by_hour[hour].append(a)

        for hour in sorted(by_hour.keys()):
            hour_actions = by_hour[hour]
            print(f"\n  [{hour}]")
            for a in hour_actions[:10]:  # Limit per hour
                if a["type"] == "file_change":
                    fname = Path(a["detail"]).name if a["detail"] else "?"
                    print(f"    {a['tool']:6} | {fname}")
                elif a["type"] == "command":
                    cmd = a["detail"][:50]
                    print(f"    Bash   | {cmd}")
                elif a["type"] == "search":
                    print(f"    Grep   | {a['detail'][:50]}")

def main():
    parser = argparse.ArgumentParser(description="Session history indexer")
    parser.add_argument("project", nargs="?", default=".", help="Project path")
    parser.add_argument("--days", type=int, default=7, help="Days to index")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--since", type=str, help="Time filter (e.g., 2d, 1w)")
    parser.add_argument("--timeline", action="store_true", help="Show timeline view")
    parser.add_argument("--files", action="store_true", help="Show only file changes")
    parser.add_argument("--commands", action="store_true", help="Show only commands")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    project_path = str(Path(args.project).resolve())

    # Parse since argument
    since_days = None
    if args.since:
        match = re.match(r"(\d+)([dwh])", args.since)
        if match:
            num, unit = match.groups()
            if unit == "d":
                since_days = int(num)
            elif unit == "w":
                since_days = int(num) * 7
            elif unit == "h":
                since_days = int(num) / 24

    # Build index
    index = build_index(project_path, args.days)

    if args.search:
        # Search mode
        results = search_index(index, args.search, since_days)
        print(f"=== Search: '{args.search}' ===")
        print(f"Found {len(results)} matches")
        print()
        for r in results[-20:]:
            print(f"{r['date']} {r['time']} | {r['tool']:8} | {r['detail'][:70]}")
    elif args.timeline:
        # Timeline mode
        days = since_days if since_days else 2
        print_timeline(index, int(days))
    elif args.files:
        # File changes only
        print("=== File Changes ===")
        for filepath, actions in sorted(index["files_touched"].items(),
                                         key=lambda x: max(a["timestamp"] for a in x[1]),
                                         reverse=True)[:30]:
            for a in actions:
                print(f"{a['date']} {a['time']} | {a['tool']:6} | {filepath}")
    elif args.commands:
        # Commands only
        print("=== Commands Run ===")
        for cmd in index["commands_run"][-30:]:
            print(f"{cmd['date']} {cmd['time']} | {cmd['detail'][:80]}")
    elif args.json:
        # JSON output
        print(json.dumps(index, indent=2, default=str))
    else:
        # Summary mode
        print_summary(index)

if __name__ == "__main__":
    main()
