# Classification to Governance Matrix

## Purpose

Define the minimum required governance, data handling rules, and operating constraints for each project classification.

This ensures:
- sensitive data is never mishandled
- compliance posture is consistent
- onboarding produces a safe, governed workspace
- projects scale without introducing risk

---

## Core Principle

Data classification determines governance requirements.

No project is considered “onboarded” until its governance requirements are met.

---

## Classification Matrix

### regulated-sensitive (HIPAA-aligned)

Required Governance Docs:
- working-agreement.md
- remote-collaboration.md
- privacy-data-boundaries.md (MANDATORY)

Rules:
- No PHI stored
- Only aggregate, anonymized, or hashed data
- Private repo only
- No public sync

---

### family-sensitive (COPPA-aware)

Required:
- working-agreement.md
- minor-privacy-boundaries.md

Rules:
- No identifiable child data
- Guardian approval required for sharing
- Use pseudonyms

---

### legal-financial-restricted

Required:
- working-agreement.md
- evidence-handling-policy.md

Rules:
- Private only
- No public sharing
- Treat as sensitive evidence

---

### internal-ops

Required:
- working-agreement.md

Rules:
- Internal only
- No accidental public exposure

---

### public-open

Required:
- publication-checklist.md
- redaction-policy.md

Rules:
- Allowlist publishing only
- Validate before release

---

### archive-sensitive

Required:
- archive-handling-policy.md

Rules:
- No new work
- No public exposure

---

## Cross-Cutting Operational Governance (When Applicable)

### customer-facing delivery

Required:
- customer-service-sla.md
- incident-escalation-policy.md
- support-handoff-runbook.md

Rules:
- Define support tiers with response and resolution targets
- Assign named support owner and backup
- Track and review SLA exceptions
- Publish escalation contacts
- Define staffing and training readiness triggers before launch

---

### project-type downstream governance

Required:
- project-type-downstream-governance-rules.md
- kpi-profile-matrix.md

Rules:
- Apply downstream controls based on assigned `project_type`
- `Producer`, `Archiavellian`, and `Archive` must each follow profile-specific review cadence
- Financial controls must align to selected financial reporting profile

---

## Enforcement

A project is NOT onboarded until:
- classification assigned
- governance docs exist
- repo visibility matches classification

Customer-facing projects are NOT operationally onboarded until SLA governance requirements are met.

Projects are NOT downstream-governed until `docs/governance/project-type-downstream-governance-rules.md` requirements are satisfied.

---

## Notes

HIPAA and COPPA references indicate data handling posture, not legal certification.
