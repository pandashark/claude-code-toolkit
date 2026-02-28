# Presentations Plugin

Generate C-suite consulting presentations in McKinsey/Bain style with pyramid principle structure, quantified action titles, and automated quality validation.

## Overview

The Presentations plugin transforms analysis findings into executive-ready presentation decks. It encodes McKinsey pyramid principle methodology, SCR (Situation-Complication-Resolution) framing, and MECE organization into every deck it produces. The output is markdown-formatted slides with presenter notes, leave-behind notes, and an automated quality validation report.

Use this plugin when you need to present analytical findings to senior leadership, board members, or cross-functional stakeholders in a structured, evidence-backed format.

## Quick Start

```bash
# Generate a deck from a YAML configuration
/deck findings.yaml

# Synthesize a deck from existing markdown analysis files
/deck --from-markdown outputs/workstreams/

# Generate a board-level summary
/deck findings.yaml --type board-readout
```

Output is saved to `outputs/deliverables/drafts/YYYY-MM-DD-HHmm-deck.md` by default.

## Core Methodology

The deck-builder agent follows established consulting presentation frameworks:

- **Pyramid Principle** (Barbara Minto): Lead with the answer, then support. Every slide flows top-down from action title to supporting argument to evidence.
- **SCR Framework**: Executive summaries follow Situation → Complication → Resolution to frame the narrative arc.
- **MECE Organization**: Sections are mutually exclusive and collectively exhaustive. No overlaps, no gaps.
- **Horizontal Flow**: Reading only the slide titles tells the complete story. If a colleague reads just the title strip, they understand the full argument.
- **1-3-10 Rule**: Grasp the point in 1 second (title), understand the logic in 3 seconds (argument), act on the evidence in 10 seconds (data).
- **Quantified Action Titles**: 80%+ of titles must contain a specific number. "Revenue grew" is rejected; "Revenue grew 23% YoY to $4.2B" passes.

## The `/deck` Command

### Purpose

Generate a complete consulting presentation deck from structured YAML input or by synthesizing existing markdown analysis outputs.

### Input Modes

| Mode | Trigger | Best For |
|------|---------|----------|
| **YAML** | `/deck config.yaml` | Structured deck from prepared findings |
| **Markdown synthesis** | `/deck --from-markdown DIR` | Auto-synthesize from analysis output directories |
| **Hybrid** | YAML with `@path` references | YAML structure + evidence pulled from files |

### Usage

```bash
/deck config.yaml                              # From YAML config (primary)
/deck --from-markdown outputs/workstreams/      # Synthesize from markdown files
/deck config.yaml --type board-readout          # Override deck type
/deck config.yaml --output custom/path/         # Override output directory
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--type TYPE` | Deck type: `decision-meeting`, `board-readout`, `deep-dive` | `decision-meeting` |
| `--output PATH` | Output directory | `outputs/deliverables/drafts/` |
| `--from-markdown DIR` | Switch to markdown synthesis mode | - |

### Output

Markdown file with one section per slide, saved with timestamp filename (`2026-02-06-1430-deck.md`). Each slide includes:

- Quantified action title
- Supporting argument and evidence
- Footer with slide number, source hypothesis IDs, and classification
- Presenter notes with delivery cues (pauses, emphasis, transitions)
- Leave-behind notes (150-200 words, self-contained for absent stakeholders)

A **Quality Validation Report** is appended to every generated deck.

**Agent**: `deck-builder` (consulting presentation specialist with McKinsey/Bain methodology)

## Deck Types

| Type | Use Case | Slide Count | When to Use |
|------|----------|-------------|-------------|
| `decision-meeting` | Executive decision with options matrix and asks | 15-25 | Comprehensive analysis with recommendation and decision ask |
| `board-readout` | Board-level strategic summary | 8-12 | C-suite brief focused on progress, risks, and asks |
| `deep-dive` | Technical deep-dive with full evidence | 20-40 | Stakeholder or team working session with detailed methodology |

### Type-Specific Requirements

- **`decision-meeting`**: Requires `recommendations` and `decision_ask` sections. Includes options matrix with scoring, implementation roadmap, and explicit asks with owners and deadlines.
- **`board-readout`**: Requires `executive_summary`. Shorter format focused on strategic framing, progress signals, and a small number of targeted asks.
- **`deep-dive`**: Requires `methodology`. Includes full evidence tables, control analysis, appendices with raw data, and detailed statistical backing.

