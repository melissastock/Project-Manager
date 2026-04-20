# Project Manager Publication Review — 2026-04-02

Purpose: classify the current `Project Manager` PR-scope files for publication risk before any push or PR packaging.

## Current Gate

- Repository visibility status observed during review: `public`
- Required target state before packaging governance or DAM-related material: `private`
- Current CLI constraint: `gh auth status` reports an invalid token, so repo visibility could not be changed from the terminal during this pass

## Publication Standard

`public-safe` means safe to be searchable, indexable, quotable, and readable out of context on the public internet.

Use:
- `public-safe`
- `private-only`
- `needs rewrite before publish`

## Current File Classification

| File | Classification | Reason |
| --- | --- | --- |
| `docs/SESSION_CLOSE.md` | public-safe | General session-closing protocol without sensitive project content |
| `docs/SESSION_OPEN.md` | public-safe | General session-opening protocol without sensitive project content |
| `docs/codex-close-checklist.md` | public-safe | Generic close checklist |
| `docs/pr-prep-checklist.md` | public-safe | Generic PR process doc; includes publication review gate |
| `docs/session-handoffs/README.md` | public-safe | Generic naming and workflow guidance |
| `scripts/create_session_handoff.py` | public-safe | Generic handoff generator |
| `scripts/session_handoff_common.py` | public-safe | Shared handoff file parsing and selection logic |
| `scripts/open_session.py` | public-safe | Generic session-open helper |
| `scripts/open_session_v2.py` | public-safe | Generic session-open helper once fixed and tested |
| `scripts/open_session_v3.py` | public-safe | Generic PM-aware session-open helper |
| `scripts/test_session_handoff_scripts.py` | public-safe | Regression coverage for generic session tooling behavior |
| `docs/archiavellian-portfolio-integration.md` | private-only | Portfolio governance decision about Archiavellian inclusion and tracking intent |
| `docs/archiavellian-dependency-map.md` | private-only | Internal dependency mapping and archive relationship detail |
| `docs/current-project-portfolio-audit.md` | private-only | Internal audit of active projects, gaps, and tracking decisions |
| `docs/document-update-status-2026-04-01.md` | private-only | Internal portfolio sync and PR-packaging note set |

## Packaging Rule

- Do not publish any file marked `private-only` while the repository is public.
- If the repository remains public, limit packaging to files classified `public-safe`.
- DAM and governance material should stay private by default unless explicitly reviewed for release.
