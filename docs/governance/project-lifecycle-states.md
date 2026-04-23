# Project Lifecycle States

## Purpose

Define portfolio lifecycle states that tie governance, execution, KPI, and launch gates into one status model.

---

## States

- `not-onboarded`  
  Intake exists, but mandatory onboarding/governance gates are incomplete.

- `governed`  
  Classification and required governance artifacts are complete.

- `execution-ready`  
  Governance is complete and execution gates (production readiness + architecture fit + downstream governance) pass.

- `launch-ready`  
  Execution-ready plus launch-proximal gates pass where applicable (commercialization, marketing, SOP, Path 2 identity if required).

- `scaled`  
  Launch-ready and operating with sustained KPI/financial cadence and periodic governance compliance.

---

## Advancement Rules

- Projects may only move one state forward when required gates pass.
- Any failed mandatory gate should block advancement and may require status rollback.
- `archive` projects remain outside active advancement until formally reactivated.

