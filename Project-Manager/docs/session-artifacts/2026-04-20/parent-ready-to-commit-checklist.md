# Parent Ready-To-Commit Checklist

Generated: 2026-04-20 MDT

## Objective

Prepare clean, intentional parent-repo commit boundaries without committing yet.

## Guardrails

- Do **not** use `git add .` from parent.
- Stage by explicit path lists only.
- Exclude `Divorce/` file-level changes from parent commits unless explicitly reviewed.
- Keep legal/financial sensitive content in child repos; parent should primarily carry control-plane metadata and gitlink pointers.

---

## Commit Group A: PM Control-Plane Architecture

### Stage exactly these paths

- `config/repos.json`
- `scripts/portfolio_status.py`
- `STATUS.md`
- `docs/new-project-intake-template.md`
- `docs/portfolio-operating-system-architecture-map-plan.md`
- `docs/portfolio-crossref-recommendations.md`
- `docs/session-artifacts/2026-04-20/recovery-core-operational-snapshot.md`
- `docs/session-artifacts/2026-04-20/parent-ready-to-commit-checklist.md`

### Optional staging command

```bash
git add \
  "config/repos.json" \
  "scripts/portfolio_status.py" \
  "STATUS.md" \
  "docs/new-project-intake-template.md" \
  "docs/portfolio-operating-system-architecture-map-plan.md" \
  "docs/portfolio-crossref-recommendations.md" \
  "docs/session-artifacts/2026-04-20/recovery-core-operational-snapshot.md" \
  "docs/session-artifacts/2026-04-20/parent-ready-to-commit-checklist.md"
```

---

## Commit Group B: Child Repo Pointer Updates

### Stage only repo pointer paths (no parent docs)

- `Aneumind and TC Structure`
- `App Builder/Teach/home-learning-playbook`
- `App Builder/Teach/zahmeir-learning-system`
- `Archiavellian-Archive`
- `MJS Financial Dash`
- `MJS Financial Dash backup 20260310_153810`
- `Momentum-OS`
- `Producer`

### Optional staging command

```bash
git add \
  "Aneumind and TC Structure" \
  "App Builder/Teach/home-learning-playbook" \
  "App Builder/Teach/zahmeir-learning-system" \
  "Archiavellian-Archive" \
  "MJS Financial Dash" \
  "MJS Financial Dash backup 20260310_153810" \
  "Momentum-OS" \
  "Producer"
```

---

## Explicit Exclusions (Current Pass)

Do not stage these in parent unless explicitly approved:

- `Divorce/draft_motion_for_contempt_and_enforcement_23DR30686.md`
- `Divorce/forensic_timeline_evidence_map_23DR30686.md`
- `Divorce/master_handoff_2026-04-11.md`
- `Divorce/petitioners_damages_ledger_23DR30686.md`

Also keep untracked repo placeholders out of this pass:

- `App Builder/App Builder`
- `GitHub/mjsds_dashboard`
- `Resume Builder`
- `TuneFab`
- `Wayne Strain`
- `mjsds-website`
- `provider-access-hub`

---

## Pre-Commit Validation (No Commit Yet)

Run after staging each commit group:

```bash
git status --short
git diff --staged --name-only
```

Review criteria:

1. Staged paths match the intended group exactly.
2. No `Divorce/` file-level changes appear in staged list.
3. No raw sensitive records are staged in parent.

