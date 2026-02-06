# Deck YAML Schema Reference

## Overview

The deck YAML schema defines the input format for the `/deck` command. It is a **concise configuration** (target: <200 lines) that the deck-builder agent expands into a full presentation with evidence, presenter notes, and leave-behind notes.

The user provides **structure and key data**; the agent reads evidence files (via `@path` references) and generates the complete deck.

## Deck Types

| Type | Purpose | Typical Length | Key Sections |
|------|---------|---------------|--------------|
| `decision-meeting` | Executive decision with options matrix | 15-25 slides | SCR, findings, options, ask |
| `board-readout` | Board-level strategic summary | 8-12 slides | SCR, highlights, outlook |
| `deep-dive` | Technical deep-dive with full evidence | 20-40 slides | Methodology, detailed findings, appendix |

---

## Top-Level Fields

```yaml
# Required
title: string              # Deck title
subtitle: string           # Subtitle/tagline
date: string               # Presentation date
audience: string           # Target audience
deck_type: string          # decision-meeting | board-readout | deep-dive

# Optional
author: string             # Preparer/team name
classification: string     # confidential | internal | public (default: confidential)
duration_minutes: int      # Expected presentation time
```

## Executive Summary (SCR Framework)

```yaml
executive_summary:
  situation: string        # Current state (required)
  complication: string     # What changed / what's wrong (required)
  resolution: string       # Recommended path forward (required)
  governing_thought: string  # 1-2 sentence synthesis (optional, agent generates if omitted)
  key_numbers:             # Headline metrics (optional)
    - string
    - string
```

## Methodology

```yaml
methodology:
  scope: string            # What was tested/analyzed (required)
  approach: string         # How it was tested (required)
  data_sources:            # Where data came from (required)
    - string
  population: string       # Sample size / universe (optional)
  time_period: string      # Date range (optional)
  caveats:                 # Known limitations (optional)
    - string
```

## Findings Sections (MECE)

Sections organize findings by decision area or theme. Each section can contain multiple slides.

```yaml
sections:
  - title: string          # Section title (required)
    decision: string       # Decision area ID, e.g., "A" (optional)
    key_finding: string    # One-line summary (required)
    evidence_source: string  # @path to workstream directory (optional)
    slides:                # Individual slides within this section
      - action_title: string         # Quantified "so what" (required)
        supporting_argument: string  # Bridge between title and evidence (optional)
        evidence_source: string      # @path to specific file/dir (optional)
        hypothesis_ids:              # Traceability to hypothesis matrix
          - string
        data_points:                 # Key metrics for this slide
          - metric: string
            value: string
            comparison: string       # e.g., "vs 4.9% for SSR" (optional)
            trend: string            # e.g., "declining", "improving" (optional)
        evidence_tables:             # Structured data tables
          - title: string
            rows:
              - label: string
                values: [string]
                highlight: bool      # Emphasize this row (optional)
                footnote: string     # Annotation (optional)
        proven_levers:               # Actionable levers extracted from evidence
          - lever: string
            effect: string           # e.g., "+21.5pp"
            hypothesis_id: string
        control_analysis:            # For findings with confound controls
          - control: string          # Variable controlled for
            before: string           # Raw effect
            after: string            # Controlled effect
            persistence: string      # % of effect remaining
```

## Claims Validation (Contradictions)

For decks that challenge existing narratives:

```yaml
claims_validation:
  summary: string          # e.g., "5 validated | 11 contradicted | 4 partial"
  source_documents:        # Where claims originated
    - string
  claims:
    - claim: string        # What was believed (required)
      source: string       # Who said it (required)
      verdict: string      # VALIDATED | CONTRADICTED | PARTIAL (required)
      reality: string      # What data shows (required)
      hypothesis_id: string  # Finding that tested it (required)
      implication: string  # Strategic consequence (optional)
```

## Options Matrix

```yaml
recommendations:
  preferred: string        # Name of recommended option (required)
  scoring:                 # Scoring methodology (optional)
    formula: string        # How composite is calculated
    criteria:
      - name: string       # e.g., "Impact"
        weight: string     # e.g., "35%"
  options:
    - name: string         # Option name (required)
      score: float         # Composite score (required)
      description: string  # What this option means (required)
      impact: int          # Score 1-5 (optional)
      effort: int          # Score 1-5 (optional)
      risk: int            # Score 1-5 (optional)
      time: int            # Score 1-5 (optional)
      rationale: string    # Why this score (optional)
      highlight: bool      # Mark as recommended (optional)
  fallback: string         # Alternative if preferred is rejected (optional)
  why_winner: string       # Why the preferred option wins (optional)
```

## Recommendation Detail

```yaml
recommendation:
  parts:                   # Multi-part recommendation (optional)
    - name: string         # Part title (required)
      prerequisite: bool   # Must complete before others (optional)
      actions:
        - string           # Action with evidence reference, e.g., "Standardize method (E11)"
      segmentation:        # For segment-specific recs (optional)
        keep:
          - segment: string
            effect: string
        redirect:
          - segment: string
            current: string
            target: string
            gap: string
```

## Implementation Roadmap

```yaml
roadmap:
  total_days: int          # Implementation horizon (optional)
  phases:
    - name: string         # Phase name (required)
      days: string         # e.g., "0-30" (required)
      theme: string        # Phase objective (optional)
      actions:
        - string           # Action description (required)
      success_metrics:     # How to measure (optional)
        - string
  decision_gates:          # Go/no-go points (optional)
    - name: string
      day: int
      decision: string
  critical_path:           # Dependency chain (optional)
    - string
```

## Decision Ask

```yaml
decision_ask:
  decisions:
    - decision: string     # What needs to be decided (required)
      owner: string        # Who decides (required)
      by_when: string      # Deadline (required)
  if_decided: string       # What happens if yes (optional)
  if_not_decided: string   # What happens if deferred (optional)
```

## Appendix

```yaml
appendix:
  - title: string          # Appendix section title (required)
    content_ref: string    # @path to source document (required)
    summary: string        # Brief description (optional)
```

## Data Gaps

```yaml
data_gaps:
  - gap: string            # What's missing (required)
    impact: string         # How it affects conclusions (required)
    hypothesis_id: string  # Which hypothesis was skipped (optional)
```

---

## Evidence Linking Patterns

### @path References

Use `@path` to point the agent at files to read for evidence:

```yaml
evidence_source: "@outputs/workstreams/01-source-performance/"    # Directory
evidence_source: "@outputs/workstreams/01-source-performance/A1_summary.md"  # File
evidence_source: "@docs/hypotheses_matrix.md"                     # Doc reference
```

The agent reads these files and extracts relevant data for slide generation.

### Hypothesis ID Traceability

Every slide links to hypothesis IDs for auditability:

```yaml
hypothesis_ids: ["A1", "A2", "B3"]  # On a slide
footer: "5 | A1, A2, B3 | CONFIDENTIAL"  # Auto-generated
```

### Control Analysis

For causal claims, show what happens after controlling for confounds:

```yaml
control_analysis:
  - control: "Segment"
    before: "+19.0pp"
    after: "+18.0pp"
    persistence: "95%"
```

---

## Validation Rules

The agent validates the YAML config against these rules:

1. **Required fields**: title, subtitle, date, audience, deck_type, executive_summary (with SCR)
2. **Quantification**: Action titles should contain numbers (agent warns if <80%)
3. **Evidence traceability**: Slides with data claims must have hypothesis_ids or evidence_source
4. **MECE**: Section titles should not overlap in scope
5. **Deck type constraints**: decision-meeting requires recommendations + decision_ask; board-readout requires executive_summary; deep-dive requires methodology
