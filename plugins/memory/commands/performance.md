---
title: performance
aliases: [metrics, usage, cost]
description: View token usage and performance metrics
allowed-tools: [Bash]
argument-hint: "[session|daily|weekly|monthly|help]"
---

# Performance Metrics

View token usage, costs, and performance metrics for your Claude Code sessions.

## Usage

```bash
# View current session metrics
/performance

# View daily metrics
/performance daily

# View weekly metrics
/performance weekly

# View monthly metrics
/performance monthly

# Get help with ccusage
/performance help
```

## Implementation

```bash
# Check if ccusage is available
if ! command -v npx >/dev/null 2>&1; then
    echo "❌ Performance monitoring requires npx (Node.js)"
    echo ""
    echo "To enable performance tracking:"
    echo "1. Install Node.js: https://nodejs.org/"
    echo "2. Run: npx ccusage@latest"
    exit 1
fi

# Parse arguments
TIMEFRAME="${ARGUMENTS:-session}"

echo "📊 Claude Code Performance Metrics"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

case "$TIMEFRAME" in
    daily|day)
        echo "📅 Daily Usage Report"
        npx ccusage@latest daily
        ;;
    weekly|week)
        echo "📅 Weekly Usage Report"
        npx ccusage@latest weekly
        ;;
    monthly|month)
        echo "📅 Monthly Usage Report"
        npx ccusage@latest monthly
        ;;
    help|--help)
        echo "📚 ccusage Help"
        npx ccusage@latest --help
        ;;
    session|*)
        echo "💬 Current Session Metrics"
        npx ccusage@latest session

        # Also show daily summary
        echo ""
        echo "📅 Today's Summary"
        npx ccusage@latest daily
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 Performance Tips:"
echo "   • Use MCP tools for efficiency:"
echo "     - Serena: 70-90% token reduction on code operations"
echo "     - Context7: 50% faster documentation lookup"
echo "     - Sequential Thinking: Better analysis with fewer iterations"
echo "   • Monitor usage regularly to optimize workflows"
echo "   • Consider caching frequently accessed documentation"
```

## Model Cost Reference

After running the bash script above, present this pricing table to the user for context.

> Prices are approximate as of early 2026. See [Anthropic pricing](https://www.anthropic.com/pricing) for current rates.

| Model | Input (per 1M) | Output (per 1M) | Context | Best For |
|-------|----------------|------------------|---------|----------|
| Opus 4 | $15 | $75 | 200K | Complex architecture, multi-file refactors, deep analysis |
| Sonnet 4 | $3 | $15 | 200K | Day-to-day development, code review, feature work |
| Haiku 3.5 | $0.80 | $4 | 200K | Quick lookups, simple edits, subagent tasks |

Prompt caching and extended thinking have separate pricing tiers not shown here.

## Usage Optimization Guide

After presenting ccusage output, analyze the user's patterns and offer relevant suggestions from this list:

**High token usage per session** — Context filling quickly
- Use `/transition:handoff` proactively at ~70% perceived context usage
- Run `/memory:index` to build project knowledge that reduces repeated exploration
- Prefer Serena MCP for code navigation (70-90% token reduction vs grep/read cycles)

**High cost relative to work output** — Model selection opportunity
- Use Sonnet for routine development; reserve Opus for complex analysis
- Haiku is ideal for subagent tasks (search, validation, formatting)
- Prompt caching reduces input costs on repeated context

**Frequent sessions on same topic** — Poor continuity between sessions
- Run `/memory:memory-update` to persist key learnings
- Use `/transition:handoff` + `/transition:continue` for explicit session continuity
- Run `/memory:index` to reduce re-exploration overhead

**Many short sessions** — Possible compaction or setup issues
- Check if project has `/memory:index` — missing project maps cause excess exploration
- Ensure CLAUDE.md has clear project context to reduce startup cost
- Consider hooks for auto-compaction (see `/setup:hooks`)

**High output-to-input ratio** — Verbose responses
- Be more specific in prompts to reduce unnecessary output
- Use `--brief` flags where available
- Break large tasks into focused subtasks

## Features

### Token Usage Tracking
- Session-level metrics via ccusage
- Daily, weekly, monthly aggregation
- Cost calculation based on model pricing

### MCP Tool Efficiency
Estimated gains when MCP servers are configured:
- **Serena**: 70-90% token reduction on code analysis
- **Context7**: 50% faster documentation access
- **Sequential Thinking**: 20-30% better analysis quality

## Graceful Degradation

Without ccusage/Node.js, still present the Model Cost Reference table and Usage Optimization Guide based on the user's qualitative description of their usage patterns.

## Integration

Performance metrics integrate with:
- `/system:status` — session management
- `/workflow:work` — work unit tracking
- `/development:analyze` — project analysis
- `/transition:handoff` — context management optimization
- `/memory:memory-update` — session continuity
- `/memory:index` — project knowledge for token efficiency

---

*Performance monitoring with model costs and optimization guidance, powered by ccusage*