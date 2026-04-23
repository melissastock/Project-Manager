# Project Boundary Policy

## Purpose

This policy keeps project-side information inside each project repository and keeps portfolio management responsibilities inside `Project Manager`.

## Project Repositories Own

- product purpose and scope
- project architecture and implementation docs
- project-specific milestones and delivery notes
- project-specific runbooks and operating instructions
- local setup, build, and verification steps
- domain-specific risks, assumptions, and technical decisions

## Project Manager Owns

- intake and onboarding workflow
- portfolio classification and lane assignment
- active vs onboarding vs archive state
- staffing and role assignment across projects
- priority, sequencing, and capacity decisions
- cross-project dependency visibility
- portfolio dashboards and review cadence

## Practical Rule

If a document answers "how do we build or operate this specific project?" it belongs in the project repo.

If a document answers "how do we prioritize, supervise, classify, or sequence projects across the portfolio?" it belongs in `Project Manager`.

## Visibility And Publication Rule

- `Project Manager` is private canonical by default.
- Any public publication must be generated from an explicit allowlist export.
- Client-sensitive, legal/financial, family, regulated, or IP-protected artifacts are never eligible for public export.

## Git Isolation Rule

- Client isolation is repository-based (repo-per-client/project), not branch-based.
- Branches are lifecycle tools (`feature/*`, `release/*`, `hotfix/*`), not long-term client partitions.
- Backup/archive clones must use separate remotes from canonical production repositories.


## Shared Data Registry Boundary

- `os-registry` is the canonical source for cross-product shared metadata (skills, product models, portfolio metadata, and shared structured profile data).
- `Project Manager` remains the control plane for intake, sequencing, and governance decisions across repositories.
- During migration, `config/repos.json` is treated as a derived mirror from `os-registry`, not an independent source.
