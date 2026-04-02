# SESSION_CLOSE.md

Use this file as the standard instruction for ending any development session.

## Requirement
Every session must end with a **Developer Session Handoff** markdown file that is factual, traceable, and complete.

## Core Rules

1. **Facts must be verifiable**
   - Supported by commit SHA, file path, command output, or test/log output
   - If not verifiable, move it to Interpretation or Opinion

2. **Separate fact / interpretation / opinion**
   - Facts → verifiable only
   - Interpretations → clearly labeled conclusions
   - Opinions → explicitly labeled as "Opinion:"

3. **Preserve raw reference material**
   - Do not delete or compress evidence
   - Keep commits, files, commands, and notes intact

4. **No handoff = session not complete**

## Output Location

Create the handoff file at:

`docs/session-handoffs/YYYY-MM-DD-[short-project-name]-handoff.md`

Create the folder if it does not exist.

## Required Sections (High Level)

- PM-Ready Summary (top, short, factual)
- Evidence Log (commits, files, commands)
- Fact vs Interpretation vs Opinion
- Context for next developer
- Work status
- Dependencies
- Open questions
- Issues / challenges
- System impact
- Validation / testing
- Raw notes

## Session Close Procedure

1. Gather evidence (commits, files, commands, tests)
2. Write PM-ready summary (short, factual)
3. Classify facts vs interpretations vs opinions
4. Preserve raw notes
5. Save handoff file
6. State PM update requirements (repos.json, STATUS.md, dependencies, or none)

## Portfolio Rules

If the session changes:
- project list
- project status
- dependencies
- archive vs active classification

Then the handoff must explicitly state:
- what changed
- what PM docs need updating
- what is local vs pushed

## Evidence-Sensitive Work

- Default to factual statements
- Do not infer intent
- Do not collapse evidence into conclusions
- Call out uncertainty directly

## Completion Standard

A session is complete only if:
- Handoff file exists
- Summary is filled
- Evidence is captured
- Fact vs interpretation is separated
- Next actions are clear
