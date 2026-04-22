# Governance Framework

## Purpose

Define the single operating logic for Project Manager governance so rules, execution, KPI, and commercialization are enforced as one system.

This is the source-of-truth map for how projects move from intake to scale.

---

## System Stack (Top to Bottom)

1. **Governance** - what is allowed
2. **Execution** - how work gets done
3. **Performance** - how success is measured
4. **Commercialization** - how value is realized

All lower layers are constrained by upper layers.

---

## Control Flow

1. **Classification assigned** (`docs/governance/classification-to-governance-matrix.md`)
2. **Required governance artifacts enforced** (classification + cross-cutting rules)
3. **Onboarding gates enforced** (`docs/new-project-onboarding-checklist.md`)
4. **Execution readiness enforced** (`check_production_readiness.py`, architecture-fit gates)
5. **KPI and financial profile enforced** (`kpi-profile-matrix.md`, downstream governance)
6. **Launch-proximal commercialization enforced** (`validate_launch_readiness.py`)

No project should be treated as fully active unless the required prior gate has passed.

---

## Enforcement Model

Governance is not documentation-only. It is validated by scripted gates:

- `validate_downstream_governance.py`
- `check_production_readiness.py`
- `validate_architecture_scale_fit.py`
- `validate_launch_readiness.py`
- `run_portfolio_readiness_checks.py`

`--fix` modes are remediation helpers, not bypasses. Final state must still validate PASS.

---

## Classification -> Behavior

Classification must trigger required behavior, not optional guidance.

Examples:
- `regulated-sensitive` -> privacy boundaries + private collaboration controls + no public sync
- `family-sensitive` -> minor-privacy boundaries
- `legal-financial-restricted` -> evidence-handling controls
- launch-proximal projects -> commercialization + marketing + operational SOP artifacts

If required artifacts are missing, project readiness status must not advance.

---

## Lifecycle State Model

Canonical lifecycle states are defined in:
- `docs/governance/project-lifecycle-states.md`

Lifecycle state should match gate status, not intent.

---

## Portfolio Law

A project is not "active-ready" unless:
- governance requirements are complete
- downstream profile and owners are complete
- required execution gates pass

A project is not "launch-ready" unless:
- launch-proximal commercialization/marketing/SOP gates pass
- Path 2 white-label configuration is set when applicable

