# New Project Onboarding Checklist

Portfolio-wide gotchas (Git allowlists, CI on `main`, env files, Supabase, ports) live in **`docs/operator-friction-log.md`**—glance it when onboarding stalls for non-project reasons.

## Create

- Confirm project name, purpose, and owner.
- Create the working directory in the portfolio workspace, or use `python3 scripts/intake_wizard.py` for a guided flow.
- Use `python3 scripts/bootstrap_project.py` when you want a fully flag-driven setup.
- Use `python3 scripts/onboard_existing_project.py` when the folder already exists and needs to be registered, documented, and onboarded automatically.
- Add `--initial-commit --commit-all-files` when onboarding should also capture the folder's baseline contents in the child repo history.
- Decide whether the project should be managed by the Project Manager portfolio plan or stay standalone.
- Initialize the project repository on `main`.
- Create or connect the GitHub remote.

## Configure

- Add a project README.
- Add a project `.gitignore`.
- Capture intake details with `docs/new-project-intake-template.md`.
- Use `python3 scripts/scaffold_client_engagement_pack.py --target "path/to/repo" --project-name "Project Name"` when a managed client-facing repo needs the reusable engagement doc pack.
- Use `python3 scripts/scaffold_investor_book.py --target "path/to/repo" --project-name "Project Name"` when fundraising or investor-ready documentation is expected.
- Use `python3 scripts/scaffold_production_delivery.py --target "path/to/repo"` to install standardized agile production delivery artifacts.
- Use `python3 scripts/scaffold_gtm_pack.py --target "path/to/repo"` when commercialization, pilot, or partner outreach planning is in scope.
- Use `python3 scripts/rollout_pm_backbone.py` from Project Manager when you need to apply the latest PM backbone standards to all managed repos in one pass.
- By default the bootstrap flow adds the repo to the Project Manager plan.
- Use `--skip-portfolio-plan` when the repo should opt out and stay standalone.

## Operationalize

- Define the first milestone and next actions.
- Clarify whether the project is active, onboarding, paused, or archive.
- Confirm how this project should be represented in the top-level dashboard.
- Refresh `STATUS.md` with `python3 scripts/portfolio_status.py`.

## Verify

- Confirm the child repo has at least one commit.
- Confirm the top-level Project Manager repo sees the child repo correctly.
- Use `python3 scripts/sync_child_repo_pointers.py` to inspect child repo commit drift.
- Run `python3 scripts/check_production_readiness.py --target "path/to/repo"` before opening PRs to enforce backlog, sprint, and testing gates.
- Create or update `docs/architecture-scale-fit.md` and run `python3 scripts/validate_architecture_scale_fit.py` before scaling work.
- Commit the Project Manager updates.
- Push both the child repo and the Project Manager repo.
