# Review Gates

Use these gates for any Project Manager work before a PR is considered ready.

These are system requirements, not optional nice-to-haves.

## Gate 1 — Code Review

Every code-bearing change must receive a review pass focused on:
- correctness
- regressions
- edge cases
- missing tests
- workflow breakage

Minimum standard:
- findings are written down
- blockers are fixed or explicitly accepted
- non-blocking risks are called out in PR notes or handoff

## Gate 2 — QC / Validation

Every change must have a validation pass appropriate to the change type.

Examples:
- scripts: syntax check plus at least one execution path
- docs with process impact: workflow walkthrough against current repo state
- generated files: regenerate from source and compare expected output

Minimum standard:
- what was tested
- what passed
- what failed
- what was not tested

## Gate 3 — Governance / Legal / Privacy Compliance

Every PR must be checked for publication safety and release-path appropriateness.

Questions:
- Is the repo visibility appropriate for this material?
- Does any file include secrets, tokens, credentials, or direct identifiers?
- Does any file include governance, archive, legal, privacy, or portfolio-control material that should remain private?
- Is the content safe to be searchable, indexable, quotable, and readable out of context?

Classification:
- `public-safe`
- `private-only`
- `needs rewrite before publish`

## Required Artifacts

Before greenlighting a PR:
- review findings or explicit no-findings note
- QC notes
- publication review file if visibility or sensitivity is relevant

Recommended commands:
- `python3 scripts/review_gate.py`
- repo-specific tests or script checks

## Greenlight Rule

Do not greenlight a PR unless:
- code review is complete
- QC is complete
- compliance review is complete
- blockers are fixed or explicitly accepted
