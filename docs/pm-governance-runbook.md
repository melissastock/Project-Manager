# PM Governance Runbook

## Daily Sweep

Run from `Project Manager` root:

```bash
./scripts/run_pm_governance_sweep.sh
```

Or stepwise:

```bash
python3 scripts/portfolio_status.py
python3 scripts/check_remote_collisions.py
python3 scripts/review_gate.py
```

If any command fails:

1. Log issue in session handoff under `Issues / Challenges`.
2. Record whether it is blocker or accepted exception.
3. Assign owner and due date.

## Weekly Control Review

1. Review `STATUS.md` for:
   - missing upstream repos
   - dirty/high-drift repos in core lanes
   - visibility/data/IP classification anomalies
2. Review sampled high-risk projects for intake drift.
3. Re-confirm archive/backup remote safety posture.
4. Revalidate publication boundary (public-safe outputs only).

## Pre-Send/Pre-Release

1. Complete [docs/pm-sending-checklist.md](pm-sending-checklist.md).
2. Run delivery/readiness checks for target repo.
3. Confirm review gates:
   - code review
   - QC/validation
   - governance/legal/privacy
4. Confirm recipient class and data class compatibility.
5. Record release decision and approver in handoff notes.

