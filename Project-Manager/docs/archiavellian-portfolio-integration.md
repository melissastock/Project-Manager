# Archiavellian Portfolio Integration

Date: 2026-04-01
Status: approved for inclusion in the Project Manager portfolio
Owner: Melissa Stock

## Decision

`archiavellian` is now part of the managed system.

`Archiavellian-Archive` is also part of the managed system as the archive-side companion repository.

This means both repos should report into Project Manager rather than living as untracked standalone repositories.

## Intended Portfolio Role

### Archiavellian
- category: media or strategy
- role: primary narrative, story architecture, and productization workspace for the Archiavellian project
- intake stage: active

### Archiavellian-Archive
- category: archive
- role: supporting archive repository for evidence, source materials, and preserved project inputs tied to Archiavellian
- intake stage: archive

## Required Tracking Updates

The following portfolio surfaces should reflect this decision:

1. `config/repos.json`
2. generated `STATUS.md`
3. `README.md` managed repository snapshot
4. any future dependency or milestone views created in Project Manager

## Tonight's Immediate Outcome

This decision is now documented in the repo so the portfolio intent is explicit.

## Next Execution Steps

1. Add both repositories to `config/repos.json`.
2. Refresh `STATUS.md` with `python3 scripts/portfolio_status.py` from the local Project Manager workspace.
3. Update `README.md` to include both repositories in the managed set.
4. Confirm the local folder paths that map to the GitHub repos:
   - `archiavellian`
   - `Archiavellian-Archive`
5. Decide whether Archiavellian should also appear in any milestone, dependency, or lane-planning views once those docs are formalized.

## Dependency Note

Archiavellian should be treated as part of the same overall system as:
- Project Manager for portfolio supervision
- MJS Financial Dash where financial and evidentiary structure overlaps
- Producer / archive-style workspaces where story and source materials interact

## Current Limitation

The live manifest and generated dashboard have not yet been refreshed by script from the local workspace in this GitHub-only pass. This document records the approved direction so that the next local sync can update the generated files cleanly.
