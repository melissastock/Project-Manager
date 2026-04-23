# Archiavellian Pre-Commit Checklist - 2026-04-20

- Generated at: `2026-04-20T12:40:14-06:00`
- Repository: `Archiavellian-Archive`
- Staged files: `273`
- Untracked files still present (intentionally held back): `130`

## Boss Rules Compliance (Project Manager)

- [x] **Gate 1 Code Review posture applied**: staging narrowed and risk classes identified; security and artifact passes completed.
- [x] **Gate 2 QC/Validation applied**: staged-state verified after each pass (`git diff --cached --stat`), exclusions verified by report files.
- [x] **Gate 3 Governance/Privacy applied**: 85 sensitive candidates intentionally unstaged; low-value artifacts intentionally unstaged.
- [x] **Required artifacts present**: staging report + sensitive review + artifact hardening report.
- [ ] **Commit approved by user** (pending explicit go/no-go).

## Repo Integrity

- [x] Correct repo targeted (`Archiavellian-Archive`).
- [x] Excluded derived cache files remain unstaged.
- [x] Sensitive candidates remain unstaged pending explicit review.
- [x] Low-value system/media artifacts remain unstaged.

## Staged Scope Snapshot

- `inbox/google-drive/2026-04/ingest-2026-04-20-net-new`: 258 files staged
- `reference/pm_managed_dam/2026-04-02_legal_financial_intake/03_metadata`: 4 files staged
- `reference/pm_managed_dam/2026-04-02_legal_financial_intake/01_originals`: 2 files staged
- `inbox/to-check-misc-2026-04-20/2024-10-02_ACH Centennial Accounting.pdf`: 1 files staged
- `inbox/to-check-misc-2026-04-20/Request-for-Determination-and-Signature-Pages.pdf`: 1 files staged
- `index/archive-index.csv`: 1 files staged
- `index/archive-index.md`: 1 files staged
- `reference/pm_managed_dam/2026-04-02_legal_financial_intake/00_intake`: 1 files staged

## Top Staged Extensions

- `.docx`: 145
- `.pdf`: 45
- `.xlsx`: 22
- `.m4a`: 14
- `.pptx`: 13
- `.png`: 8
- `.zip`: 5
- `.csv`: 5
- `.md`: 5
- `.pages`: 4

## Security Holdback (Do Not Commit Yet)

- Sensitive holdback report: `docs/archiavellian-sensitive-staging-review-2026-04-20.md`
- Artifact holdback report: `docs/archiavellian-artifact-hardening-review-2026-04-20.md`
- Initial include/exclude matrix: `docs/archiavellian-archive-staging-report-2026-04-20.md`

## Pre-Commit Decision

- Recommended: commit staged 273-file evidence package only after you confirm no additional privacy holdbacks are required.
- Next action after commit: proceed to `MJS Financial Dash backup 20260310_153810` cleanup queue item.
