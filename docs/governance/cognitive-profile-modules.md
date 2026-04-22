# Cognitive Profile Modules

## Purpose

Provide self-imposed execution support modes so creators can finish work consistently without lowering governance quality standards.

Completion requirements stay universal. Workflow behavior adapts per cognitive profile.

---

## Profiles

- `adhd`
- `audhd`
- `autistic`
- `neurotypical`

Profile defaults are defined in:
- `config/cognitive-profiles.json`

---

## Universal Rule

Cognitive profile modules change *how* work is executed, not *what* must be delivered.

All profiles must still satisfy:
- governance requirements
- lifecycle state gates
- closeout and readiness controls

---

## Required Intake Fields

- `Creator cognitive profile`
- `Creator workflow preferences`
- `Focus plan artifact path`
- `Closeout rhythm artifact path`

---

## Required Artifacts

- `docs/process/creator-focus-plan.md`
- `docs/process/creator-closeout-rhythm.md`

Templates:
- `templates/process/creator-focus-plan-template.md`
- `templates/process/creator-closeout-rhythm-template.md`

---

## Enforcement

Use:
- `python3 scripts/validate_cognitive_profile_alignment.py --target "path/to/repo"`
- add `--fix` to scaffold missing profile metadata and process artifacts

