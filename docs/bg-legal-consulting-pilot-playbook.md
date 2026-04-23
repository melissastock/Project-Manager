# bg-legal — Pilot both consulting offerings (SKU A + SKU B)

This playbook pilots **both consulting SKUs** from `docs/master-consulting-operator-workflow.md` against the **bg-legal** engagement: first **Clarity Sprint (SKU A)**, then **Execution OS Build (SKU B)**. Follow the master doc for stage gates, payments, and anti-spin rules; this file only adds **repo mapping** and a **pilot checklist**.

---

## 1) Where “bg-legal” lives in this portfolio

| Concept | Detail |
| --- | --- |
| **Git remote** | `melissastock/bg-legal` (`config/repo-remotes.json`) |
| **Local folder name** | **Only** **`bg-legal/`** under the Project Manager workspace root (portfolio manifest path in `config/repos.json`). |
| **Google Drive “Case Files”** | Intake source name only — **not** a second git working tree. Raw exports and bulk evidence stay in **`Archiavellian-Archive`** per `docs/case-files-track-onboarding-2026-04-22.md`. |
| **`config/repos.json`** | Managed entry is **`bg-legal`** with path **`bg-legal`**. If you still have an old **`Case Files/`** folder, migrate then remove it: `docs/bg-legal-folder-migration.md`. |

**Practical rule:** one git repo, one folder on disk (`bg-legal/`), one SOW. Remote sync scripts still accept the binding name **Case Files** → `bg-legal` in `config/repo-remotes.json` for `sync_repo_remotes.py`.

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

## 6) If you meant “run internal portfolio gates on bg-legal”

If the goal is only to run **portfolio** validators on the `bg-legal` folder (not consulting SKUs), from Project Manager root after the repo exists:

```bash
python3 scripts/run_repo_readiness_gates.py --target bg-legal
```

Equivalent individual commands: `check_production_readiness.py` and `validate_downstream_governance.py` with `--target` set to the absolute or `bg-legal` path.

That is **orthogonal** to selling and delivering consulting SKU A and SKU B; use the checklists above for the actual pilot.
