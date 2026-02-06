---
allowed-tools: [Task, Read, Write, Bash, Grep, Glob]
argument-hint: "[config.yaml | --from-markdown DIR] [--type TYPE] [--output PATH]"
description: "Generate McKinsey/Bain style C-suite presentations from analysis findings"
---

# Generate Presentation Deck

Generate a C-suite consulting presentation in McKinsey/Bain style with pyramid principle structure, quantified action titles, and automated quality validation.

**Input**: $ARGUMENTS

## Usage

```bash
/deck config.yaml                              # From YAML config (primary)
/deck --from-markdown outputs/workstreams/      # Synthesize from markdown files
/deck config.yaml --type board-readout          # Override deck type
/deck config.yaml --output custom/path/         # Override output directory
```

## Deck Types

| Type | Use Case | Slides |
|------|----------|--------|
| `decision-meeting` | Executive decision with options matrix and asks (default) | 15-25 |
| `board-readout` | Board-level strategic summary | 8-12 |
| `deep-dive` | Technical deep-dive with full evidence | 20-40 |

## Process

Execute these phases in order. Report progress at each phase.

### Phase 1: Parse Arguments

Parse `$ARGUMENTS` to determine the input mode and options.

**Argument parsing rules:**
- If argument is a `.yaml` or `.yml` file path: **YAML mode**
- If argument starts with `--from-markdown`: **Markdown synthesis mode** (next argument is the directory path)
- `--type TYPE`: Override deck type (decision-meeting, board-readout, deep-dive)
- `--output PATH`: Override output directory (default: `outputs/deliverables/drafts/`)

**If no arguments provided**, print usage help and stop:
```
Usage: /deck <config.yaml> [--type TYPE] [--output PATH]
       /deck --from-markdown <directory> [--type TYPE] [--output PATH]

See schema.md for YAML format or examples/ for templates.
```

### Phase 2: Validate Input

#### YAML Mode

1. **Check file exists** - Use Read to verify the YAML file can be read
   - If not found: `"Error: File '{filename}' not found. Check the path and try again."`
   - Suggest: List `.yaml` and `.yml` files in the current directory

2. **Read and parse YAML** - Read the file contents
   - If YAML syntax error: `"Error: Invalid YAML syntax in {filename}. Check formatting."`

3. **Validate required fields** - The YAML must contain at minimum:
   - `title` (string)
   - `audience` (string)
   - `deck_type` (string) - or use `--type` flag or default to `decision-meeting`
   - `executive_summary` with `situation`, `complication`, `resolution` (strings)
   - At least one section in `sections` with at least one finding

   If missing: `"Error: Missing required fields: [list]. See schema.md for the full schema reference."`

4. **Resolve @path references** - Scan YAML for any `@path` evidence file references
   - For each `@path`, verify the file exists
   - If a referenced file is missing: `"Warning: Evidence file '{path}' not found. Agent will generate without this evidence."`

#### Markdown Synthesis Mode

1. **Check directory exists** - Verify the directory path
   - If not found: `"Error: Directory '{path}' not found."`

2. **Scan for markdown files** - Use Glob to find all `.md` files recursively
   - If no files found: `"Error: No .md files found in '{path}'. Check the directory path."`
   - Report: `"Found N markdown files in {path}"`

3. **Read markdown files** - Read each file and prepare for agent synthesis
   - Extract headers, findings, tables, hypothesis references, and metrics
   - Note: The agent will handle the actual synthesis; the command just needs to read the files

### Phase 3: Determine Output Path

Generate the output file path:

1. **Output directory**: Use `--output PATH` if provided, otherwise `outputs/deliverables/drafts/`
2. **Create directory** if it doesn't exist: `mkdir -p {output_dir}`
3. **Generate filename**: `{YYYY-MM-DD}-{HHmm}-deck.md` using current timestamp
4. **Full path**: `{output_dir}/{filename}`

Report: `"Output will be written to: {full_path}"`

### Phase 4: Invoke Deck-Builder Agent

Use the **Task tool** to invoke the deck-builder agent with a comprehensive prompt.

**For YAML mode**, construct this prompt for the Task agent:

```
You are the deck-builder agent. Generate a complete consulting presentation deck.

**Deck Type**: {deck_type}
**Input Mode**: YAML configuration

**YAML Configuration**:
{full YAML content}

**Evidence Files** (read via @path references):
{for each @path reference, include the file content or note if missing}

**Output Requirements**:
- Follow the deck architecture for {deck_type} type
- Generate ALL slides with: action title, supporting argument, evidence, footer, presenter notes, leave-behind notes
- Run the horizontal flow test and include results
- Run all 6 quality validation checks and include the report
- If quality score < 7.0, explain what's needed to improve

Generate the complete deck now.
```

**For Markdown synthesis mode**, construct this prompt:

```
You are the deck-builder agent. Generate a complete consulting presentation deck by synthesizing findings from analysis markdown files.

**Deck Type**: {deck_type}
**Input Mode**: Markdown synthesis

**Source Files**:
{for each markdown file, include filename and content}

**Instructions**:
- Extract findings, evidence, hypothesis references, and metrics from the markdown files
- Organize into MECE sections
- Infer action titles from the evidence (quantified, outcome-focused)
- If metadata (title, audience, date) is not clear from files, use reasonable defaults and note them
- Follow the deck architecture for {deck_type} type
- Generate ALL slides with full consulting structure
- Run horizontal flow test and quality validation
- If quality score < 7.0, explain what's needed

Generate the complete deck now.
```

**Task tool configuration**:
- `subagent_type`: Use a general-purpose agent (the agent prompt encoding is in the task description)
- Provide the full deck-builder methodology context in the prompt
- The agent should return the complete markdown deck with quality report

### Phase 5: Handle Output

1. **Capture agent output** - The Task agent returns the generated deck markdown

2. **Write the deck file** - Use Write to save to the output path determined in Phase 3

3. **Report results** to the user:

```
Deck generated successfully.

Output: {output_path}
Slides: {count slides by counting "## Slide" headers}
Quality Score: {extract from Quality Validation Report section}

{If quality warnings or failures, list the action items}
```

4. **If agent returned errors or quality < 7.0**:
```
Deck generation completed with issues.

Quality Score: {score}/10 [{PASS|WARN|FAIL}]

Issues:
{list from quality validation action items}

The deck has been saved to {output_path} for review.
Consider addressing the issues and regenerating.
```

## Error Recovery

| Error | Action |
|-------|--------|
| File not found | List available YAML files in current directory |
| Invalid YAML | Point to schema.md for format reference |
| Missing required fields | Show which fields are missing with examples |
| Directory empty | Suggest checking the path or using YAML mode |
| Agent timeout | Suggest splitting into smaller sections |
| Quality < 7.0 | Save deck anyway with warnings; list specific fixes |

## Schema Reference

The full YAML schema is documented in the plugin's `schema.md` file. Key sections:

- `title`, `subtitle`, `date`, `audience`, `deck_type` (top-level metadata)
- `executive_summary` with SCR framework (`situation`, `complication`, `resolution`)
- `methodology` (scope, approach, population)
- `claims_validation` (tested claims with verdicts)
- `sections` (MECE-organized findings with evidence)
- `recommendations` (multi-part with evidence sources)
- `roadmap` (phased implementation)
- `decision_asks` (specific decisions with owners)

## Examples

Example YAML configs are available in the plugin's `examples/` directory:
- `example-diagnostic.yaml` - Full 18-slide decision meeting (146 lines)
- `example-board-readout.yaml` - Board-level summary (67 lines)
- `example-output.md` - Sample generated output showing expected format
