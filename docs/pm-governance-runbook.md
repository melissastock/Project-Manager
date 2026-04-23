# PM Governance Runbook

## Daily Sweep (MVP fast profile)

Run from `Project Manager` root:

```bash
PROFILE=fast ./scripts/run_governance_profile.sh
```

## Start-of-Day Reliability Gate (P0)

Run before product execution:

```bash
python3 scripts/run_start_of_day_gate.py
```

This enforces:

- remote audit pass via `scripts/sync_repo_remotes.py` (no missing bindings or remote-key drift),
- fresh standup artifact refresh for the current session,
- drift classification against `config/drift-baseline.json` for `provider-access-hub`, `Momentum-OS`, and `bg-legal`.

If this gate fails, do not continue with multi-repo commit/push until drift is classified and baseline-reviewed.

This runs only lightweight checks by default. Use env flags to force specific checks for a small chunk:

```bash
PROFILE=fast RUN_SCOPE_CHECK=1 RUN_ARCH_SCALE_FIT_CHECK=1 ./scripts/run_governance_profile.sh
```

## Profiles

- `fast` (default): PR/push-safe selective checks only.
- `pm-portal`: portal/mobile policy and disclosure alignment checks.
- `release`: pre-send/pre-release checks for a target scope.
- `full`: all governance checks (best for nightly/manual full audits).

Examples:

```bash
PROFILE=pm-portal ./scripts/run_governance_profile.sh
PROFILE=release TARGET_REPO="pm-portal" ./scripts/run_governance_profile.sh
PROFILE=full ./scripts/run_governance_profile.sh
```

Each profile run writes a transparency summary artifact:

- `docs/session-artifacts/governance/last-governance-run.json`
- `docs/session-artifacts/governance/last-governance-run.md`

These files show which checks were enabled/skipped and why (profile + trigger reason).

## Full Legacy Sweep (compatibility)

```bash
./scripts/run_pm_governance_sweep.sh
```

If any command fails:

1. Log issue in session handoff under `Issues / Challenges`.
2. Record whether it is blocker or accepted exception.
3. Assign owner and due date.

## Weekly Control Review

Run `PROFILE=full ./scripts/run_governance_profile.sh` at least weekly (or use nightly CI schedule) before high-risk release windows.

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

