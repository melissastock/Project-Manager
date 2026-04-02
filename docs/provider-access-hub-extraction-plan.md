# Provider Access Hub Extraction Plan

## Goal

Extract `TuneFab/provider-access-hub` into its own standalone repository without moving any files yet and without carrying over runtime noise.

## Current Assessment

- `TuneFab/provider-access-hub` is a full application repository-in-waiting:
  - product docs
  - OpenAPI specs
  - Prisma schemas and migrations
  - workspace config
  - services and shared packages
  - scripts and templates
- `TuneFab` itself appears to be a mixed container:
  - `provider-access-hub/` application code
  - `Spotify/` media files
  - summary artifacts
- The bulk of the current size is not real source:
  - `provider-access-hub/node_modules` is approximately `601M`
  - `provider-access-hub/.tmp` is approximately `118M`
  - `Spotify/` is approximately `23M`

## Recommendation

Create a new top-level repo at:

- `/Users/melissastock/Desktop/Project Manager/provider-access-hub`

Keep `TuneFab` separate as either:

- a smaller archive/media repo, or
- a repo to retire after extraction if it no longer has a real purpose

## What Should Move

Move these from `TuneFab/provider-access-hub` into the new repo:

- `.env.example`
- `.gitignore`
- `README.md`
- `contracts/`
- `docker-compose.yml`
- `docs/`
- `exports/`
- `infra/`
- `openapi/`
- `package.json`
- `packages/`
- `pnpm-lock.yaml`
- `pnpm-workspace.yaml`
- `prisma/`
- `scripts/`
- `services/`
- `templates/`
- `tsconfig.base.json`

## What Should Not Move

Do not carry these into the new repo history:

- `node_modules/`
- `.tmp/`
- `.env`
- `.DS_Store`

These should either be ignored, regenerated, or recreated locally later.

## Pre-Extraction Cleanup In TuneFab

Before any move:

1. Update `TuneFab/provider-access-hub/.gitignore` to include:
   - `.tmp/`
   - `node_modules/`
   - `.env`
   - `.DS_Store`
2. Stop any running embedded Postgres process that may still be touching `.tmp/`.
3. Decide whether the current real source edits in these files should be preserved as the starting point:
   - `provider-access-hub/README.md`
   - `provider-access-hub/docs/phase-2-test-evidence.md`
   - `provider-access-hub/openapi/pah-mvp.yaml`
   - `provider-access-hub/openapi/provider-master-profile.yaml`
   - `provider-access-hub/package.json`
   - `provider-access-hub/scripts/app-start.mjs`
   - `provider-access-hub/scripts/dev-embedded-postgres.mjs`
   - `provider-access-hub/docs/18-qa-test-plan.md`
   - `provider-access-hub/docs/ops/`
   - `provider-access-hub/prisma/services/credentialing/migrations/20260331154000_fix_multistate_unique_index/`
   - `provider-access-hub/scripts/phase2-smoke-stack.mjs`
   - `provider-access-hub/scripts/phase2-smoke.mjs`

## Safe Extraction Sequence

1. Create the new repo folder with the Project Manager bootstrap flow:
   - `python3 scripts/bootstrap_project.py --name "provider-access-hub" --path "provider-access-hub" --category software --role "provider platform codebase" --initial-commit`
2. Remove the bootstrap starter files from the new repo if they overlap with the real PAH files.
3. Copy only the approved source directories and files from `TuneFab/provider-access-hub` into the new repo.
4. Add the stronger ignore rules in the new repo before the first real import commit.
5. Review the imported tree to confirm that `.tmp`, `node_modules`, `.env`, and `.DS_Store` are absent.
6. Commit the imported PAH codebase in the new repo.
7. Decide what `TuneFab` becomes after extraction:
   - keep `Spotify/` and summary files only, or
   - archive/remove the repo from the active portfolio
8. Update `Project Manager`:
   - add the new `provider-access-hub` repo to the portfolio plan if desired
   - update `TuneFab` role/status if its purpose changes
   - refresh `STATUS.md`

## Lowest-Risk Variant

The safest first execution is copy-first, not move-first:

1. Create new repo.
2. Copy curated PAH source into it.
3. Commit and verify there.
4. Leave the old `TuneFab/provider-access-hub` folder untouched until the new repo is proven healthy.

This avoids accidental data loss and gives a clean rollback path.

## Decisions To Make Before Execution

- Should `provider-access-hub` be managed by the Project Manager plan? Recommended: yes.
- Should `TuneFab` remain an active repo after extraction? Recommended: probably no, unless the media/archive content still matters.
- Should the new repo preserve any historical connection to `TuneFab`? Recommended: no special history-preservation work for the first pass; do a clean curated import.
