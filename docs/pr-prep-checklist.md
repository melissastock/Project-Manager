# PR Preparation Checklist

Use this before opening any pull request.

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

## 4. Portfolio Alignment (Project Manager)
- [ ] config/repos.json updated (if needed)
- [ ] STATUS.md regenerated (if needed)
- [ ] README.md updated (if needed)

## 5. Dependency Check
- [ ] dependencies documented
- [ ] no missing upstream assumptions
- [ ] no circular or unclear dependencies introduced

## 6. Documentation Check
- [ ] new docs included
- [ ] docs reflect current system reality
- [ ] no outdated references

## 7. Evidence Discipline
- [ ] factual statements are verifiable
- [ ] interpretations labeled
- [ ] opinions labeled

## 8. Testing Notes
- what was tested:
- what passed:
- what failed:
- what not tested:

## 9. PR Write-Up

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

## 10. Final Check
- [ ] another developer could review this without confusion
- [ ] nothing critical is undocumented

## Done
If all boxes are checked, open PR