## Input Schema

The full YAML schema is documented in [`schema.md`](schema.md). Here is the structure overview:

```yaml
# Required top-level fields
title: string              # Deck title
subtitle: string           # Subtitle/tagline
date: string               # Presentation date
audience: string           # Target audience
deck_type: string          # decision-meeting | board-readout | deep-dive

# SCR Framework (required)
executive_summary:
  situation: string        # Current state
  complication: string     # What changed / what's wrong
  resolution: string       # Recommended path forward
  key_numbers:             # 3-5 headline metrics (optional)
    - string

# Methodology (required for deep-dive)
methodology:
  scope: string
  approach: string
  data_sources: [string]

# Findings organized by theme (required)
sections:
  - title: string
    key_finding: string
    slides:
      - action_title: string         # Quantified "so what"
        hypothesis_ids: [string]     # Traceability
        data_points:                 # Key metrics
          - metric: string
            value: string

# Recommendations (required for decision-meeting)
recommendations:
  preferred: string
  options:
    - name: string
      score: float
      description: string

# Decision ask (required for decision-meeting)
decision_ask:
  decisions:
    - decision: string
      owner: string
      by_when: string
```

### Evidence Linking

Use `@path` references to point the agent at source files:

```yaml
evidence_source: "@outputs/workstreams/01-source-performance/"    # Directory
evidence_source: "@outputs/workstreams/01-source-performance/A1.md"  # Specific file
evidence_source: "@docs/hypotheses_matrix.md"                     # Documentation
```

The agent reads these files and extracts relevant data, metrics, and tables for slide generation.

## Examples

Three complete examples are provided in the `examples/` directory.

### Example 1: Decision Meeting (Full Diagnostic)

**File**: [`examples/example-diagnostic.yaml`](examples/example-diagnostic.yaml) (146 lines)

A complete 18-slide decision meeting deck from a pipeline conversion diagnostic. Demonstrates all schema features: SCR framework, claims validation, MECE sections, options matrix with scoring, multi-part recommendation, 90-day roadmap, and decision asks.

```bash
/deck examples/example-diagnostic.yaml
# Output: outputs/deliverables/drafts/2026-02-06-1430-deck.md
# Result: 18 slides + 6 appendix, quality score 9.4/10
```

### Example 2: Board Readout

**File**: [`examples/example-board-readout.yaml`](examples/example-board-readout.yaml) (67 lines)

A shorter board-level update deck focused on implementation progress, early impact signals, and targeted asks. Demonstrates the `board-readout` type with strategic framing.

```bash
/deck examples/example-board-readout.yaml
# Output: outputs/deliverables/drafts/2026-02-06-1430-deck.md
# Result: 8-10 slides, focused on progress + asks
```

### Example 3: Markdown Synthesis

Synthesize a deck directly from an analysis output directory without writing YAML:

```bash
/deck --from-markdown outputs/workstreams/03-market-fit/
# Agent extracts findings, evidence, and metrics from markdown files
# Infers action titles, organizes into MECE sections
# Output: outputs/deliverables/drafts/2026-02-06-1430-deck.md
```

### Example 4: Custom Output Path

```bash
/deck findings.yaml --type deep-dive --output presentations/q1-review/
# Generates a deep-dive deck saved to presentations/q1-review/
```

## Quality Validation

Every generated deck includes an automated quality report with 6 checks:

| Check | Weight | What It Validates | Pass Threshold |
|-------|--------|-------------------|----------------|
| **Horizontal Flow** | 2.0 | Titles read as coherent narrative when read in sequence | Logical story arc |
| **Quantification** | 1.5 | Action titles contain specific numbers | 80%+ of titles |
| **Evidence Traceability** | 1.5 | All claims link to hypothesis IDs or source files | 100% sourced |
| **Vertical Flow** | 2.0 | Each slide has title → argument → evidence → footer | All 4 elements |
| **Presenter Notes** | 1.5 | Conversational tone with delivery cues (pauses, emphasis) | Every slide |
| **Leave-Behind Notes** | 1.5 | Self-contained, 150-200 words, readable by absent stakeholders | Every slide |

**Scoring**: Weighted sum out of 10.0 maximum. Decks scoring below 7.0 are flagged with specific action items for improvement.

**Output format** (appended to deck):

