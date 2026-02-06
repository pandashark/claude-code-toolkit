---
allowed-tools: [Task, Read, Write, Bash, Grep, Glob]
argument-hint: "[config.yaml | @analysis.md] [--type deck_type]"
description: "Generate a McKinsey/Bain style presentation deck"
---

# Generate Presentation Deck

Generate a C-suite consulting presentation in McKinsey/Bain style with pyramid principle structure, quantified action titles, and quality validation.

**Input**: $ARGUMENTS

## Deck Types

- `decision-meeting` (default) - Executive decision deck with options matrix and asks
- `board-readout` - Board-level summary with strategic framing
- `deep-dive` - Technical deep-dive with detailed evidence

## Input Formats

1. **YAML config** (primary): Structured deck specification file
   ```
   /deck config.yaml
   ```

2. **Markdown synthesis** (secondary): Point at analysis outputs for automatic synthesis
   ```
   /deck @outputs/workstreams/
   ```

3. **Hybrid**: YAML config that references markdown files as evidence sources
   ```
   /deck config.yaml  # where config references @file paths
   ```

## Process

1. **Parse Input**: Read YAML config or scan markdown directory for synthesis
2. **Validate Schema**: Ensure all required fields present (title, audience, sections)
3. **Launch Agent**: Invoke deck-builder agent with parsed configuration
4. **Generate Deck**: Agent produces structured markdown with all slide types
5. **Quality Validation**: Run 6 automated checks (horizontal flow, quantification, traceability, vertical flow, presenter notes, leave-behind)
6. **Write Output**: Save to `outputs/deliverables/drafts/{deck-name}.md`

## Output

- Markdown deck file with one section per slide
- Each slide: action title, body, presenter notes, leave-behind notes
- Quality validation report appended as final section
- Saved to `outputs/deliverables/drafts/`
