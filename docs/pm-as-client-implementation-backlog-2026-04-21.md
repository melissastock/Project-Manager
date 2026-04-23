# PM-as-Client Implementation Backlog

Date: `2026-04-21`  
Source: [docs/pm-as-client-full-review-2026-04-21.md](pm-as-client-full-review-2026-04-21.md)

This backlog tracks the 90-day program after the one-time review. Treat it like a client backlog: one owner, explicit acceptance criteria, and no silent scope creep.

---

## P0 — Security and enforcement

| ID | Item | Owner | Acceptance criteria |
| --- | --- | --- | --- |
| BL-PM-001 | Branch protection/rulesets on all canonical default branches | governance_steward | Every managed repo with a GitHub remote has protection documented and verified in GitHub settings |
| BL-PM-002 | Secret scanning + push protection verification (private repos) | automation_maintainer | Settings verified or documented exception with expiry |
| BL-PM-003 | Archive/backup remote topology audit (quarterly) | automation_maintainer | `check_remote_collisions.py` PASS; no backup→canonical shared `origin` |

---

## P1 — Automation and drift control

| ID | Item | Owner | Acceptance criteria |
| --- | --- | --- | --- |
| BL-PM-010 | Intake-vs-manifest drift validator script | automation_maintainer | Fails CI or local pre-commit when lane/classification/public_sync drift |
| BL-PM-011 | Single orchestrated governance sweep | automation_maintainer | `scripts/run_pm_governance_sweep.sh` runs status + collisions + optional review gate |
| BL-PM-012 | Packaging gate orchestrator (pre-send/pre-release) | release_packaging_owner | One command composes readiness + compliance checklist output |

---

## P2 — Packaging, sending, and transparency

| ID | Item | Owner | Acceptance criteria |
| --- | --- | --- | --- |
| BL-PM-020 | Outbound sending checklist adoption | compliance_reviewer | [docs/pm-sending-checklist.md](pm-sending-checklist.md) referenced in runbook and used on first real send |
| BL-PM-021 | Public mirror export automation (allowlist) | governance_steward | Export script + validation gate; no restricted-class files in output |

---

## P3 — Portfolio scale-out

| ID | Item | Owner | Acceptance criteria |
| --- | --- | --- | --- |
| BL-PM-030 | Expand sanity checks from sample to full manifest | lane_operator | All repos pass drift validator or have logged exception |
| BL-PM-031 | Quarterly PM-as-client control review | governance_steward | Session handoff + updated role register |
