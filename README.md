# Project Manager

This repository is the portfolio control plane for the projects inside this workspace.

It keeps a workspace-level view of the portfolio, preserves each child project's independent git history, and provides the intake and onboarding path for new projects.

If Git, CI, Conda, or environment wiring keeps fighting you, skim **`docs/operator-friction-log.md`** first—it lists recurring gotchas and workarounds.

## What This Repo Does

- Tracks child repositories as independent projects
- Maintains a portfolio manifest in `config/repos.json`
- Generates a portfolio dashboard in `STATUS.md`
- Standardizes intake and onboarding for new projects
- Defines the boundary between project-owned docs and PM-owned portfolio responsibilities

## Core Workflow

1. Add or update project metadata in `config/repos.json`.
2. Refresh the dashboard with `python3 scripts/portfolio_status.py`.
3. Use `docs/new-project-intake-template.md` for intake.
4. Use `docs/new-project-onboarding-checklist.md` to operationalize new projects.
5. Bootstrap new projects with `python3 scripts/bootstrap_project.py --name "Project Name"`.
6. Onboard an already-existing project folder with `python3 scripts/onboard_existing_project.py --name "Project Name" --path "Existing Folder"`.
7. Add `--initial-commit --commit-all-files` when the onboarding run should also create the baseline repo commit for the full existing folder contents.
8. Use `--skip-portfolio-plan` when a new repo should stay standalone instead of being managed by the Project Manager portfolio plan.
9. Use `python3 scripts/intake_wizard.py` for a lighter guided intake flow.
10. Inspect child repo pointer drift with `python3 scripts/sync_child_repo_pointers.py`.
11. Use `python3 scripts/scaffold_client_engagement_pack.py --target "path/to/repo" --project-name "Project Name"` when a managed child repo needs the reusable client-facing engagement doc pack.
12. Use `python3 scripts/scaffold_investor_book.py --target "path/to/repo" --project-name "Project Name"` when a project needs a repeatable investor-book template and section-coverage checklist.
13. Use `python3 scripts/scaffold_production_delivery.py --target "path/to/repo"` to add standardized backlog/sprint/test/PR-readiness docs.
14. Before any PR, run `python3 scripts/check_production_readiness.py --target "path/to/repo"` to enforce agile planning + testing evidence gates.
15. To run production readiness and downstream governance together on one repo: `python3 scripts/run_repo_readiness_gates.py --target "path/to/repo"` (internal portfolio gates; not consulting SKUs).
16. Use `python3 scripts/scaffold_gtm_pack.py --target "path/to/repo"` when a project needs repeatable GTM hypothesis and pilot outreach docs.
17. Use `python3 scripts/rollout_pm_backbone.py` to roll out the latest production/GTM/investor scaffolds across managed projects.
18. Commit the portfolio updates from this top-level repo.

## Managed Repositories

- `Aneumind and TC Structure`
- `Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System` (tracked gitlink; private GitHub **CIMPT**; parent portfolio is this **Project Manager** repo — see `config/repos.json`)
- `App Builder/App Builder`
- `App Builder/Teach/home-learning-playbook`
- `App Builder/Teach/zahmeir-learning-system`
- `GitHub/mjsds_dashboard`
- `MJS Financial Dash`
- `MJS Financial Dash backup 20260310_153810`
- `Momentum-OS`
- `Archiavellian-Archive`
- `bg-legal` (Case Files program — see `docs/bg-legal-folder-migration.md`)
- `Producer`
- `Resume Builder`
- `TuneFab`
- `provider-access-hub`
- `Wayne Strain`
- `mjsds-website`

## Public GitHub review (sanitized)

- Treat the directory `private-only/20260420-session-artifacts` as **local-only** (it is under `private-only/`, which git must never track). Do not sync legal work product, archive intake, DAM material, or iCloud-derived indexes from there (or equivalents) to GitHub or any other public-facing path. Keep those artifacts only in restricted private storage when they must be retained.
- For GitHub review and pull requests that touch this portfolio control plane, use the sanitized branch **`codex/review-and-pr-20260420`** only (safe onboarding and portfolio metadata changes). Do not fold unsanitized session or privacy-classified material into that branch.

## Notes

- Private host repository **CIMPT** is the same engagement as the child folder `Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System/` (short remote name, full local path). **Keep `CIMPT` Private on GitHub** (invite-only); it must not be made public from the portfolio control plane.
- `2024 Taxes` is not yet tracked as a child gitlink because that repo has no first commit yet.
- Child repos remain the source of truth for their own code and history.
- This repo is the source of truth for portfolio visibility, intake, and onboarding.
- **`bg-legal/`** is the single git working copy for the Case Files program (`melissastock/bg-legal`): operating docs, routing, timeline evidence, reviewed derivatives. The Google Drive folder **Case Files** is intake-only; raw evidence stays in `Archiavellian-Archive` per `docs/case-files-track-onboarding-2026-04-22.md`. Migration from an old `Case Files/` folder: `docs/bg-legal-folder-migration.md`.
- `MJS Financial Dash` is the canonical finance repository. `MJS Financial Dash backup 20260310_153810` is retained only as a deprecated archive-only snapshot until final removal is explicitly approved.
- `provider-access-hub` is now the active PAH codebase; `TuneFab` is being transitioned toward archive status.
- Operator friction (Git, CI, Supabase keys, ports, CLI): `docs/operator-friction-log.md`
- Portfolio execution queue (rules + where live scores live): `docs/portfolio-execution-queue.md`
- Boundary policy: `docs/project-boundary-policy.md`
- Investor-book repeatable process: `docs/investor-book-repeatable-workflow.md`
- Agile production process standard: `docs/agile-production-process.md`
- GTM repeatable process: `docs/gtm-repeatable-workflow.md`
- Consulting operator workflow (offers, stage gates, payments, web/portal): `docs/master-consulting-operator-workflow.md`
- Pilot both consulting SKUs on bg-legal (sequencing + repo mapping): `docs/bg-legal-consulting-pilot-playbook.md`
