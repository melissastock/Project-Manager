# TuneFab Archive Transition Plan

## Current State

`TuneFab` is no longer the best active home for Provider Access Hub work.

What remains inside `TuneFab`:

- `provider-access-hub/`
  - legacy source copy of PAH
  - embedded Postgres runtime data under `.tmp/embedded-postgres`
  - local `.env`
- `Spotify/`
  - three MP3 files
- `app_summary_one_page.pdf`
- `app_summary_one_page.txt`
- `.codex/environments/environment.toml`
- `.DS_Store`

## Recommendation

Treat `TuneFab` as an archive repo, not an active software repo.

The new active software repo is:

- `/Users/melissastock/Desktop/Project Manager/provider-access-hub`

## Safe Transition Sequence

1. Verify the new standalone `provider-access-hub` repo is the working source of truth.
2. Add a remote for `provider-access-hub` and push it.
3. Optionally verify install/build workflows in the new repo.
4. Only after the new repo is established, clean `TuneFab`.

## TuneFab Cleanup Goal

Reduce `TuneFab` to one of these shapes:

### Preferred

Archive/media repo containing only:

- `Spotify/`
- `app_summary_one_page.pdf`
- `app_summary_one_page.txt`

### Acceptable Temporary State

Archive repo containing the media files plus the old `provider-access-hub/` copy until the new repo is fully backed up remotely.

## What To Remove From TuneFab Later

Once the standalone PAH repo is safely backed up:

- `provider-access-hub/`
  - entire legacy source copy
  - `.tmp/embedded-postgres`
  - `.env`
  - old scripts/docs/openapi/services/packages/prisma tree
- `.DS_Store`
- local-only `.codex/` files if they are not useful to keep

## Decision Rule

- If a file is part of the PAH application, it belongs in `provider-access-hub`.
- If a file is just media or summary material related to the old TuneFab workspace, it can stay in `TuneFab`.
- If a file is runtime state or machine-local config, it should not stay tracked anywhere.
