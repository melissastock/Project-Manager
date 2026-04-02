# Portfolio Status

Generated: 2026-04-01 21:20:27 MDT

## Summary

- Managed repositories: 15
- Clean repositories: 8
- Repositories with local changes: 7
- Repositories in onboarding: 2

## Repository Snapshot

| Project | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Aneumind and TC Structure | active | codex/taylor-shell-claim-scenario | unstaged:3, untracked:44 | no-upstream | c1a02f2 | Add onboarding pack |
| App Builder | active | codex/project-manager-scaffold | clean | ahead:2 behind:0 | 7f5a60e | Add project onboarding pack |
| MJS Financial Dash | active | codex/finance-snapshot-onboarding | unstaged:23, untracked:44 | ahead:0 behind:0 | 326be3b | Apply archival metadata and finish outputs routing |
| MJS Financial Dash Backup | archive | main | unstaged:20, untracked:33 | ahead:0 behind:0 | 1d88e08 | Financial Dashboard 2022-26 |
| MJSDS Dashboard | active | main | clean | ahead:1 behind:0 | f5d1e51 | Add project onboarding pack |
| MJSDS Website | onboarding | main | clean | no-upstream | 138378e | Keep website README project-scoped |
| Momentum-OS | active | main | unstaged:5, untracked:6 | ahead:3 behind:0 | d334cf0 | Add project onboarding pack |
| Producer | active | main | unstaged:7, untracked:10 | ahead:3 behind:0 | facedb9 | Add project onboarding pack |
| Producer Archive | archive | main | clean | ahead:1 behind:0 | b084cdb | Remove sensitive archive inventories from tracking |
| provider-access-hub | active | main | clean | ahead:1 behind:0 | ac76a94 | Add project onboarding pack |
| Resume Builder | onboarding | main | clean | no-upstream | 1e0b7cd | Add project onboarding pack |
| Teach - Home Learning Playbook | active | main | unstaged:6, untracked:5 | ahead:1 behind:0 | 13dd225 | Add project onboarding pack |
| Teach - Zahmeir Learning System | active | feat/lesson-1-direct-launch | unstaged:19, untracked:2 | ahead:1 behind:0 | a8bce64 | Add project onboarding pack |
| TuneFab | archive | main | clean | no-upstream | 0ccf7a6 | Convert TuneFab into archive workspace |
| Wayne Strain | active | codex/milestone-1-jurisdiction-research | clean | ahead:1 behind:0 | ea8ebaf | Add onboarding milestone docs |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
