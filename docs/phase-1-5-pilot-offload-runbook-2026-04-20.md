# Phase 1.5 Pilot Offload Runbook - 2026-04-20

- Pilot bundle: `Archiavellian-Archive/previews/ql`
- Files in bundle: 6
- Bundle bytes: 9235940
- SHA256 manifest: `docs/manifests/pilot-offload-2026-04-20-ql-sha256.txt`

## Pilot Validation Result

- Status: `Validated`
- Offload destination: `~/Documents/Archive-Offload/bundles/pilot-2026-04-20-ql`
- Verification log: `~/Documents/Archive-Offload/logs/pilot-2026-04-20-ql-verify.log`
- Checksum verification: `checked_files=6`, `mismatches=0`
- Retrieval test: `pass` (sample restore hash matched)
- Source handling: Local source retained (no deletion)

## Next Actions

1. Choose `offload_destination` (external drive path or cloud mirror path).
2. Copy bundle to destination without deleting source.
3. Recompute hashes at destination and compare with manifest.
4. Run retrieval test on one sample file.
5. Update `docs/storage-offload-ledger.csv` (`moved_at`, destination, result notes).
6. Only after successful verification, decide whether to remove local source copy.

## Next Queued Bundle

1. Bundle: `Archiavellian-Archive/backups/phone_cleanup_backups`
2. Bundle bytes: `5228002` (`14` files)
3. SHA256 manifest: `docs/manifests/next-offload-2026-04-20-phone-cleanup-backups-sha256.txt`
4. Planned destination: `~/Documents/Archive-Offload/bundles/queue-2026-04-20-phone-cleanup-backups`
5. Execution mode: copy + verify + retrieval test, then ledger update (no source deletion in same step).

## Queue Execution Result

- Bundle: `Archiavellian-Archive/backups/phone_cleanup_backups`
- Destination: `~/Documents/Archive-Offload/bundles/queue-2026-04-20-phone-cleanup-backups`
- Verification log: `~/Documents/Archive-Offload/logs/queue-2026-04-20-phone-cleanup-backups-verify.log`
- Checksum verification: `checked_files=14`, `mismatches=0`
- Retrieval test: `pass` (sample restore hash matched)
- Source handling: Local source retained (no deletion)
