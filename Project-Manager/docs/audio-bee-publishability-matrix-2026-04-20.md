# Audio Bee Publishability Matrix - 2026-04-20

Phase 2 refinement: taxonomy, metadata readiness, and publishing triage. No source files changed.

## Overview

- Total files reviewed: 238
- Confirmed story anchors from config: 4
- Files with duration metadata available: 193
- Zero-byte files detected: 2

## Refined Taxonomy

- `dated_session_capture`: 203 files (7.99 GiB)
- `named_story_anchor`: 18 files (1.09 GiB)
- `catalog_and_docs`: 7 files (0.00 GiB)
- `ops_system`: 6 files (0.00 GiB)
- `other_media`: 4 files (0.00 GiB)

## Publish Stage Triage

- `review_backlog`: 219 files
- `internal`: 7 files
- `exclude`: 6 files
- `priority_review`: 6 files

## Priority Review Queue (Anchors)

- `audio recordings/Swoll.mp3` | title: `Swoll` | duration: `2591.556` sec | rights: `needs_review`
- `audio recordings/Swoll^.wav` | title: `Swoll` | duration: `2591.556` sec | rights: `needs_review`
- `audio recordings/Slender Man.mp3` | title: `Slender Man` | duration: `1857.336` sec | rights: `needs_review`
- `audio recordings/Slender Man^.wav` | title: `Slender Man` | duration: `1857.336` sec | rights: `needs_review`
- `audio recordings/No Bird.mp3` | title: `No Bird` | duration: `313.472` sec | rights: `needs_review`
- `audio recordings/Variety Baby^.wav` | title: `Variety Baby` | duration: `` sec | rights: `needs_review`

## Risks and Gaps

- Zero-byte file: `audio recordings/Audio_01_02_2025_13_16_41.mp3`
- Zero-byte file: `audio recordings/Audio_10_11_2024_09_08_33.mp3`

## Recommended Next Actions

1. Fill manual metadata fields in `docs/audio-bee-inventory-refined-2026-04-20.csv` for `priority_review` first.
2. Confirm rights status for each priority file before any publish mark.
3. Approve naming convention and then apply rename in dry-run mode first.
4. Keep `ops_system` and `catalog_and_docs` out of publish pipeline.
