# Governance Module Catalog

## Purpose

Define which governance controls are always-on core controls versus modular controls that can be enabled per project instance.

---

## Core (Always Enabled)

Core modules are mandatory for every managed repository:

- `core-readiness`
  - Runs baseline production readiness checks.
  - Validator: `scripts/check_production_readiness.py`
- `lifecycle-state`
  - Enforces state progression against active gates.
  - Validator: `scripts/validate_lifecycle_state.py`

---

## Optional Modules (Attach Per Instance)

- `downstream-governance`
  - Enforces project-type KPI/financial/downstream profile completeness.
  - Validator: `scripts/validate_downstream_governance.py`
- `persona-research`
  - Enforces persona assignment, modular/orientation linkage, and research evidence quality.
  - Validator: `scripts/validate_persona_research_layer.py`
- `launch-readiness`
  - Enforces commercialization, marketing, and operationalization artifacts when launch-proximal.
  - Validator: `scripts/validate_launch_readiness.py`

---

## Intake Activation Fields

Projects may activate modules in intake using:

- `enabled_modules` (array)
- `module_activation_source` (`classification` / `project_type` / `manual` / `mixed`)
- `module_states` (object keyed by module name with `pending` / `active` / `waived`)

If `enabled_modules` is missing, auto-rules infer modules from intake signals and repository metadata.

---

## Auto-Activation Rules

- `downstream-governance` is auto-enabled when `Project type` or `Downstream governance profile` is present.
- `persona-research` is auto-enabled when persona/orientation fields are present.
- `launch-readiness` is auto-enabled when any launch-proximal required flag is true.

---

## Waivers

Waivers are allowed only with explicit rationale in project governance artifacts. Waived modules must remain visible in reporting.

