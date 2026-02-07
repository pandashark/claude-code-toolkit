---
allowed-tools: [Task, Bash, Read, Write, Grep, MultiEdit, mcp__firecrawl__firecrawl_search, mcp__firecrawl__firecrawl_scrape, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[@file | #issue | description | --interview | empty] [--work-unit ID]"
description: "Explore requirements and codebase before planning"
---

# Requirements Exploration

Analyze requirements and codebase context. First step in "Explore → Plan → Code → Commit" workflow.

**Input**: $ARGUMENTS

## Sources

- `@file.md` - Read and analyze document
- `#123` - Fetch GitHub issue
- `"description"` - Natural language requirement
- `--interview` - Structured interview to elicit complete requirements
- *(empty)* - General codebase exploration

## Process

1. **Create Work Unit**
   - Generate ID: `YYYY-MM-DD_NN_topic`
   - Create `.claude/work/{id}/` with: metadata.json, requirements.md, exploration.md
   - Set as ACTIVE_WORK

2. **Analyze Source**
   - Documents: Extract requirements, identify gaps, assess complexity
   - Issues: Fetch details, understand context, map technical needs
   - Description: Clarify scope, define success criteria, identify constraints

3. **Explore Codebase**
   - Understand architecture and patterns
   - Identify integration points
   - Map affected components
   - Use Serena for semantic analysis when available

4. **Generate Output**
   - `requirements.md`: Functional/non-functional requirements, acceptance criteria, risks
   - `exploration.md`: Architecture analysis, implementation approach, key files

5. **Smart Planning**
   - Simple requirements → Generate complete plan + state.json → Ready for /next
   - Complex requirements → Generate outline → Recommend /plan

## Work Unit Structure

```
.claude/work/YYYY-MM-DD_NN_topic/
├── metadata.json      # Status, created_at, requirement_type
├── requirements.md    # Captured requirements
├── exploration.md     # Analysis findings
└── state.json        # Tasks (if plan auto-generated)
```

## Interview Mode (--interview)

When `--interview` is specified, act as an interviewer to systematically elicit requirements before proceeding with exploration. Ask questions in phases, waiting for the user's response before moving to the next phase:

1. **Vision**: What are you building? Who is it for? What problem does it solve?
2. **Scope**: What's in scope for this work? What's explicitly out of scope? What's the MVP?
3. **Technical**: Any technology constraints? Existing systems to integrate with? Performance/scale requirements?
4. **Acceptance**: How will you know it's done? What does success look like? Key acceptance criteria?
5. **Risks**: What could go wrong? What are the unknowns? Any deadlines or dependencies?

After the interview, proceed with the normal process (steps 1-5 above) using the gathered answers as the requirements source. The interview produces a more thorough `requirements.md` since it systematically covers areas the user might not think to mention.

## Next Steps

- **Clear plan generated**: "Run /next to implement"
- **Needs refinement**: "Run /plan for detailed breakdown"
- **Has ambiguities**: List clarifying questions first
