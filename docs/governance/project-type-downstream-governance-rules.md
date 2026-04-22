# Project Type Downstream Governance Rules

## Purpose

Define mandatory downstream governance controls that must be applied after intake based on `project_type`.

This ensures governance is not only documented at onboarding, but cascaded into operations, reporting, and review gates.

---

## Core Enforcement Rule

For every project, downstream governance is considered active only when:
- project type is assigned
- required governance artifacts exist
- required KPI/financial profiles are configured
- review cadence and owner assignments are active

---

## Project Type Rules

### Producer

Downstream requirements:
- enforce delivery cadence and milestone tracking
- enforce quality/rework KPI reporting
- enforce budget vs actual reporting when funded
- enforce weekly KPI review checkpoint

Required artifacts:
- working-agreement.md
- sprint or delivery plan artifact
- KPI profile assignment (`Producer`)

Escalation triggers:
- on-time delivery rate below target for 2 periods
- unresolved blocker aging beyond agreed threshold
- budget variance exceeds defined threshold

---

### Archiavellian

Downstream requirements:
- enforce dependency and portfolio risk review cadence
- enforce decision log hygiene and closure tracking
- enforce committed vs forecast spend reviews
- enforce architecture-fit and governance exception visibility

Required artifacts:
- working-agreement.md
- architecture-fit artifact
- KPI profile assignment (`Archiavellian`)

Escalation triggers:
- dependency risk index exceeds accepted band
- roadmap confidence declines across 2 reporting cycles
- governance exception backlog is unowned

---

### Archive

Downstream requirements:
- enforce no-new-work operating posture unless reactivation is approved
- enforce periodic integrity and retention checks
- enforce access logging and exposure prevention controls
- enforce archive cost tracking where applicable

Required artifacts:
- archive-handling-policy.md
- archive integrity checkpoint record
- KPI profile assignment (`Archive`)

Escalation triggers:
- integrity check failure
- unauthorized access attempt
- archive retention checkpoint missed

---

## Cross-Cutting Financial Rules

When financial reporting is enabled, downstream controls must include:
- source mapping (`bank`, `accounting`, `manual`)
- project allocation rule for shared costs
- variance threshold and escalation owner
- reviewer signoff for period close

---

## Review And Verification

- verify downstream governance status at onboarding completion
- verify monthly for active projects
- verify quarterly for archive projects
- enforce via `python3 scripts/validate_downstream_governance.py --target "path/to/repo"` before marking onboarding complete
- remediation shortcut: run `python3 scripts/validate_downstream_governance.py --target "path/to/repo" --fix` to auto-fill missing downstream intake fields, then rerun validation

Projects that fail downstream governance checks must be marked at-risk until remediated.

