# Presentations Plugin

Generate C-suite consulting presentations in McKinsey/Bain style with pyramid principle structure, quantified action titles, and automated quality validation.

## Quick Start

```bash
# From a YAML config
/deck config.yaml

# From markdown analysis outputs
/deck @outputs/workstreams/

# Specify deck type
/deck config.yaml --type board-readout
```

## Features

- **Pyramid Principle**: Vertical flow (title -> argument -> evidence) on every slide
- **Horizontal Flow**: Reading action titles in sequence tells the complete story
- **SCR Framework**: Situation-Complication-Resolution executive summaries
- **MECE Organization**: Mutually exclusive, collectively exhaustive section structure
- **Quality Validation**: 6 automated checks with scoring
- **Presenter Notes**: Conversational delivery guidance with timing cues
- **Leave-Behind Notes**: Self-contained summaries (150-200 words) for readers

## Deck Types

| Type | Use Case |
|------|----------|
| `decision-meeting` | Executive decision with options matrix and asks |
| `board-readout` | Board-level strategic summary |
| `deep-dive` | Technical deep-dive with detailed evidence |

## Input Formats

1. **YAML config** - Structured deck specification (see `examples/example-diagnostic.yaml`)
2. **Markdown synthesis** - Auto-synthesize from analysis output directories
3. **Hybrid** - YAML config referencing markdown evidence sources with `@path` notation

## Output

Markdown file with one section per slide, saved to `outputs/deliverables/drafts/`. Each slide includes:
- Quantified action title
- Supporting argument and evidence
- Presenter notes with delivery cues
- Leave-behind notes for document distribution

## Quality Validation

Every generated deck includes an automated quality report checking:

| Check | What It Validates |
|-------|-------------------|
| Horizontal Flow | Titles read as coherent narrative |
| Quantification | 80%+ titles contain numbers |
| Evidence Traceability | All claims link to sources |
| Vertical Flow | Each title supported by body |
| Presenter Notes | Conversational with cues |
| Leave-Behind Notes | Self-contained, 150-200 words |

## Examples

See `examples/` for complete input and output samples.
