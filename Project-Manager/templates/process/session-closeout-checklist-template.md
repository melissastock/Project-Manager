# Session Closeout Checklist

## Session Setup
- Mode selected: `Draft` or `Apply`
- Scope confirmed (repos in/out of scope)

## Validation
- Ran `python3 scripts/run_portfolio_readiness_checks.py` (Draft) or `--fix` (Apply)
- Reviewed failing gates and remediation output

## Commits
- Parent engine changes committed
- Child repo scaffold/implementation changes committed
- Parent pointer sync committed

## Push
- Child repos pushed
- Parent pointer sync pushed
- Remote refs confirmed

## Data Sensitivity Review
- Reviewed `docs/research/persona-validation-notes.md` files for sensitive content
- Confirmed evidence files are intentional for remote

## Final State
- Child repos clean
- Parent repo clean
- Session notes captured

