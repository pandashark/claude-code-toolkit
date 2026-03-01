---
description: Search session history for past decisions, discussions, and context
allowed-tools: [Bash, Read, Grep, Glob]
argument-hint: "[query] [--summaries-only] [--recent N]"
---

# /memory:search [query]

Search session history to find past decisions, discussions, and context.

**Input**: $ARGUMENTS

## How It Works

Session history is stored in `~/.claude/projects/` as JSONL files. This command searches that history to recover:
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

## Process

### 1. Parse Arguments

From `$ARGUMENTS`, extract:
- **query**: The search keywords (everything that isn't a flag)
- **summaries_only**: Whether `--summaries-only` is present
- **recent_n**: The number after `--recent` (default 20)

If no query is provided, ask the user what to search for.

### 2. Locate Session Directory

Determine the project session directory:

```bash
PROJECT_DIR=$(pwd)
CLAUDE_PROJECT="-$(echo "$PROJECT_DIR" | sed 's|^/||; s|/|-|g')"
SESSION_DIR="$HOME/.claude/projects/$CLAUDE_PROJECT"
```

If the directory doesn't exist, tell the user:
> No session history found for this project.

### 3. Search Summaries

Search the N most recent session files for summary entries matching the query:

```bash
QUERY="the search query"
N=20  # or value from --recent
for f in $(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -$N); do
    grep -i "$QUERY" "$f" 2>/dev/null | \
        jq -r 'select(.type=="summary") | .summary' 2>/dev/null
done | sort -u | head -15
```

Present results under `## Relevant Summaries`.

If `--summaries-only` was specified, stop here.

### 4. Search Discussions

Search the same session files for assistant messages containing the query, focusing on decisions and recommendations:

```bash
for f in $(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -$N); do
    DATE=$(stat -f "%Sm" -t "%Y-%m-%d" "$f" 2>/dev/null || stat -c %y "$f" 2>/dev/null | cut -d' ' -f1 || echo "Unknown")
    if grep -qi "$QUERY" "$f"; then
        echo "### Session: $DATE"
        grep -i "$QUERY" "$f" | \
            jq -r 'select(.type=="assistant") | .message.content[]? |
                   select(.type=="text") | .text' 2>/dev/null | \
            grep -i "$QUERY" | \
            grep -iE "(decided|chose|recommend|should|will use|verdict|conclusion|the answer|solution)" | \
            head -5
    fi
done
```

Present results under `## Key Discussions`.

### 5. Report Results

If no matches found in either section, tell the user:
> No results found for "[query]". Try different keywords or increase --recent.

## Output Format

```
## Relevant Summaries
- Summary headline 1
- Summary headline 2

## Key Discussions
### Session: 2025-12-10
- Decided to use RS256 for JWT signing due to key rotation needs
- Should implement refresh token rotation for security
```

## When to Use

- **Recovering lost context**: "What did we decide about X?"
- **Before starting new work**: "Have we discussed Y before?"
- **Debugging**: "When did we change Z?"
- **Continuity**: "What was the rationale for W?"

## Limitations

- Only searches current project's sessions
- Requires `jq` for JSON parsing
- Best for keyword-based searches (not semantic)
- Recent sessions searched first (older may be missed)

## See Also

- `/memory:index` - Create project knowledge index
- `/transition:handoff` - Create manual handoff (for major milestones)
- `/transition:continue` - Resume from handoff document
