# Archive CMS Map

Date: 2026-04-20  
Owner: Melissa Stock  
Scope: Project Manager workspace

## Purpose

This document defines the archive that serves as a content management system (CMS), so files can be found quickly and backed up consistently.

## Canonical Archive CMS

- Primary archive CMS repository: `Archiavellian-Archive`
- Portfolio manifest source: `config/repos.json` entry named `Archiavellian-Archive`
- Current role in manifest: `archive repository for evidence, source materials, and preserved project inputs`

When we say "archive CMS" in this workspace, this repository is the default destination unless a project has its own explicit archive companion repository.

## Not The Archive CMS

These locations may contain archived or legacy material, but they are not the canonical CMS:

- `MJS Financial Dash backup 20260310_153810` (snapshot backup repo)
- `TuneFab` (legacy container in archive transition)
- `Phone Files` (intake source location, not final archive taxonomy)
- Google Drive folders (intake source location, not final archive taxonomy)

## Storage Model (Findability First)

- Intake sources (where files arrive first):
  - `Phone Files`
  - Google Drive export/sync folders
- Archive CMS destination (where preserved files live with durable structure):
  - `Archiavellian-Archive`
- Project-specific active repositories (where working files live):
  - entries in `config/repos.json` with `intake_stage` `active` or `onboarding`

Rule: source locations are for capture and transfer; archive CMS is for durable organization and retrieval.

## Proposed Archive CMS Folder Convention

Use this structure inside `Archiavellian-Archive`:

- `Archiavellian-Archive/inbox/mobile/YYYY-MM/`
- `Archiavellian-Archive/inbox/google-drive/YYYY-MM/`
- `Archiavellian-Archive/collections/<project-or-topic>/`
- `Archiavellian-Archive/evidence/<case-or-theme>/`
- `Archiavellian-Archive/reference/<domain>/`
- `Archiavellian-Archive/index/`

Use `inbox/*` only for first landing. Curate from inbox into stable `collections`, `evidence`, or `reference` paths.

## File Naming Convention

Recommended filename pattern:

`YYYY-MM-DD__source__topic__short-description.ext`

Examples:

- `2026-04-20__mobile__banking__statement-page-1.jpg`
- `2026-04-20__gdrive__legal__draft-motion-v3.docx`

Keep names lowercase except proper nouns; use hyphens for readability.

## Mobile Intake Workflow

1. Export/copy files from phone into a dated intake folder under `Phone Files`.
2. Move batch into `Archiavellian-Archive/inbox/mobile/YYYY-MM/`.
3. Rename files using the naming convention.
4. Refile curated items into:
   - `collections/` for project bundles
   - `evidence/` for legal/evidentiary material
   - `reference/` for supporting docs and context
5. Add or update an index entry (see below).

## Google Drive Intake Workflow

1. Export/sync selected Google Drive folders to a local dated transfer folder.
2. Move batch into `Archiavellian-Archive/inbox/google-drive/YYYY-MM/`.
3. Normalize names and remove exact duplicates.
4. Refile curated items into `collections/`, `evidence/`, or `reference/`.
5. Add or update an index entry.

## Archive Index Requirement

Keep a machine-readable + human-readable index in:

- `Archiavellian-Archive/index/archive-index.csv` (sortable inventory)
- `Archiavellian-Archive/index/archive-index.md` (quick manual lookup)

Minimum fields:

- `file_path`
- `source` (`mobile`, `gdrive`, `local`, etc.)
- `project_or_case`
- `category` (`collection`, `evidence`, `reference`)
- `date_captured`
- `notes`

If a file is not in the index, treat it as not yet archived.

## Classification Rules

- Active work-in-progress files belong in the relevant active project repo.
- Historical source materials and completed evidence bundles belong in the archive CMS.
- Backups/snapshots can exist separately, but should be linked from the archive index.

## Immediate Cleanup Actions

1. Confirm `Archiavellian-Archive` as the canonical archive CMS in team practice.
2. Create the folder structure above inside `Producer/archive`.
3. Ingest current `Phone Files` into `inbox/mobile` by month.
4. Ingest Google Drive exports into `inbox/google-drive` by month.
5. Build initial `archive-index.csv` from those imports.
6. Add cross-links in `Project Manager/docs` if additional archive companion repos are formalized (for example, Archiavellian archive).

## Open Decisions

- Whether `Phone Files` remains as temporary intake-only or is emptied after each ingest cycle.
- Whether Google Drive should be mirrored continuously or imported in periodic snapshots.
- Whether to add additional managed archive companion repositories to `config/repos.json`.

