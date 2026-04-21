# Git Operating Model Policy

Version: `v1.0`
Last updated: `2026-04-21`

## 1) Portfolio Model

- Client isolation is **repo-per-client/project**.
- `Project Manager` is the control plane, not a container for client evidence files.
- Child repos may be tracked as gitlinks in parent, but canonical work lives in child repos.

## 2) Branch Model

Allowed long-lived branches:

- `main` (or one canonical default branch)
- `release/*` when needed

Short-lived branches:

- `feature/*`
- `fix/*`
- `hotfix/*`

Disallowed pattern:

- Long-lived branch-per-client isolation inside a shared repo.

## 3) Remote Safety Model

- Canonical repos and backup/archive clones must not share the same production `origin`.
- Backup remotes must use dedicated endpoints (`-backup`, fork, or mirror).
- Force-push to canonical `main` is incident-only and must be logged in session handoff.

## 4) Security Baseline

- Branch protection/ruleset on default branch for canonical repos.
- Secret scanning and push protection where available.
- Pull-request review required for:
  - `config/repos.json`
  - `scripts/portfolio_status.py`
  - policy and architecture docs

## 5) PM Metadata Requirements

Every managed repo in `config/repos.json` must include:

- `lane`
- `priority_class`
- `visibility_tier`
- `data_class`
- `ip_class`
- `public_sync_allowed`

## 6) Daily PM Review Checks

1. `python3 scripts/portfolio_status.py`
2. Review repos missing upstream or branch protection.
3. Run `python3 scripts/check_remote_collisions.py` and remediate any duplicate `origin` remotes.
4. Confirm no restricted repos are marked for public sync.
