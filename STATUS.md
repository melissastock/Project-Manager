Wrote /Users/melissastock/Desktop/Project Manager/STATUS.md
ummary

- Managed repositories: 16
- Clean repositories: 8
- Repositories with local changes: 8
- Repositories in onboarding: 2

## Repository Snapshot

| Project | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Aneumind and TC Structure | active | codex/taylor-shell-claim-scenario | unstaged:3, untracked:45 | no-upstream | c1a02f2 | Add onboarding pack |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | active | main | unstaged:1, untracked:4 | ahead:0 behind:0 | e202c32 | Add discovery workflow and domain model docs; parent Project Manager; GitHub CIMPT (private) |
| App Builder | active | codex/project-manager-scaffold | clean | ahead:3 behind:0 | 89b7045 | Update Resume Builder repository path |
| MJS Financial Dash | active | codex/finance-snapshot-onboarding | unstaged:23, untracked:50 | ahead:0 behind:0 | 034da28 | Merge backup-only outputs into canonical archive snapshot. |
| MJS Financial Dash Backup | archive | main | unstaged:20, untracked:33 | ahead:0 behind:3 | 1d88e08 | Financial Dashboard 2022-26 |
| MJSDS Dashboard | active | main | clean | ahead:0 behind:0 | 4133068 | Align dashboard scaffold with deprecated status |
| MJSDS Website | onboarding | main | clean | no-upstream | 138378e | Keep website README project-scoped |
| Momentum-OS | active | main | clean | ahead:0 behind:0 | cc1bff2 | Remove stale Momentum-OS snapshot files; GitHub momentum-os (private) |
| Producer | active | main | unstaged:7, untracked:10 | ahead:0 behind:0 | facedb9 | Add project onboarding pack |
| Archiavellian-Archive | archive | main | untracked:334 | ahead:0 behind:0 | 55e146d | Clean archive index batch note formatting |
| provider-access-hub | active | main | clean | ahead:0 behind:0 | eded0c5 | Add client-facing delivery scaffold docs |
| Resume Builder | onboarding | main | clean | no-upstream | 6e950f5 | Update repo paths after extraction |
| Teach - Home Learning Playbook | active | main | staged:6, unstaged:1, untracked:11 | ahead:0 behind:0 | 9d43225 | Add project onboarding pack |
| Teach - Zahmeir Learning System | active | feat/lesson-1-direct-launch | unstaged:19, untracked:2 | ahead:1 behind:0 | a8bce64 | Add project onboarding pack |
| TuneFab | archive | main | clean | no-upstream | 0ccf7a6 | Convert TuneFab into archive workspace |
| Wayne Strain | active | codex/milestone-1-jurisdiction-research | clean | ahead:1 behind:0 | ea8ebaf | Add onboarding milestone docs |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
