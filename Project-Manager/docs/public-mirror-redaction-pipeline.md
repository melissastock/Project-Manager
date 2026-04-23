# Public Mirror Redaction Pipeline

Version: `v1.0`
Last updated: `2026-04-21`

## Goal

Publish portfolio process transparency while guaranteeing no client-sensitive data, restricted legal/financial material, or protected IP is exposed.

## Source and Target

- Source: private canonical `Project Manager`
- Target: dedicated public mirror repo or public-only branch

## Export Model

1. Build candidate file set from allowlist in `docs/manifests/public-mirror-allowlist.txt`.
2. Exclude any path under session artifacts, raw inventories, legal/financial evidence, or private-only folders.
3. Validate the export payload using both:
   - content scans for secrets/high-risk markers
   - manifest policy checks (`public_sync_allowed=true` only)
4. Require manual approval before publish push.

## Required Guards

- Block publish if any managed repo referenced in export has:
  - `visibility_tier` != `public`
  - `public_sync_allowed` != `true`
  - restricted `data_class` or protected `ip_class`
- Block publish if content includes likely credentials (`token`, `secret`, API keys, OAuth artifacts).

## Suggested Workflow

1. `scripts/export_public_mirror.py` generates a temporary export directory.
2. `scripts/check_public_export.py` runs policy + secret checks.
3. Approved export commit is pushed to public mirror remote.

## Initial Allowlist Candidates

- `README.md`
- `docs/portfolio-operating-system-architecture-map-plan.md`
- `docs/pm-public-private-git-architecture.md`
- `docs/new-project-intake-template.md` (template only)
- `STATUS.md` (only after redaction-safe generation checks)

## Non-Negotiable Exclusions

- `docs/session-artifacts/**`
- `docs/session-handoffs/**`
- any client evidence or legal/financial source exports
- any file tagged or classified as restricted by manifest policy fields
