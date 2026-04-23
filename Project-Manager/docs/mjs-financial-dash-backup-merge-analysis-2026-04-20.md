# MJS Financial Dash Backup Merge Analysis

Date: 2026-04-20

Primary repo: `MJS Financial Dash`
Backup repo: `MJS Financial Dash backup 20260310_153810`

## Scope

This review compared both repositories read-only, excluding `.git`, `.DS_Store`, and cache directories, to determine what should be preserved in the canonical repo and what should remain excluded from staging.

## Git Baseline

- Backup committed `HEAD`: `1d88e08` on `main`
- Primary committed `HEAD`: `326be3b` on `codex/finance-snapshot-onboarding`
- Result: backup `HEAD` is an ancestor of the primary repo's committed `HEAD`

Interpretation:
- This is not a separate unrelated history.
- The backup is an older snapshot of the same project lineage.
- Most preservation risk is in uncommitted backup working-tree files, not in git ancestry.

## File-Level Summary

- Primary files scanned: `1440`
- Backup files scanned: `82`
- Identical same-path files: `20`
- Same-path conflicts: `9`
- Net-new in primary: `1411`
- Net-new in backup by path: `53`
- Backup-only files already present elsewhere in primary by content hash: `50`
- Backup-only files with unique content not yet present in primary: `3`

## Already Identical

These files are byte-identical at the same relative path in both repos:

- `setup.py`
- `src/finance_snapshot/__init__.py`
- `src/finance_snapshot/analytics.py`
- `src/finance_snapshot/cli.py`
- `src/finance_snapshot/config.py`
- `src/finance_snapshot/extractors.py`
- `src/finance_snapshot/google_sources.py`
- `src/finance_snapshot/oauth.py`
- `src/finance_snapshot/reporting.py`
- `src/finance_snapshot/types.py`
- `src/finance_snapshot/utils.py`
- `tests/fixtures/sample_finance_data.json`
- `tests/test_pipeline.py`
- `tests/test_utils.py`
- `src/finance_snapshot.egg-info/*`

## Net-New In Backup

### Already Present Elsewhere In Primary

The backup's apparent net-new files are mostly already preserved under reorganized primary paths.

Examples:
- `outputs/2022_obligations.csv` -> `03_working_data/ledgers/2022_obligations.csv`
- `outputs/document_inventory.csv` -> `03_working_data/extracted_tables/document_inventory.csv`
- `outputs/risk_warnings.csv` -> `03_working_data/review_outputs/risk_warnings.csv`
- `scripts/build_attorney_case_briefing.py` -> `05_scripts/build_attorney_case_briefing.py`
- `credentials.json` -> `07_archive/restricted_review_materials_20260316/_review_needed/credentials.json`

### Unique Content Not Yet Present In Primary

Only three backup files had unique content not already present elsewhere in the primary repo:

1. `outputs/cleanup_notes.md`
2. `outputs/document_gaps_clean.csv`
3. `token.json`

Recommended handling:
- Preserve `outputs/cleanup_notes.md` as an archived superseded snapshot inside the primary repo.
- Preserve `outputs/document_gaps_clean.csv` as an archived superseded snapshot inside the primary repo.
- Do not merge `token.json`.

## Same-Path Conflicts / Overwrites

These files exist in both repos at the same relative path but differ:

- `README.md`
- `outputs.zip`
- `outputs/2026_obligations.csv`
- `outputs/debt_registry.csv`
- `outputs/financial_timeline.csv`
- `outputs/master_bill_registry.csv`
- `outputs/normalized_records.csv`
- `outputs/report.md`
- `pyproject.toml`

Recommended handling:
- Retain the primary repo's current versions.
- Do not overwrite primary working files with older backup copies.
- Treat backup-side conflicting generated outputs as already preserved elsewhere in reorganized primary paths.
- Treat `pyproject.toml` as superseded pipeline packaging state now covered by git history rather than a working-tree merge candidate.

