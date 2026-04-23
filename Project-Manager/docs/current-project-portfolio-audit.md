# Current Project Portfolio Audit

Date: 2026-04-01
Repo: Project Manager
Purpose: compare the current GitHub-visible project set and the active work discussed this week against the portfolio documents in this repo.

## Documents Reviewed

- `README.md`
- `config/repos.json`
- `STATUS.md`
- current GitHub repository list visible to this account

## Portfolio Tracking Rule

A project is considered fully accounted for only when it is represented in the places it should report into:

1. `config/repos.json` when it is a managed project or archive in the portfolio
2. `STATUS.md` when it is being tracked operationally by the portfolio scripts
3. `README.md` when it belongs in the managed-repository snapshot for human review
4. its own project repo for project-specific scope, setup, milestones, and delivery docs

## Current Project Audit

| Project | Current state | Accounted for in PM docs | Gap / note |
| --- | --- | --- | --- |
| Project Manager | active portfolio control plane | Partial | Repo describes itself, but it is not tracked as a portfolio item in `config/repos.json` or `STATUS.md` because it is the control plane. That is acceptable if kept intentional. |
| MJS Financial Dash | active | Yes | Already present in `README.md`, `config/repos.json`, and `STATUS.md`. |
| Resume Builder | active but still local-only / no upstream | Partial | Present in `README.md`, `config/repos.json`, and `STATUS.md`, but still marked onboarding with no upstream. After push to GitHub, update path/remotes and refresh status. |
| MJSDS Dashboard | active | Yes | Already represented in PM docs. |
| Momentum-OS | active | Yes | Already represented in PM docs. |
| provider-access-hub | active | Yes | Already represented in PM docs. |
| home-learning-playbook | active | Yes | Represented as `Teach - Home Learning Playbook`. |
| app-builder | active | Partial | PM docs refer to local path `App Builder/App Builder`. If the canonical remote is now `app-builder`, PM docs should be normalized so local path and remote naming do not drift. |
| archiavellian | active | No | Missing from `README.md`, `config/repos.json`, and `STATUS.md`. Should be added if it is now an active managed project rather than a standalone repo outside the portfolio. |
| Archiavellian-Archive | active archive repo | No | Missing from `README.md`, `config/repos.json`, and `STATUS.md`. Should be added if archive governance is now part of the portfolio. |
| 2024 Taxes | active local-only workstream | Partial | Called out in `README.md` notes as not yet tracked as a child gitlink because there is no first commit yet. Still needs formal project entry once initialized. |
| Aneumind and TC Structure | active | Yes | Already represented in PM docs. |
| Producer / Producer Archive | active + archive | Yes | Already represented in PM docs. |
| TuneFab | archive transition | Yes | Already represented in PM docs as archive. |
| Wayne Strain | active | Yes | Already represented in PM docs. |
| MJSDS Website | onboarding | Yes | Already represented in PM docs. |
| provider-access-hub replacement status for TuneFab | tracked | Yes | Boundary is documented, but future status refresh should confirm TuneFab archive completion. |
| football-pickem | standalone repo | No portfolio tracking | Not enough evidence that this should be in Project Manager. Leave out unless it is now part of the managed portfolio. |
| football-pickem-jim-s-rules | standalone repo | No portfolio tracking | Same as above. Leave out unless it is part of the managed portfolio. |
| financial_dash | likely earlier or duplicate repo | No portfolio tracking | Do not add automatically. Verify whether this is deprecated, duplicate, or intentionally separate from `MJS-Financial-Dash`. |
| wayne-strain remote naming | tracked under spaced local path | Partial | PM docs use `Wayne Strain` while GitHub repo is `wayne-strain`. Acceptable if local path differs, but should be documented explicitly. |

## Bottom Line

Not all current projects are fully accounted for in the Project Manager documentation.

### Clearly accounted for

- MJS Financial Dash
- MJSDS Dashboard
- Momentum-OS
- provider-access-hub
- Aneumind and TC Structure
- Producer
- Producer Archive
- TuneFab
- Wayne Strain
- MJSDS Website
- Teach - Home Learning Playbook
- Teach - Zahmeir Learning System

### Partially accounted for

- Resume Builder
- app-builder / App Builder naming
- 2024 Taxes
- Project Manager self-tracking boundary
- Wayne Strain local-path vs remote-name normalization

### Missing from PM tracking even though they look active now

- archiavellian
- Archiavellian-Archive

## What Should Be Updated Next

1. Add `archiavellian` to `config/repos.json` if it is now part of the managed portfolio.
2. Add `Archiavellian-Archive` to `config/repos.json` if archive governance belongs in Project Manager.
3. After Resume Builder is pushed, update its canonical path/remote and rerun `python3 scripts/portfolio_status.py`.
4. Normalize any mismatches between local folder names and remote repo names where that mismatch creates confusion.
5. Decide whether `Project Manager` should remain outside its own managed list by policy, or whether a self-entry should be documented in a special-case note.
6. Confirm whether `financial_dash` is deprecated, duplicate, or still active before adding it anywhere.

## Reporting Recommendation

Use this rule going forward:

- Active managed project: must appear in `config/repos.json` and the generated `STATUS.md`
- Archive project with portfolio relevance: must appear in `config/repos.json` and the generated `STATUS.md` with archive state
- Local-only project not yet pushed: must be called out explicitly in `README.md` notes and moved into `config/repos.json` once initialized
- Standalone repo outside the managed portfolio: do not add unless there is a deliberate decision that it reports into Project Manager
