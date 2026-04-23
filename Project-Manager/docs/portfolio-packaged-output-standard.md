# Portfolio Packaged Output Standard

## Purpose

Define the minimum release package each managed project must produce before a project
output can be considered managed, publishable, or client-deliverable.

## Required Files (child repo)

Store under `docs/delivery/`:

1. `release-package.md`
2. `release-notes.md`
3. `rollback-plan.md`
4. `output-acceptance.md`

## Required Release Package Fields

`release-package.md` must include:

- Package version
- Owner
- Audience
- Included artifacts
- Distribution channel

## Required Acceptance Fields

`output-acceptance.md` must include:

- Accepted by
- Acceptance date
- Accepted scope
- Residual risks

## Enforcement

Run:

```bash
python3 scripts/check_packaged_output.py --target "path/to/child/repo"
```

This gate is required before release packaging is marked complete.

## Portfolio-Level Gate

For full release readiness, run:

```bash
python3 scripts/check_portfolio_release_gate.py --target "path/to/child/repo" --decision-log "docs/session-artifacts/standup/DECISION_LOG-YYYYMMDD_HHMMSS.md"
```

The consolidated gate validates production readiness, packaging completeness, review
coverage, remote collision safety, and optional decision-log completion.
