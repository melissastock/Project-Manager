# New Project Onboarding Checklist

Portfolio-wide gotchas (Git allowlists, CI on `main`, env files, Supabase, ports) live in **`docs/operator-friction-log.md`**—glance it when onboarding stalls for non-project reasons.
For recurring session workflow (Draft/Apply mode, commit sequencing, and push order), use **`docs/process/session-playbook.md`**.

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
- Apply routing and redaction decisions with `docs/data-routing-and-templatization-policy.md`.
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
- Run `python3 scripts/validate_downstream_governance.py --target "path/to/repo"` to enforce project-type downstream governance intake gates.
- Use `python3 scripts/validate_downstream_governance.py --target "path/to/repo" --fix` to auto-fill missing downstream governance intake fields when needed.
- Run `python3 scripts/validate_launch_readiness.py --target "path/to/repo"` to enforce launch-proximal commercialization, marketing, and SOP gates when applicable.
- Use `python3 scripts/validate_launch_readiness.py --target "path/to/repo" --fix` to scaffold missing launch artifacts and Path 2 brand mode intake metadata when applicable.
- Run `python3 scripts/validate_lifecycle_state.py --target "path/to/repo"` to enforce lifecycle state consistency with governance/execution/launch gates.
- Use `python3 scripts/validate_lifecycle_state.py --target "path/to/repo" --fix` to auto-correct lifecycle state when it exceeds gate-valid readiness.
- Run `python3 scripts/validate_persona_research_layer.py --target "path/to/repo"` to enforce persona/modular/orientation and user-research evidence quality.
- Use `python3 scripts/validate_persona_research_layer.py --target "path/to/repo" --fix` to scaffold missing persona-research metadata and evidence notes.
- Run `python3 scripts/validate_cognitive_profile_alignment.py --target "path/to/repo"` to enforce self-imposed cognitive profile workflow metadata and artifacts.
- Use `python3 scripts/validate_cognitive_profile_alignment.py --target "path/to/repo" --fix` to scaffold missing profile metadata and creator workflow artifacts.
- Create or update `docs/architecture-scale-fit.md` and run `python3 scripts/validate_architecture_scale_fit.py --target "path/to/repo"` for local validation before scaling work.
- Use `python3 scripts/validate_architecture_scale_fit.py` for global changed-repo validation across the portfolio.
- Commit the Project Manager updates.
- Push both the child repo and the Project Manager repo.

## Governance Requirements (MANDATORY)

- classification assigned
- compliance profile assigned
- governance docs created
- repo visibility verified
- lifecycle state assigned using `docs/governance/project-lifecycle-states.md`

### regulated-sensitive
- privacy boundaries doc exists
- private collaboration enforced

### family-sensitive
- minor privacy rules defined

### legal-financial
- evidence handling defined

### customer-facing projects
- customer service SLA documented
- escalation path documented
- support owner + backup assigned
- staffing trigger criteria defined
- CS training plan documented before launch

### KPI profile requirements
- project type explicitly assigned (`Producer`, `Archiavellian`, `Archive`, or other approved type)
- KPI profile assigned in `docs/governance/kpi-profile-matrix.md`
- KPI owner assigned
- reporting cadence defined
- financial KPIs selected based on project type

### persona and modular-instance requirements
- primary user persona assigned (`docs/governance/project-persona-framework.md`)
- modular instance type documented (`templates/portfolio-modules/modular-instance-template.md`)
- portfolio orientation declared (`horizontal` or `vertical`)
- persona validation and research layer documented (`docs/governance/persona-validation-and-user-research-policy.md`)
- persona research evidence linked and confidence recorded

### cognitive profile requirements
- creator cognitive profile assigned (`adhd`, `audhd`, `autistic`, or `neurotypical`)
- creator focus plan documented (`docs/process/creator-focus-plan.md`)
- creator closeout rhythm documented (`docs/process/creator-closeout-rhythm.md`)
- cognitive profile governance documented (`docs/governance/cognitive-profile-modules.md`)

### downstream governance requirements
- downstream governance profile mapped in `docs/governance/project-type-downstream-governance-rules.md`
- project-type escalation triggers defined
- review cadence checkpoint created based on project type
- downstream governance owner assigned

### launch-proximal requirements (when launch window is committed)
- commercialization plan documented (`templates/monetization/commercialization-plan-template.md`)
- marketing plan documented (`templates/gtm/marketing-plan-template.md`)
- operationalization SOP set documented (`templates/operations/operationalization-sop-template.md`)
- Path 2 white-label identity selected and confirmed in command center admin when applicable

Project is NOT onboarded until complete.
