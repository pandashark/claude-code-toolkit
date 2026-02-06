# Presentations Plugin Examples

## Files

### example-diagnostic.yaml
A complete YAML configuration for the Pipeline Conversion Diagnostic deck. Demonstrates all schema fields including SCR framing, MECE sections, evidence source references, recommendations with scoring, and phased roadmap.

### example-output.md
Sample output showing the first few slides of a generated deck. Demonstrates the slide format with action titles, presenter notes, leave-behind notes, and the quality validation report.

## Usage

```bash
# Generate a deck from the example config
/deck examples/example-diagnostic.yaml

# Generate from markdown analysis outputs
/deck @outputs/workstreams/
```
