# Architecture And Scale Fit Gate

Use this gate to verify each project is built with the right stack, service model, data design, and hosting posture for its mandate.

## Why this gate exists

Readiness artifacts (backlog/sprint/tests) are necessary but not sufficient.  
This gate ensures implementation choices are technically appropriate before scale risks become expensive.

## Required project artifact

Each in-scope project should maintain:

- `docs/architecture-scale-fit.md`

Minimum required sections:

1. `## Mandate`
2. `## Tech Stack Decision`
3. `## Database Structure`
4. `## Service Model`
5. `## Hooks and Integrations`
6. `## Hosting Plan`
7. `## Scale Triggers`

## Review rubric

Score each section `0/1/2`:

- `0` = missing or vague
- `1` = present but weakly justified
- `2` = explicit and decision-ready

Suggested threshold:

- `>= 11/14` = pass
- `< 11/14` = needs revision

## What “good” looks like

### Mandate
- Clear problem and target users.
- Explicit non-goals.

### Tech Stack Decision
- Why chosen language/runtime/framework fits this mandate.
- Known tradeoffs and alternatives rejected.

### Database Structure
- Core entities/relationships and data classification.
- Retention, audit, and migration strategy.

### Service Model
- Monolith vs modular monolith vs microservices rationale.
- Conditions that trigger service decomposition.

### Hooks and Integrations
- Required external systems and event flows.
- Secrets/auth boundary and failure behavior.

### Hosting Plan
- Current deployment target and rationale.
- Environment separation (dev/staging/prod) and rollback approach.

### Scale Triggers
- Concrete thresholds (load, latency, storage, team ownership).
- Triggered actions when thresholds are exceeded.

## Scope

Apply this gate by cascade scope:

- `all-repos`: enforce for all active repos with commits.
- `selected-lanes`: enforce only listed lanes.
- `pm-portal-only`: enforce for portal app artifacts only.

## Automation

Validation script:

- `python3 scripts/validate_architecture_scale_fit.py`

Integrated via:

- `scripts/run_pm_governance_sweep.sh`
- `.github/workflows/pm-governance-checks.yml`

