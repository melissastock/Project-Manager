# Phase 1.5 Findability-First Storage Plan - 2026-04-20

## Goal

Reduce local disk pressure while preserving fast retrieval, traceability, and publish/archive workflows.

## Operating Rule

No file is moved to cold storage unless:

1. it is indexed in a searchable manifest, and
2. its retrieval location is recorded in Project Manager docs.

## Storage Tiers

### Tier A - Hot (local, active)

Keep local when files are actively edited or currently in review.

Examples:

- `Audio Bee/audio recordings` (current metadata/redaction work)
- `Archiavellian-Archive/inbox/*` current intake batches
- active project working folders in managed repos

### Tier B - Warm (local archive snapshot + optional cloud mirror)

Keep local but compressed/snapshotted when files are needed occasionally.

Examples:

- finalized monthly intake batches
- completed source bundles already indexed

### Tier C - Cold (external drive or cloud-only archive copy)

Move off local disk when content is stable and low-edit frequency.

Examples:

- legacy large media collections
- superseded bundles with canonical replacements
- historical backups after verification

## Candidate Targets For Offload (first wave)

Ordered by expected space impact and low disruption risk:

1. `Audio Bee` non-active subsets after canonical metadata review
2. `Archiavellian-Archive` legacy backup trees and preview renders
3. `Producer` historical assets not required for current production pass

## Required Index Artifacts

Maintain these before/after any offload:

- `Archiavellian-Archive/index/archive-index.csv`
- `Archiavellian-Archive/index/archive-index.md`
- new offload ledger: `docs/storage-offload-ledger.csv`

## Offload Ledger Schema

Use one row per moved bundle:

- `bundle_id`
- `source_path`
- `offload_destination` (external path or cloud path)
- `storage_tier` (`warm` or `cold`)
- `bytes`
- `sha256_manifest_file`
- `moved_at`
- `retrieval_instructions`
- `owner`
- `notes`

## Safe Offload Procedure (per bundle)

1. Build bundle manifest with checksums.
2. Copy to destination (do not delete source yet).
3. Verify checksums at destination.
4. Write ledger row and archive-index references.
5. Perform retrieval test on one sample file.
6. Only then delete local source if tier is `cold`.

## Retrieval Standard

Every offloaded bundle must support:

- path-based lookup via `storage-offload-ledger.csv`
- topic/case lookup via `archive-index.csv`
- restore steps documented in `retrieval_instructions`

If retrieval takes more than 5 minutes for known bundle IDs, improve index instructions.

## Immediate Next Deliverables

1. Create `docs/storage-offload-ledger.csv` template.
2. Produce a ranked bundle list with estimated bytes by folder.
3. Execute one pilot offload (small, non-critical bundle) and validate restore.

## Decision Gate

Proceed to full offload waves only after:

- pilot retrieval test succeeds,
- ledger/index entries are complete,
- no active workflow depends on moved local paths.

