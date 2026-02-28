---
allowed-tools: [Read, Write, Task, Bash, Grep, Glob, mcp__sequential-thinking__sequentialthinking, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols]
argument-hint: "[file/directory] [--spec requirements.md] [--systematic] [--semantic] [--fresh]"
description: "Code review: bugs, design flaws, dead code, with prioritized action plan"
---

# Code Review

Practical code review focused on bugs, design issues, and maintainability.

**Input**: $ARGUMENTS

## Usage

```bash
/review                        # Review entire project
/review src/auth.py            # Review specific file
/review --spec design.md       # Validate against requirements
/review --systematic           # Structured reasoning for complex code
/review --semantic             # Use Serena (70-90% token reduction)
/review --fresh                # Fresh-eyes review (writer/reviewer pattern)
```

## Focus Areas

1. **Bugs**: Logic errors, edge cases, error handling, null checks
2. **Design**: Organization, coupling, SOLID violations, patterns
3. **Dead Code**: Unused functions, imports, variables, commented code
4. **Quality**: Readability, complexity, naming, documentation gaps
5. **Performance**: Obvious inefficiencies, N+1 queries, memory leaks

## NOT Included (By Design)

- Security scanning → use specialized tools
- Infrastructure audits → use `/audit`

## Output Format

```markdown
# Code Review Results

## Summary
Brief overview of findings.

## Critical Issues (Fix Immediately)
- **Issue**: [description]
  - **Location**: file:line
  - **Impact**: [why it matters]
  - **Fix**: [specific steps]

## Important Issues (Fix Soon)
[same format]

## Minor Issues (Fix When Convenient)
[same format]

## Positive Observations
- Well-implemented patterns
- Good practices found

## Action Plan
1. Immediate: [critical fixes]
2. This Sprint: [important improvements]
3. Backlog: [minor cleanups]

## Estimated Effort
- Critical: X hours
- Important: Y hours
- Minor: Z hours
```

## Fresh-Eyes Review (--fresh)

The `--fresh` flag activates the **writer/reviewer pattern**: run this in a NEW Claude Code session (not the one that wrote the code) for an unbiased, independent review.

**When `--fresh` is set:**
- Assume nothing about the author's intent — form your own understanding from the code alone
- Do not give benefit of the doubt on unclear logic — flag it
- Apply stricter standards: if you have to think hard about what code does, it needs better naming or comments
- Explicitly check that the code does what the surrounding documentation/tests claim
- Challenge architectural decisions — ask "why not X?" for non-obvious choices

**How to use the writer/reviewer pattern:**
1. Session A writes the code (normal development)
2. Open a new terminal with a fresh Claude Code session
3. In Session B, run `/review --fresh [target]`
4. Session B reviews without the implementation context that biases Session A

## Integration

After review: `/fix review` to apply recommended fixes