```
## Quality Validation Report

| Check | Status | Details |
|-------|--------|---------|
| Horizontal Flow | PASS | 18 titles read as coherent narrative |
| Quantification | PASS | 16/18 titles contain numbers (89%) |
| ...

Overall Score: 9.4/10
```

## Integration with Claude Code

### Step 1: Configure Marketplace

Add the toolkit as a plugin marketplace in your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "aai-plugins": {
      "source": {
        "source": "directory",
        "path": "/path/to/claude-code-toolkit/plugins"
      }
    }
  }
}
```

### Step 2: Enable the Plugin

Add `presentations` to your enabled plugins:

```json
{
  "enabledPlugins": {
    "presentations@aai-plugins": true
  }
}
```

### Step 3: Verify

Restart Claude Code. The `/deck` command should appear in autocompletion.

### Full Example

A project using the presentations plugin alongside other toolkit plugins:

```json
{
  "extraKnownMarketplaces": {
    "aai-plugins": {
      "source": {
        "source": "directory",
        "path": "/path/to/claude-code-toolkit/plugins"
      }
    }
  },
  "enabledPlugins": {
    "workflow@aai-plugins": true,
    "development@aai-plugins": true,
    "memory@aai-plugins": true,
    "presentations@aai-plugins": true
  }
}
```

## Troubleshooting

### `/deck` command not appearing

Restart Claude Code after modifying `.claude/settings.json`. Verify the marketplace path points to the correct directory containing the `presentations/` plugin folder.

### YAML validation errors

Check your YAML against the examples in `examples/` or the full schema in [`schema.md`](schema.md). Common issues:
- Missing required fields (`title`, `audience`, `deck_type`, `executive_summary`)
- Incorrect indentation (YAML is whitespace-sensitive)
- Unquoted strings containing colons or special characters

### Quality score below 7.0

Review the specific check failures in the Quality Validation Report appended to the deck. Common fixes:
- **Low quantification**: Add numbers to action titles ("improved" → "improved 23%")
- **Missing traceability**: Add `hypothesis_ids` or `evidence_source` to slides with data claims
- **Weak presenter notes**: Add delivery cues like `[pause]`, `[emphasis]`, transitions between slides

### Output not generated

Verify the input file exists and the output directory is writable. Check for YAML syntax errors by reviewing the error message. If using `--from-markdown`, ensure the directory contains `.md` files.

### Context window exceeded

For very large decks (40+ slides) or many evidence files, the agent may hit context limits. Strategies:
- Reduce the number of `@path` evidence references
- Summarize evidence in the YAML rather than referencing raw files
- Split into multiple smaller decks by section

## Generated Deck Examples

- **Gold standard**: [`examples/example-output.md`](examples/example-output.md) - Sample 2-slide output showing the expected format with action titles, SCR framework, presenter notes, and leave-behind notes
- **Full validation**: The plugin was validated against an 18-slide diagnostic deck (975 lines), scoring 9.4/10 with 6/6 quality checks passed

## Advanced Usage

### Custom Output Path

```bash
/deck input.yaml --output presentations/board-meeting/
```

### Deck Type Override

Override the `deck_type` in the YAML without editing the file:

```bash
/deck diagnostic.yaml --type board-readout
```

This generates a shorter board-level deck from a full diagnostic YAML by selecting only the most strategic findings.

### Adapting for Other Domains

The plugin is domain-agnostic. While examples use pipeline analytics, the schema works for any analytical domain:

- Product launch readouts
- Market entry analysis
- Operational improvement diagnostics
- M&A due diligence summaries
- Quarterly business reviews

Replace `hypothesis_ids` with your own traceability scheme and update `sections` to match your analysis structure.

## File Structure

```
presentations/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/
│   └── deck.md                  # /deck command definition
├── agents/
│   └── deck-builder.md          # Core agent (McKinsey/Bain methodology)
├── examples/
│   ├── example-diagnostic.yaml  # Full decision-meeting example (146 lines)
│   ├── example-board-readout.yaml  # Board readout example (67 lines)
│   ├── example-output.md        # Sample generated output
│   └── README.md                # Examples directory guide
├── schema.md                    # Complete YAML schema reference
└── README.md                    # This file
```

## License

MIT. Methodology based on McKinsey Pyramid Principle (Barbara Minto) and BCG/Bain presentation frameworks.
