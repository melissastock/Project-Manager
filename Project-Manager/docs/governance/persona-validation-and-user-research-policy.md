# Persona Validation and User Research Policy

## Purpose

Ensure persona choices are evidence-backed, not assumption-backed, before projects advance through execution and launch lifecycle states.

---

## Core Rule

Primary persona selection must be validated with documented user research evidence.

Persona metadata is incomplete unless all are present:
- persona validation status
- persona research evidence path
- persona research confidence
- last validation date

---

## Minimum Research Layer

Accepted evidence can include:
- user interviews
- stakeholder discovery sessions
- workflow observation notes
- behavioral/support telemetry summaries

At least one durable artifact must be stored in-repo and linked from intake.

---

## Lifecycle Enforcement

- `not-onboarded` / `governed`: persona validation may be pending.
- `execution-ready`: persona validation must be complete with at least medium confidence.
- `launch-ready` / `scaled`: persona validation must be complete with high confidence and current evidence.

---

## Enforcement

Use:
- `python3 scripts/validate_persona_research_layer.py --target "path/to/repo"`
- add `--fix` to scaffold missing persona-research metadata/artifact placeholders

