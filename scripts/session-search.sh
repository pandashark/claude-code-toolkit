#!/bin/bash
# Session Search - Query Claude Code session history
# Usage: session-search.sh <query> [project-path] [--summaries-only]

set -euo pipefail

QUERY="${1:-}"
PROJECT_PATH="${2:-$PWD}"
SUMMARIES_ONLY="${3:-}"

if [ -z "$QUERY" ]; then
    echo "Usage: session-search.sh <query> [project-path] [--summaries-only]"
    echo ""
    echo "Search Claude Code session history for keywords, decisions, and context."
    echo ""
    echo "Options:"
    echo "  --summaries-only  Only show auto-compact summaries (fast overview)"
    echo ""
    echo "Examples:"
    echo "  session-search.sh 'JWT authentication'"
    echo "  session-search.sh 'bug fix' ~/projects/myapp"
    echo "  session-search.sh 'database' . --summaries-only"
    exit 1
fi

# Convert project path to Claude's directory format
PROJECT_PATH=$(cd "$PROJECT_PATH" 2>/dev/null && pwd || echo "$PROJECT_PATH")
CLAUDE_PROJECT_DIR="-$(echo "$PROJECT_PATH" | sed 's|^/||; s|/|-|g')"
SESSION_DIR="$HOME/.claude/projects/$CLAUDE_PROJECT_DIR"

if [ ! -d "$SESSION_DIR" ]; then
    echo "No session data found for: $PROJECT_PATH"
    exit 1
fi

SESSION_COUNT=$(ls -1 "$SESSION_DIR"/*.jsonl 2>/dev/null | wc -l)

echo "=== Session Search: '$QUERY' ==="
echo "Project: $PROJECT_PATH"
echo "Sessions: $SESSION_COUNT"
echo ""

if [ "$SUMMARIES_ONLY" = "--summaries-only" ]; then
    # Fast path: just search summaries
    echo "--- Matching Summaries ---"
    for f in "$SESSION_DIR"/*.jsonl; do
        grep -i "$QUERY" "$f" 2>/dev/null | \
            jq -r 'select(.type=="summary") | .summary' 2>/dev/null
    done | sort -u | head -30
    exit 0
fi

# Full search
for SESSION_FILE in $(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -20); do
    [ -f "$SESSION_FILE" ] || continue

    SESSION_DATE=$(stat -c %y "$SESSION_FILE" 2>/dev/null | cut -d' ' -f1)

    # Check if file contains query
    if grep -qi "$QUERY" "$SESSION_FILE" 2>/dev/null; then
        echo "--- $SESSION_DATE ---"

        # Extract summaries
        grep -i "$QUERY" "$SESSION_FILE" 2>/dev/null | \
            jq -r 'select(.type=="summary") | "📋 " + .summary' 2>/dev/null | head -5

        # Extract user questions containing query
        grep -i "$QUERY" "$SESSION_FILE" 2>/dev/null | \
            jq -r 'select(.type=="user") | .message.content |
                   if type=="string" then .
                   elif type=="array" then (.[0].text // .[0].content // "")
                   else "" end' 2>/dev/null | \
            grep -i "$QUERY" | \
            sed 's/^/❓ /' | \
            cut -c1-120 | head -3

        # Extract decisions/conclusions from assistant
        grep -i "$QUERY" "$SESSION_FILE" 2>/dev/null | \
            jq -r 'select(.type=="assistant") | .message.content[]? |
                   select(.type=="text") | .text' 2>/dev/null | \
            grep -i "$QUERY" | \
            grep -iE "(decided|chose|will|should|recommend|conclusion|verdict|result)" | \
            sed 's/^/💡 /' | \
            cut -c1-150 | head -3

        echo ""
    fi
done

echo "=== Search complete ==="
