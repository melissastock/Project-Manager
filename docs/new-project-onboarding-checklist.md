# New Project Onboarding Checklist

## Create

- Confirm project name, purpose, and owner.
- Create the working directory in the portfolio workspace, or use `python3 scripts/intake_wizard.py` for a guided flow.
- Use `python3 scripts/bootstrap_project.py` when you want a fully flag-driven setup.
- Initialize the project repository on `main`.
- Create or connect the GitHub remote.

## Configure

- Add a project README.
- Add a project `.gitignore`.
- Capture intake details with `docs/new-project-intake-template.md`.
- Add the new project to `config/repos.json`, or let the bootstrap script do it with `--add-to-manifest`.

## Operationalize

- Define the first milestone and next actions.
- Clarify whether the project is active, onboarding, paused, or archive.
- Confirm how this project should be represented in the top-level dashboard.
- Refresh `STATUS.md` with `python3 scripts/portfolio_status.py`.

## Verify

- Confirm the child repo has at least one commit.
- Confirm the top-level Project Manager repo sees the child repo correctly.
- Use `python3 scripts/sync_child_repo_pointers.py` to inspect child repo commit drift.
- Commit the Project Manager updates.
- Push both the child repo and the Project Manager repo.
