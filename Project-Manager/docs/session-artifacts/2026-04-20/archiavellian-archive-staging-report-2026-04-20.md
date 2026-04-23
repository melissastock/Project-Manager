# Archiavellian-Archive Staging Report - 2026-04-20

- Generated at: `2026-04-20T12:35:23-06:00`
- Repository: `Archiavellian-Archive`
- Untracked paths detected: `403`
- Recommended include count: `398`
- Recommended exclude count: `5`
- Full path matrix: `docs/archiavellian-archive-staging-report-2026-04-20.csv`

## Top Path Prefixes

- `inbox/google-drive/2026-04/ingest-2026-04-20-net-new`: 345 files
- `reference/pm_managed_dam/2026-04-02_legal_financial_intake/01_originals`: 30 files
- `reference/pm_managed_dam/2026-04-02_legal_financial_intake/02_working`: 9 files
- `reference/pm_managed_dam/2026-04-02_legal_financial_intake/03_metadata`: 4 files
- `inbox/to-check-misc-2026-04-20/2024-10-02_ACH Centennial Accounting.pdf`: 1 files
- `inbox/to-check-misc-2026-04-20/Authorization-for-Release-and-Exchange-of-Information-2022.pdf`: 1 files
- `inbox/to-check-misc-2026-04-20/COA-Care-Management-Referral-Form ZG.pdf`: 1 files
- `inbox/to-check-misc-2026-04-20/COA-Care-Management-Referral-Form.pdf`: 1 files
- `inbox/to-check-misc-2026-04-20/Kelly Paystub 1.16.pdf`: 1 files
- `inbox/to-check-misc-2026-04-20/Request-for-Determination-and-Signature-Pages.pdf`: 1 files

## Top File Extensions

- `.docx`: 152 files
- `.pdf`: 116 files
- `.jpg`: 34 files
- `.xlsx`: 25 files
- `.m4a`: 14 files
- `.pptx`: 13 files
- `.zip`: 8 files
- `.png`: 8 files
- `.ini`: 8 files
- `.csv`: 5 files

## Recommended Exclude (do not stage)

- `inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Caches.nosync/_cacheInfo.xml` - derived GarageBand/system cache metadata
- `inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Contents/PkgInfo` - derived GarageBand/system cache metadata
- `inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/_cacheInfo.xml` - derived GarageBand/system cache metadata
- `inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/assetsmetadata.plist` - derived GarageBand/system cache metadata
- `inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/metadata.plist` - derived GarageBand/system cache metadata

## Include Scope Summary

- Stage all remaining untracked content in this repository after excluding the paths above.
- This keeps primary imported source files and archive index updates together in one evidence-state checkpoint.

## Proposed Staging Commands (not executed)

```bash
cd "Archiavellian-Archive"
git add -N "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Caches.nosync/_cacheInfo.xml" && git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Caches.nosync/_cacheInfo.xml"
git add -N "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Contents/PkgInfo" && git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Contents/PkgInfo"
git add -N "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/_cacheInfo.xml" && git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/_cacheInfo.xml"
git add -N "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/assetsmetadata.plist" && git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/assetsmetadata.plist"
git add -N "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/metadata.plist" && git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/metadata.plist"
git add .
git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Caches.nosync/_cacheInfo.xml"
git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Contents/PkgInfo"
git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/_cacheInfo.xml"
git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/assetsmetadata.plist"
git restore --staged "inbox/google-drive/2026-04/ingest-2026-04-20-net-new/Aneumind/My Song.band/Output/metadata.plist"
git status --short
```
