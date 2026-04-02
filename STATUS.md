# Portfolio Status

Generated: 2026-04-01 19:31:30 MDT

## Summary

- Managed repositories: 14
- Clean repositories: 6
- Repositories with local changes: 8
- Repositories in onboarding: 2

## Repository Snapshot

| Project | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Aneumind and TC Structure | active | codex/taylor-shell-claim-scenario | unstaged:3, untracked:44 | no-upstream | 6b6cc45 | Initial evidence baseline |
| App Builder | active | codex/project-manager-scaffold | clean | ahead:0 behind:0 | 62b060a | Start onboarding MJS Digital Strategy |
| Teach - Home Learning Playbook | active | main | unstaged:6, untracked:5 | ahead:0 behind:0 | 3ec80a1 | Initial commit |
| Teach - Zahmeir Learning System | active | feat/lesson-1-direct-launch | unstaged:19, untracked:2 | ahead:0 behind:0 | 403bde0 | fix: add explicit Expo app entrypoint |
| MJSDS Dashboard | active | main | clean | ahead:0 behind:0 | b11084b | Add dashboard app, index redirect, fix README |
| MJS Financial Dash | active | codex/finance-snapshot-onboarding | unstaged:23, untracked:44 | ahead:0 behind:0 | 326be3b | Apply archival metadata and finish outputs routing |
| Resume Builder | onboarding | main | clean | no-upstream | 17929bf | Initialize Resume Builder standalone repo |
| MJS Financial Dash Backup | archive | main | unstaged:20, untracked:33 | ahead:0 behind:0 | 1d88e08 | Financial Dashboard 2022-26 |
| Momentum-OS | active | main | unstaged:6, untracked:6 | ahead:1 behind:0 | 6afc5a3 | Provide summary and next steps |
| Producer | active | main | unstaged:7, untracked:10 | ahead:2 behind:0 | d787e75 | Refine Archiavellian story, format, and sales materials |
| Producer Archive | archive | main | clean | ahead:1 behind:0 | b084cdb | Remove sensitive archive inventories from tracking |
| TuneFab | active | main | unstaged:70, untracked:6 | no-upstream | 792378a | Fix pnpm workspace indentation |
| Wayne Strain | active | codex/milestone-1-jurisdiction-research | clean | ahead:0 behind:0 | 9693206 | Add Milestone 1 jurisdiction screening baseline |
| MJSDS Website | onboarding | main | clean | no-upstream | d834f2a | Initialize MJSDS website project workspace |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
