# Presentations Plugin Examples

## Input Examples

### example-diagnostic.yaml
Complete YAML config for a **decision-meeting** deck (the Pipeline Conversion Diagnostic). Demonstrates all schema features: SCR framing, claims validation, MECE sections with evidence references, options matrix with scoring, multi-part recommendation with segmentation, phased roadmap, decision ask, appendix, and data gaps. ~240 lines expressing an 18-slide + appendix deck.

### example-board-readout.yaml
Shorter YAML config for a **board-readout** deck. Demonstrates how the same schema scales down for executive summaries: fewer sections, simpler evidence, focus on progress tracking and investment decisions. ~70 lines expressing a ~10-slide deck.

## Output Example

### example-output.md
Sample output showing the first 2 slides of a generated deck. Demonstrates the slide format: action titles, SCR tables, evidence tables, presenter notes with delivery cues, and leave-behind notes. Includes the quality validation report that the agent appends to every deck.

## Schema Reference

See `../schema.md` for the complete field reference with types, required/optional markers, and validation rules.

## Usage

```bash
# Generate from a YAML config
/deck examples/example-diagnostic.yaml

# Generate a board readout
/deck examples/example-board-readout.yaml

# Generate from markdown analysis outputs (auto-synthesis)
/deck @outputs/workstreams/

# Specify deck type explicitly
/deck config.yaml --type deep-dive
```

## Creating Your Own Config

1. Start with `example-board-readout.yaml` for a quick deck or `example-diagnostic.yaml` for a comprehensive one
2. Replace the content with your analysis findings
3. Use `@path` references to point at evidence files the agent should read
4. Run `/deck your-config.yaml` to generate
