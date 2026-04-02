# Project Manager

This repository is the portfolio control plane for the projects inside this workspace.

It keeps a workspace-level view of the portfolio, preserves each child project's independent git history, and provides the intake and onboarding path for new projects.

## What This Repo Does

- Tracks child repositories as independent projects
- Maintains a portfolio manifest in `config/repos.json`
- Generates a portfolio dashboard in `STATUS.md`
- Standardizes intake and onboarding for new projects

## Core Workflow

1. Add or update project metadata in `config/repos.json`.
2. Refresh the dashboard with `python3 scripts/portfolio_status.py`.
3. Use `docs/new-project-intake-template.md` for intake.
4. Use `docs/new-project-onboarding-checklist.md` to operationalize new projects.
5. Bootstrap new projects with `python3 scripts/bootstrap_project.py --name "Project Name" --add-to-manifest`.
6. Use `python3 scripts/intake_wizard.py` for a lighter guided intake flow.
7. Inspect child repo pointer drift with `python3 scripts/sync_child_repo_pointers.py`.
8. Commit the portfolio updates from this top-level repo.

## Managed Repositories

- `Aneumind and TC Structure`
- `App Builder/App Builder`
- `App Builder/Teach/home-learning-playbook`
- `App Builder/Teach/zahmeir-learning-system`
- `GitHub/mjsds_dashboard`
- `MJS Financial Dash`
- `MJS Financial Dash/Resume Builder`
- `MJS Financial Dash backup 20260310_153810`
- `Momentum-OS`
- `Producer`
- `Producer/archive`
- `TuneFab`
- `Wayne Strain`
- `mjsds-website`

## Notes

- `2024 Taxes` is not yet tracked as a child gitlink because that repo has no first commit yet.
- Child repos remain the source of truth for their own code and history.
- This repo is the source of truth for portfolio visibility, intake, and onboarding.
