# Portfolio Status

Generated: 2026-04-20 21:19:04 MDT

## Summary

- Managed repositories: 16
- Clean repositories: 0
- Repositories with local changes: 16
- Repositories in onboarding: 2

## Repository Snapshot

| Project | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Aneumind and TC Structure | active | codex/taylor-shell-claim-scenario | unstaged:3, untracked:50 | no-upstream | c1a02f2 | Add onboarding pack |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | active | main | unstaged:7, untracked:21 | ahead:0 behind:0 | e202c32 | Add discovery workflow and domain model docs; parent Project Manager; GitHub CIMPT (private) |
| App Builder | active | codex/project-manager-scaffold | untracked:5 | ahead:3 behind:0 | 89b7045 | Update Resume Builder repository path |
| MJS Financial Dash | active | codex/finance-snapshot-onboarding | unstaged:23, untracked:55 | ahead:0 behind:0 | 034da28 | Merge backup-only outputs into canonical archive snapshot. |
| MJS Financial Dash Backup | archive | main | unstaged:20, untracked:34 | ahead:0 behind:3 | 1d88e08 | Financial Dashboard 2022-26 |
| MJSDS Dashboard | active | main | untracked:5 | ahead:0 behind:0 | 4133068 | Align dashboard scaffold with deprecated status |
| MJSDS Website | onboarding | main | untracked:5 | no-upstream | 138378e | Keep website README project-scoped |
| Momentum-OS | active | main | untracked:5 | ahead:0 behind:0 | cc1bff2 | Remove stale Momentum-OS snapshot files; GitHub momentum-os (private) |
| Archiavellian | active | codex/archiavellian-report-to-project-manager | untracked:6 | ahead:0 behind:0 | b6e90ed | Add Archiavellian narrative architecture batch; GitHub archiavellian (private) |
| Archiavellian-Archive | archive | main | untracked:335 | ahead:0 behind:0 | 55e146d | Clean archive index batch note formatting |
| provider-access-hub | active | main | untracked:5 | ahead:0 behind:0 | eded0c5 | Add client-facing delivery scaffold docs |
| Resume Builder | onboarding | main | untracked:5 | no-upstream | 6e950f5 | Update repo paths after extraction |
| Teach - Home Learning Playbook | active | main | staged:6, untracked:16 | ahead:0 behind:0 | 9d43225 | Add project onboarding pack |
| Teach - Zahmeir Learning System | active | feat/lesson-1-direct-launch | unstaged:19, untracked:7 | ahead:1 behind:0 | a8bce64 | Add project onboarding pack |
| TuneFab | archive | main | untracked:1 | no-upstream | 0ccf7a6 | Convert TuneFab into archive workspace |
| Wayne Strain | active | codex/milestone-1-jurisdiction-research | untracked:5 | ahead:1 behind:0 | ea8ebaf | Add onboarding milestone docs |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
