# Portfolio execution queue

**If you are stuck on Git, CI, Conda, Supabase keys, `.env` saves, or ports—not the queue itself—open [`docs/operator-friction-log.md`](operator-friction-log.md) first.**

This document is the **canonical place for execution rules and batch structure**. The **live ordered queue** (scores, drift counts, project order) comes from the **latest PM standup artifacts**; refresh them before treating numbers as current.

## Authoritative timestamp

Use the **latest handoff addendum** under `docs/session-handoffs/` that names the current standup artifact set (time in the filename, e.g. `…143723` = 14:37). Older timestamped files are **historical comparison only**.

## Source of truth (replace `YYYYMMDD_HHMMSS` with your addendum’s stamp)

From the Project Manager workspace root:

- `docs/session-artifacts/standup/STANDUP_SUMMARY-YYYYMMDD_HHMMSS.md`
- `docs/session-artifacts/standup/READINESS_SCORECARD-YYYYMMDD_HHMMSS.md`
- `docs/session-artifacts/standup/NEXT_STEPS_PROPOSAL-YYYYMMDD_HHMMSS.md`
- `docs/session-artifacts/standup/DECISION_LOG-YYYYMMDD_HHMMSS.md`

Regenerate a full set when the portfolio has changed materially:

```bash
python3 scripts/run_pm_standup.py
```

Then update the handoff addendum to point at the **new** timestamp.

## Operating rules

- Security work first, then drift containment, then planning and packaging gaps, then readiness and release gates.
- Cap concurrent execution at **three** active projects unless the owner explicitly expands capacity.
- Every proposed action needs owner status: `approved`, `rejected`, or `defer`.
- Every change set needs a cascade scope tag: `all-repos`, `selected-lanes`, or `pm-portal-only` (see `docs/cascade-applicability-matrix.md`).
- Drift containment comes before backlog, sprint, or feature work.
- Do not bulk-commit untracked files from the parent repo; classify each item first.

## Batch shape (stable)

Use the scorecard and decision log to **assign projects** into these batches for the current cycle:

1. **Batch A — Security and evidence drift** (credentials, governed artifacts, archive-core drift).
2. **Batch B — Highest-risk product drift** (lowest readiness scores with active drift signals).
3. **Batch C — Remaining drift** (other drift-bearing repos).
4. **Batch D — Planning-only at-risk** (backlog/sprint coverage gaps without large untracked piles).

After each batch: re-run the standup script, compare the new scorecard to the prior one, and record the new authoritative timestamp in a handoff addendum.

## Final portfolio gate

When batches are complete: run `run_pm_standup.py`, verify scorecard movement matches expectations (drift down or documented holdbacks, no accidental public exposure of private material), and write a short addendum naming the new artifact timestamp.

## Batch close checklist

- Re-run `python3 scripts/run_pm_standup.py`.
- Confirm new standup artifacts are timestamped and reviewed.
- Mark the authoritative artifact set in a handoff addendum.
- Capture deferred actions with rationale and due date.

---

**Tooling and environment friction (again):** [`docs/operator-friction-log.md`](operator-friction-log.md)
