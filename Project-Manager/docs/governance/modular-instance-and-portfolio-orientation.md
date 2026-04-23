# Modular Instances and Portfolio Orientation

## Purpose

Define how projects are instantiated as reusable modules and how portfolios are managed in either horizontal or vertical orientation.

---

## Modular Instance Model

A project may use one or more modular instances:

- `governance-core`
- `delivery-core`
- `commercialization-core`
- `operations-core`
- `archive-core`

Rules:
- modular instance selection must be documented in intake
- selected modules must map to required artifacts and gates
- modules may be combined, but mandatory controls cannot be omitted

---

## Portfolio Orientation Modes

### Horizontal Portfolio

Organized by shared capabilities (e.g., delivery, governance, commercialization) across many projects.

Best when:
- standardization and shared execution patterns are prioritized
- multiple projects depend on common operating functions

### Vertical Portfolio

Organized by end-to-end value stream for a specific domain or project family.

Best when:
- domain specialization and ownership continuity are prioritized
- a single product/program must move from intake to launch with minimal handoff

---

## Orientation Governance Rules

- Every project must declare a portfolio orientation (`horizontal` or `vertical`).
- Command center should support filtering and reporting by orientation.
- Orientation can change only with explicit review and documented rationale.

