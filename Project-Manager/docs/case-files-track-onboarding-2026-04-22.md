# Case Files Track Onboarding - 2026-04-22

## Source

- Source location: Google Drive folder named `Case Files`
- Current connector status: Drive connector file listing was not available, but a Google Drive export zip was supplied locally.
- Local export inspected: `/Users/melissastock/Downloads/Case Files-20260422T075812Z-3-001.zip`
- Local source-of-truth policy: Google Drive is an intake source, not a canonical archive or working repo.

## Export Inventory Snapshot

- Export inspected and extracted into controlled archive intake; file contents were not reviewed.
- Total files: 95
- Uncompressed size: 1,841,333,958 bytes
- Top-level bundle counts:
  - `Evidence & Files`: 71 files
  - `Case Strategy & Analysis`: 9 files
  - `Pleadings and Legal Strategy`: 7 files
  - `Legal Correspondence`: 3 files
  - `Civil Rights Lawsuit & Public Relations`: 2 files
  - `Defense Strategy & Internal Records`: 2 files
  - `Documents`: 1 file
- Extension mix: 30 PDF, 16 XLSX, 15 DOCX, 11 MP4, 9 PNG, 6 JPG, 5 HEIC, 1 RTF, 1 MP3, 1 no-extension/system file.
- Initial track classification:
  - Legal: 83 files
  - Mixed legal/content strategy: 9 files
  - Content creator/public relations: 2 files
  - Exclude: 1 system metadata file

## Program Model

Case Files is onboarded as a two-track program:

| Track | Purpose | Canonical working home | Archive/evidence home | Public sync |
| --- | --- | --- | --- | --- |
| Legal track | Evidence, filings, counsel packets, financial/legal source material, timelines, claim support | `Divorce`, `Bankruptcy`, `2024 Taxes`, or another private legal/financial repo selected per matter | `Archiavellian-Archive` under `evidence/` or `inbox/google-drive/YYYY-MM/` until classified | No |
| Content creator track | Sanitized narrative, creator IP, production notes, scripts, arcs, public-safe derivatives | `Producer` / Archiavellian working repo after privacy review | `Archiavellian-Archive` under `collections/` or `reference/` | No by default; explicit export only |

## Classification Rules

- Treat every file in `Case Files` as restricted until reviewed.
- Do not bulk-add raw Drive contents to Project Manager, Producer, or public-facing repos.
- Legal/financial, family, medical, identity, tax, banking, court, counsel, or claim material routes to the legal track.
- Story, script, development, production, creative positioning, or creator package material routes to the content creator track only after redaction review.
- Mixed-use material stays in archive intake until a reviewer assigns primary and secondary track labels.

## Required Intake Fields

Use `docs/manifests/case-files-drive-intake-register-2026-04-22.csv` for the first pass.

Minimum fields:

- source_path
- file_name
- detected_topic
- primary_track (`legal`, `content-creator`, `mixed`, `exclude`)
- sensitivity (`legal-financial-restricted`, `family-sensitive`, `regulated-sensitive`, `ip-restricted`, `public-candidate`)
- canonical_home
- archive_home
- action (`index-only`, `copy-to-archive`, `route-to-working-repo`, `exclude`, `needs-review`)
- reviewer
- notes

## Initial Routing

- Legal track first homes:
  - `Divorce` for divorce, post-divorce litigation, custody/family-court, counsel packet, or legal evidence material.
  - `Bankruptcy` for bankruptcy filing, trustee, debt, SBA, creditor, or financial distress material.
  - `2024 Taxes` for tax-year filing, advisor packet, statement, 1095-A, W-9, return, IRS, or deduction support material.
  - `MJS Financial Dash` for normalized finance reconstruction, dashboards, and derived reporting only. Raw statements should be archived or kept in the legal/finance evidence repo selected for the matter.
- Content creator track first homes:
  - `Producer` for sanitized story architecture, development package, production planning, scripts, pitch, and audience-facing creator work.
  - `Archiavellian-Archive` for raw source, substantiation, consent, authorship, provenance, and archive-only creative evidence.

## Operating Gates

Before any file leaves Drive intake:

1. Record it in the intake register.
2. Assign primary track and sensitivity.
3. Decide whether it is raw evidence, working material, derivative content, or duplicate.
4. Route raw evidence to `Archiavellian-Archive` or the relevant private legal repo.
5. Route only sanitized derivative content to `Producer`.
6. Update the archive index if the file is copied into archive storage.

## First Pass Checklist

- Export or sync the Drive `Case Files` folder into a dated local transfer folder.
- Generate a file inventory with size, extension, modified date, and hash where possible.
- Fill the intake register with one row per file or logical bundle.
- Separate obvious excludes: `desktop.ini`, cache folders, duplicate exports, transient editor files, generated previews.
- Promote legal material before creator material so privacy and privilege boundaries are set before narrative reuse.
- Create a short decision log naming any files approved for the content creator track.

## Decision State

- Status: onboarded as governed track model.
- File-level ingest: local export zip extracted to `Archiavellian-Archive/inbox/google-drive/2026-04/case-files/`.
- Hash inventory: `Archiavellian-Archive/index/case-files-20260422-inventory.csv`.
- Default posture: restricted, private, index-first.
