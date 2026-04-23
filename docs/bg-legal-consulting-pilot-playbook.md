# bg-legal — Pilot both consulting offerings (SKU A + SKU B)

This playbook pilots **both consulting SKUs** from `docs/master-consulting-operator-workflow.md` against the **bg-legal** engagement: first **Clarity Sprint (SKU A)**, then **Execution OS Build (SKU B)**. Follow the master doc for stage gates, payments, and anti-spin rules; this file only adds **repo mapping** and a **pilot checklist**.

---

## 1) Where “bg-legal” lives in this portfolio

| Concept | Detail |
| --- | --- |
| **Git remote** | `melissastock/bg-legal` (`config/repo-remotes.json`) |
| **Local folder name** | Prefer a clone at **`bg-legal/`** under the Project Manager workspace root (same pattern as `provider-access-hub`, `Momentum-OS`). |
| **`Case Files` alias** | `Case Files` is bound to the **same** remote as `bg-legal` for sync purposes. Your **working tree** may still be named `Case Files/` until you rename or re-clone; pick **one** canonical folder for engagement work and stay consistent. |
| **`config/repos.json`** | Today the managed entry is **`Case Files`** with path `Case Files`. For this pilot, treat **`bg-legal`** as the canonical repo path once it exists locally, or keep `Case Files` as the path but align the remote to `bg-legal` only — avoid two divergent folders for the same engagement. |

**Practical rule:** one git repo, one folder name on disk, one SOW. If the remote is `bg-legal`, cloning into `bg-legal/` keeps naming aligned with weekly ops scripts that use `--target bg-legal`.

---

## 2) Pilot shape (recommended)

Run **SKU A first**, then **SKU B** on the **same** engagement (not in parallel). SKU A’s roadmap becomes the backbone of SKU B’s phased scope.

| Phase | Consulting SKU | Master workflow stages | Exit (high level) |
| --- | --- | --- | --- |
| **Pilot 1** | **SKU A** — Clarity Sprint | 0 → 1 → 2 → 3 → 4 → 5 → 6 for the sprint only | Signed SOW, payment, deliverables + readout + acceptance, closed invoice |
| **Pilot 2** | **SKU B** — Execution OS Build | New SOW (or explicit phase-2 amendment), repeat gates for 90-day build | Milestone payments, handoff package, acceptance, closeout |

**SKU A deliverables** (map into bg-legal docs / readout package): workflow map; risk register; decision packet; 30-day roadmap; executive readout.

**SKU B deliverables** (install in bg-legal + operating rhythm): intake/evidence routing; dashboard/tracking baseline; reporting outputs; cadence/governance loop; handoff pack (consultant-operated; client not self-configuring per master doc).

---

## 3) Day-zero setup in the repo (after clone)

When `bg-legal/` exists and is the engagement repo:

1. **Intake** — Ensure `docs/project-intake.md` reflects legal/financial sensitivity, decision owner, and lanes (`recovery-core` / `execution-*` / `narrative-output` per master workflow §4 delivery).
2. **Engagement pack (optional)** — From Project Manager root:  
   `python3 scripts/scaffold_client_engagement_pack.py --target bg-legal --project-name "bg-legal" --project-focus "legal workflow orchestration and execution OS pilot"`  
   Adjust placeholders to match the SOW.
3. **Delivery scaffold (for PM agile gates)** — If you want this repo to pass internal readiness checks:  
   `python3 scripts/scaffold_delivery_docs.py --target bg-legal`  
   (This supports **portfolio** quality gates; it is not a substitute for consulting deliverables.)
4. **Pilot log** — Add `docs/engagement/pilot-decision-log.md` (or one file per sprint) capturing Go/No-Go, change orders, and weekly decisions so SKU B builds on evidence, not memory.

---

## 4) SKU A pilot checklist (Clarity Sprint)

- [ ] Fit call + scorecard documented (master §3 Stage 1)
- [ ] Scoped offer sent (Standard vs Fast-track)
- [ ] SOW signed; **100% upfront** received (SKU A payment rule)
- [ ] Kickoff: channels, decision owner, sensitivity classification, secure paths (Stage 3)
- [ ] Current-state map + risk register + decision packet + 30-day roadmap drafted (Stage 4–5)
- [ ] Executive readout held; **written acceptance** (Stage 5)
- [ ] Invoice/close per Stage 6; capture **sanitized** proof for website “Proof” page when allowed

---

## 5) SKU B pilot checklist (Execution OS Build)

- [ ] Separate SOW or amendment: scope, **50/30/20** milestones, 90-day phases, explicit link to SKU A roadmap
- [ ] Kickoff payment cleared before build work (stop rule)
- [ ] Intake/evidence routing documented and enforced in repo or adjacent controlled storage
- [ ] Dashboard/tracking baseline agreed (what is measured weekly)
- [ ] Reporting outputs + governance cadence (weekly update template from master doc)
- [ ] Handoff package delivered; acceptance; final payment; close memo

---

## 6) If you meant “run checks on bg-legal”

If the goal is only to run **portfolio** validators on the `bg-legal` folder (readiness + downstream governance), from Project Manager root after the repo exists:

```bash
python3 scripts/check_production_readiness.py --target bg-legal
python3 scripts/validate_downstream_governance.py --target bg-legal
```

That is **orthogonal** to selling and delivering consulting SKU A and SKU B; use the checklists above for the actual pilot.
