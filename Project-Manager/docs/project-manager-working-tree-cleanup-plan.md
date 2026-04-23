# Project Manager Working Tree Cleanup Plan

## Purpose

This plan breaks the current top-level Project Manager working tree noise into safe cleanup batches.

The goal is to reduce ambiguity and restore trust in the parent repo without using destructive commands or accidentally sweeping unrelated work into one large commit.

## Current Noise Classes

### Class A: legitimate child repo pointer drift

These are modified gitlinks because child repositories moved forward locally.

Current examples:

- `Aneumind and TC Structure`
- `App Builder/Teach/home-learning-playbook`
- `App Builder/Teach/zahmeir-learning-system`
- `Archiavellian-Archive`
- `MJS Financial Dash`
- `MJS Financial Dash backup 20260310_153810`
- `Momentum-OS`
- `Producer`

Action:

- inspect each child repo individually
- decide whether the local child repo commits should be kept, pushed, and reflected in PM
- update the parent gitlink only after each child repo is intentionally reviewed

### Class B: top-level parent files with direct edits

These are files in the PM repo itself, not child repos.

Current examples:

- `Divorce/draft_motion_for_contempt_and_enforcement_23DR30686.md` deleted
- `Divorce/master_handoff_2026-04-11.md` deleted
- `Divorce/forensic_timeline_evidence_map_23DR30686.md` modified
- `Divorce/petitioners_damages_ledger_23DR30686.md` modified

Action:

- treat these as a separate legal-sensitive cleanup lane
- do not bundle them with portfolio tooling or scaffold work
- review intent before any stage or commit action

### Class C: probable duplicate artifact files with ` 2` suffixes

These appear to be duplicated files created outside the normal repo workflow.

Examples include many files under `docs/` and `scripts/` with names ending in ` 2.md`, ` 2.csv`, ` 2.py`, or ` 2.txt`.

Action:

- compare each duplicate against its non-suffixed twin
- decide whether the suffixed file is newer, redundant, or accidental
- commit only intentional keeps; remove only after verification

### Class D: generated audit and cleanup artifacts

These include large batches of CSV and markdown artifacts tied to archival review, dedupe, and ingest work.

Action:

- cluster by theme rather than filename count
- decide whether each cluster belongs in the PM repo, a child repo, or outside version control
- if retained, normalize naming and avoid duplicated ` 2` variants

## Recommended Cleanup Sequence

1. **Stabilize parent-only duplicate files**
   - start with the `docs/* 2.*` and `scripts/* 2.*` class
   - this is the noisiest and easiest batch to misunderstand later

2. **Review legal-sensitive parent edits separately**
   - isolate the `Divorce/` modifications and deletions
   - do not mix them with documentation housekeeping

3. **Review child repo drift one repo at a time**
   - pick a repo, inspect local status, decide keep-or-discard, then update the PM pointer intentionally
   - suggested order: `Momentum-OS`, `Producer`, `Aneumind and TC Structure`, `Archiavellian-Archive`, `Teach` repos, `MJS Financial Dash`, `MJS Financial Dash backup`

4. **Normalize generated audit artifacts**
   - group by theme, confirm whether they belong in PM, and remove accidental duplicates only after verification

## Safe Operating Rules

- do not run destructive bulk cleanup commands
- do not stage broad globs from the top-level PM repo
- prefer one cleanup class per commit
- if a file's origin is unclear, treat it as keep-until-reviewed
- update `STATUS.md` only after meaningful cleanup batches, not after every exploratory check

## Practical Next Batch

If we start the cleanup next, the safest first batch is:

1. review `docs/* 2.*` and `scripts/* 2.*`
2. classify them into `keep canonical`, `keep suffixed`, or `remove after verification`
3. make a small parent-only cleanup commit

That gives the repo a meaningful trust improvement without touching legal-sensitive files or child repo histories yet.
