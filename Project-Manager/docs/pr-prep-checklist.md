# PR Preparation Checklist

Use this before opening any pull request.

System rule:
- no PR is greenlit until code review, QC, and compliance checks are complete
- use `docs/REVIEW_GATES.md` as the controlling standard
- run `python3 scripts/review_gate.py` before final PR packaging

## 1. Scope Check
- What is this PR doing?
- What is explicitly NOT included?

## 2. Repo Integrity
- [ ] correct branch
- [ ] no unintended file changes
- [ ] no stray local files

## 3. Functional Check
- [ ] scripts run without errors
- [ ] commands behave as expected
- [ ] no obvious broken flows

## 4. Code Review Check
- [ ] review findings recorded or explicit no-findings note written
- [ ] blockers fixed or explicitly accepted
- [ ] regression risk and missing tests reviewed

## 5. Portfolio Alignment (Project Manager)
- [ ] config/repos.json updated (if needed)
- [ ] STATUS.md regenerated (if needed)
- [ ] README.md updated (if needed)

## 6. Dependency Check
- [ ] dependencies documented
- [ ] no missing upstream assumptions
- [ ] no circular or unclear dependencies introduced

## 7. Documentation Check
- [ ] new docs included
- [ ] docs reflect current system reality
- [ ] no outdated references

## 8. Governance / Privacy Check
- [ ] repo visibility is appropriate for the material being published
- [ ] each changed file is classified: `public-safe`, `private-only`, or `needs rewrite before publish`
- [ ] no governance, archive, DAM, legal, or privacy-sensitive material is being published unintentionally
- [ ] anything marked `private-only` is held back until the repo visibility and release path are appropriate
- [ ] GitHub-facing PRs for this control plane are based on **`codex/review-and-pr-20260420`** (sanitized) only; legal, archive intake, and iCloud-index materials stay out of git remotes (use ignored `private-only/` such as `private-only/20260420-session-artifacts` or other restricted private storage, not public branches)

Definition:
- `public-safe` means safe to be searchable, indexable, quotable, and readable out of context on the public internet

## 9. Evidence Discipline
- [ ] factual statements are verifiable
- [ ] interpretations labeled
- [ ] opinions labeled

## 10. Testing Notes
- what was tested:
- what passed:
- what failed:
- what not tested:

## 11. PR Write-Up

### Title
Clear and specific

### Summary
- what changed
- why it changed
- system impact

### Notes
- dependencies
- known gaps
- follow-up work

## 12. Final Check
- [ ] another developer could review this without confusion
- [ ] nothing critical is undocumented

## Done
If all boxes are checked, open PR
