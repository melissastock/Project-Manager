# Agile Production Delivery Process

## Purpose

Standardize a repeatable production process across managed projects so delivery quality
does not depend on individual style.

This process enforces:

- backlog grooming before sprint start
- sprint planning with explicit scope and owners
- testing evidence before PRs
- consistent PR readiness checks

## Delivery cadence (default)

- **Backlog grooming:** weekly
- **Sprint planning:** every 2 weeks
- **Daily sync:** 15 minutes during sprint
- **Sprint review:** end of sprint
- **Retro:** end of sprint

## Mandatory artifacts per active project

Store these in the child repo under `docs/delivery/`:

1. `backlog.md`
2. `sprint-plan.md`
3. `test-report.md`
4. `pr-readiness.md`

## Rules (generally accepted agile guardrails)

1. No sprint starts without groomed backlog items and acceptance criteria.
2. Only work in sprint scope unless a documented priority override is approved.
3. Every completed story has test evidence (automated and/or manual).
4. No PR should open until `pr-readiness.md` is complete and gate checks pass.
5. Definition of Done applies to all stories (code + tests + docs + risk notes).

## Definition of Ready (DoR)

A backlog item is Ready only if:

- problem statement is clear
- acceptance criteria are clear
- dependencies are identified
- test approach is identified
- estimated size is documented

## Definition of Done (DoD)

A story is Done only if:

- implementation is complete
- tests executed and captured in `test-report.md`
- regressions reviewed
- docs updated
- PR readiness checklist completed
- gate command returns success

## PR gate policy

Before opening a PR, run from Project Manager:

```bash
python3 scripts/check_production_readiness.py --target "path/to/child/repo"
```

Required pass criteria:

- required delivery docs exist
- sprint plan has in-progress sprint scope
- test report contains pass/fail/not-tested notes
- PR readiness checklist is completed
- if `docs/project-intake.md` marks `GTM workflow needed: yes`, GTM docs must exist
- if `docs/project-intake.md` marks `Investor-book workflow needed: yes`, investor docs must exist

## Rollout

For a new or existing project:

1. Scaffold delivery docs:
   ```bash
   python3 scripts/scaffold_production_delivery.py --target "path/to/child/repo"
   ```
2. Populate the docs for the current sprint.
3. Enforce gate in team workflow before PRs.

## Governance note

Project-specific implementation details stay in the child repo. This document defines only the portfolio-level delivery standard.
