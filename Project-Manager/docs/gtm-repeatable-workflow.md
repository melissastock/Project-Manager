# GTM Repeatable Workflow

## Purpose

Standardize how projects create and maintain GTM planning and pilot outreach materials.

## When to run

Run when any of the following is true:

- a project is entering pilot partner outreach
- commercialization assumptions need to be documented
- buyer, pricing, and channel hypotheses must be tested

## Steps

1. Scaffold GTM docs into the child repo:

   ```bash
   python3 scripts/scaffold_gtm_pack.py --target "path/to/repo"
   ```

2. Populate:
   - `docs/gtm-hypotheses-and-pilot-plan.md`
   - `docs/pilot-outreach-brief.md`

3. Define:
   - beachhead segment
   - buyer and user
   - pilot metrics and thresholds
   - pricing hypotheses

4. Link GTM assumptions to:
   - product scope
   - security/compliance posture
   - investor-book assumptions (if applicable)

5. Revisit monthly and after each pilot cycle.

## Guardrails

- Do not promise guaranteed outcomes.
- Keep compliance and privacy boundaries explicit.
- Keep pricing and conversion assumptions clearly labeled as hypotheses.

## Done criteria

- GTM hypothesis document exists and is current.
- Pilot outreach brief exists and is usable.
- Success metrics and thresholds are explicit.
- Owner and cadence are documented.
