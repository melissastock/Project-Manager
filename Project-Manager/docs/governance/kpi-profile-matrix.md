# KPI Profile Matrix By Project Type

## Purpose

Define required KPIs by project type so planning, reporting, and review stay relevant to each operating model.

This prevents one-size-fits-all dashboards and ensures `Producer`, `Archiavellian`, and `Archive` projects are governed with fit-for-purpose metrics.

---

## Core Rule

Every project must have:
- `project_type` assigned
- `kpi_profile` assigned
- KPI owner assigned
- reporting cadence defined

Projects are not considered operationally onboarded until required KPIs for the assigned profile are configured.

---

## KPI Profiles

### Producer

Use for production, delivery, and execution-heavy work.

Required KPIs:
- throughput (deliverables completed per period)
- on-time delivery rate
- cycle time from intake to shipped output
- quality pass rate / rework rate
- budget vs actual (if funded)

Optional:
- utilization rate
- dependency-blocked time

---

### Archiavellian

Use for strategy, architecture, systems design, and portfolio-level orchestration.

Required KPIs:
- decision velocity (major decisions closed per period)
- roadmap confidence score
- cross-project dependency risk index
- execution alignment score (actual vs planned)
- committed vs forecast spend

Optional:
- architecture-fit gate pass rate
- governance exception count

---

### Archive

Use for archived, maintenance-only, or hold-state projects.

Required KPIs:
- storage footprint trend
- retention/compliance checkpoint completion
- archive integrity check pass rate
- access request volume

Optional:
- reactivation request count
- archive cost vs budget ceiling

---

### Client-Delivery / Services

Required KPIs:
- budget vs actual
- burn rate
- open invoices / overdue AR
- delivery milestone adherence
- client satisfaction signal (if available)

---

### Internal-Ops / Platform

Required KPIs:
- budget vs actual
- committed vs forecast spend
- operational incident rate
- service reliability target attainment

---

## Financial KPI Governance

Financial KPIs are profile-dependent and must be configured per `project_type`.

Required controls:
- source system mapping defined (bank/accounting/manual)
- allocation rule defined for shared costs
- reviewer assigned for financial KPI signoff
- variance threshold and escalation trigger defined

---

## Review Cadence

- Weekly: active `Producer` and `Client-Delivery` projects
- Biweekly or monthly: `Archiavellian` and `Internal-Ops`
- Monthly or quarterly: `Archive`

Cadence exceptions must be documented in the working agreement.

