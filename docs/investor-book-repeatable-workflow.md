# Investor Book Repeatable Workflow

## Purpose

Standardize how child projects in Project Manager generate investor-book materials
without exposing private names, hard-coded ownership percentages, or unverified claims.

## When to run this workflow

Run when at least one is true:

- a project is planning a capital raise
- partner or pilot conversations require investor-style briefing documents
- strategic planning needs a structured finance and risk narrative

## Steps

1. Scaffold baseline docs into the child repo:

   ```bash
   python3 scripts/scaffold_investor_book.py --target "path/to/repo" --project-name "Project Name"
   ```

2. Populate `docs/investor-book-draft-assumptions.md` in the child repo.
   - Tag unknown values as `[ASSUMPTION]`.
   - Keep names and exact ownership percentages out of draft versions.

3. Complete `docs/investor-book-section-coverage.md` so each section maps to a project artifact.

4. Validate consistency against:
   - product docs
   - GTM plan
   - security/compliance posture
   - legal boundaries

5. Run legal and compliance review before external sharing.

## Guardrails

- Do not include PHI in investor materials.
- Do not include guaranteed outcomes claims.
- Do not finalize legal/term language without counsel.
- Keep draft metrics explicitly labeled assumptions until validated.

## Done criteria

- Template exists in child repo.
- Populated assumption draft exists.
- Section coverage checklist is complete.
- Open gaps are linked to concrete next documents or owners.