## Low-Value / System / Export Noise

Recommended exclude set:

- `.DS_Store`
- `.pycache_local/`
- `outputs.zip`
- backup-side duplicate `outputs/` files whose content is already preserved elsewhere in primary
- direct OAuth/token material

## Risk Flags

### Secrets / Credentials

- `token.json` contains a live OAuth access token and refresh token
- `credentials.json` contains a Google OAuth client ID and client secret

### Financial / Legal / Private Material

The repository includes:
- bankruptcy preparation materials
- legal packet drafts
- financial ledgers and reconciliations
- property and transaction analysis
- document-gap and evidence-tracking outputs

These materials should be treated as private by default.

### PII / Publication Risk

Multiple files contain names, financial facts, case narratives, and document references that are unsafe for public indexing or publication without rewrite.

## Governance / Privacy Gate

Proposed classification for the changed files in the recommended stage set:

### `private-only`

- archived import of backup `cleanup_notes.md`
- archived import of backup `document_gaps_clean.csv`
- this analysis report
- merge mapping CSV
- sensitive holdback CSV
- later PM metadata updates marking the backup repo as deprecated/archive-only

### `needs rewrite before publish`

- none in the proposed stage set, because the recommendation is to keep sensitive financial/legal material private rather than rewrite it for publication

### `public-safe`

- none in the proposed stage set

## Proposed Include List

Recommended merge into `MJS Financial Dash` after approval:

- `MJS Financial Dash backup 20260310_153810/outputs/cleanup_notes.md`
  Destination: `MJS Financial Dash/07_archive/backup_repo_snapshot_20260310/outputs/cleanup_notes.md`
  Reason: unique content, but superseded and private

- `MJS Financial Dash backup 20260310_153810/outputs/document_gaps_clean.csv`
  Destination: `MJS Financial Dash/07_archive/backup_repo_snapshot_20260310/outputs/document_gaps_clean.csv`
  Reason: unique content, but superseded and private

## Proposed Exclude List

- `MJS Financial Dash backup 20260310_153810/token.json`
  Reason: active secret material

- `MJS Financial Dash backup 20260310_153810/credentials.json`
  Reason: secret material already preserved under restricted archive location in primary; do not duplicate into active paths

- `MJS Financial Dash backup 20260310_153810/outputs.zip`
  Reason: low-value generated binary, older than primary archive copy, not needed for canonical working tree

- All backup `.DS_Store` and cache files
  Reason: system noise

- All backup files whose content already exists elsewhere in primary
  Reason: already reconciled by content hash

- All same-path conflicts
  Reason: primary versions are newer and/or already supported by reorganized preserved copies

## Recommended Execution Plan

1. Copy only the two unique, non-secret backup outputs into a dedicated archive snapshot folder inside the primary repo.
2. Leave all secrets, credentials, caches, and low-value exports unstaged.
3. Validate that the new archive snapshot files match the backup hashes exactly.
4. Produce a final staged summary before commit.
5. Commit only after explicit approval of the staged set.
6. Update `Project Manager` metadata so the backup repo is clearly marked deprecated/archive-only and the primary repo is the sole canonical active repo.
7. Do not delete the backup repo in this pass.

## Retirement Plan Proposal

Recommended retirement state after verification:

- Keep the backup repo on disk temporarily as `archive-only`
- Update PM metadata/docs to say `MJS Financial Dash` is the canonical repo
- Mark `MJS Financial Dash Backup` as deprecated and retained only for rollback/audit
- Revisit physical removal no earlier than 14 days after:
  - merge verification is complete
  - reports are committed
  - user explicitly approves removal timing

## Open Questions

- Whether you want `outputs.zip` additionally preserved under a dedicated archive binary folder even though the primary already has `07_archive/stale_outputs/outputs.zip`
- Whether PM metadata should keep the backup repo listed as `archive` or switch to a stronger `deprecated/archive-only` note in the next pass
