---
description: Search session history for past decisions, discussions, and context
---

# /memory:search [query]

Search Claude Code's session history to find past decisions, discussions, and context.

## How It Works

Claude Code automatically stores complete session history in `~/.claude/projects/`. This command searches that history to recover:
- Past decisions and their rationale
- Discussions about specific topics
- Auto-compact summaries
- Tool calls and their results

## Usage

```
/memory:search "authentication approach"
/memory:search "database schema" --summaries-only
/memory:search "bug fix" --recent 5
```

## Arguments

- `query` - Keywords to search for (required)
- `--summaries-only` - Only search auto-compact summaries (faster, less detail)
- `--recent N` - Only search N most recent sessions (default: 20)

## Implementation

When invoked, execute:

```bash
#!/bin/bash
QUERY="$1"
PROJECT_DIR=$(pwd)
CLAUDE_PROJECT="-$(echo "$PROJECT_DIR" | sed 's|^/||; s|/|-|g')"
SESSION_DIR="$HOME/.claude/projects/$CLAUDE_PROJECT"

if [ ! -d "$SESSION_DIR" ]; then
    echo "No session history found for this project."
    exit 1
fi

echo "Searching session history for: $QUERY"
echo ""

# Search summaries first (fast overview)
echo "## Relevant Summaries"
for f in $(ls -t "$SESSION_DIR"/*.jsonl | head -20); do
    grep -i "$QUERY" "$f" 2>/dev/null | \
        jq -r 'select(.type=="summary") | .summary' 2>/dev/null
done | sort -u | head -15

echo ""
echo "## Key Discussions"

# Search user messages and assistant responses
for f in $(ls -t "$SESSION_DIR"/*.jsonl | head -10); do
    DATE=$(stat -c %y "$f" | cut -d' ' -f1)

    # Check if file matches
    if grep -qi "$QUERY" "$f"; then
        echo ""
        echo "### Session: $DATE"

        # Extract relevant assistant text (decisions, recommendations)
        grep -i "$QUERY" "$f" | \
            jq -r 'select(.type=="assistant") | .message.content[]? |
                   select(.type=="text") | .text' 2>/dev/null | \
            grep -i "$QUERY" | \
            grep -iE "(decided|chose|recommend|should|will use|verdict|conclusion|the answer|solution)" | \
            head -5
    fi
done
```

## When to Use

- **Recovering lost context**: "What did we decide about X?"
- **Before starting new work**: "Have we discussed Y before?"
- **Debugging**: "When did we change Z?"
- **Continuity**: "What was the rationale for W?"

## Output Format

Returns:
1. **Relevant Summaries** - Auto-compact headlines mentioning the query
2. **Key Discussions** - Extracted decisions and recommendations from past sessions

## Token Efficiency

This searches raw session data (~4.5MB for 97 sessions in this project) but only returns:
- Summary headlines (1 line each)
- Key decision sentences (truncated to 150 chars)

Typical output: 500-2000 tokens regardless of total session history size.

## Limitations

- Only searches current project's sessions
- Requires `jq` for JSON parsing
- Best for keyword-based searches (not semantic)
- Recent sessions searched first (older may be missed)

## Examples

### Find authentication decisions
```
/memory:search "JWT authentication"

## Relevant Summaries
- API authentication patterns implementation
- Auth flow refactoring complete

## Key Discussions
### Session: 2025-12-10
- Decided to use RS256 for JWT signing due to key rotation needs
- Should implement refresh token rotation for security
```

### Find bug fixes
```
/memory:search "bug fix" --summaries-only

## Relevant Summaries
- Fix pagination bug in search results
- Bug fix: handle null user edge case
- Fixed race condition in async handler
```

## See Also

- `/memory:index` - Create project knowledge index
- `/transition:handoff` - Create manual handoff (for major milestones)
- `/transition:continue` - Resume from handoff document
