# Session Handoffs

This folder stores end-of-session developer handoffs.

## Naming Convention

Use:

`YYYY-MM-DD-[short-project-name]-handoff.md`

Example:

`2026-04-01-project-manager-handoff.md`

## Purpose

Each handoff should:
- preserve factual traceability
- provide a PM-ready summary at the top
- separate facts from interpretations and opinions
- leave enough context for the next developer to resume immediately

## Related Docs

- `../SESSION_CLOSE.md`
- `../codex-close-checklist.md`
- `../developer-session-handoff-template.md` (if present)

## Suggested Flow

1. Run the handoff creation script
2. Fill in commits, files changed, commands run, and next actions
3. Record cascade scope (`all-repos`, `selected-lanes`, or `pm-portal-only`) and impacted lanes/repos.
3. Save the file in this folder
4. Use the PM ingestion pass to extract only the signal needed for portfolio updates

Scope rules live in: `../cascade-applicability-matrix.md`
