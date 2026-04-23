# Next steps proposal (20260421_184351)

Generated: 2026-04-21 18:43:51 MDT

Ordered for portfolio execution queue batches (see `docs/portfolio-execution-queue.md`).

## Batch A — Security and evidence drift

- Review untracked paths below for secrets, credentials, or governed legal/finance material before any `git add`.
- Do not bulk-commit from the parent repo without per-path classification.

## Batch B — Highest-risk product drift

- No dirty repos in top drift slice; re-scan after local changes.

## Batch C — Remaining drift

- Address smaller `untracked` piles repo-by-repo (readiness scaffold, dashboard, website, resume, Wayne Strain).

## Batch D — Planning-only / unborn

- **2024 Taxes** and **Bankruptcy**: initialize first commit or explicitly **defer** with owner rationale in the decision log.

## Verification

- Run `python3 scripts/portfolio_status.py` after changes.
- Re-run this script to mint a new timestamped artifact set.

