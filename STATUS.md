# Portfolio Status

Generated: 2026-04-20 22:51:40 MDT

## Summary

- Managed repositories: 19
- Clean repositories: 5
- Repositories with local changes: 12
- Repositories in onboarding: 2

## Repository Snapshot

| Project | Lane | Priority | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024 Taxes | recovery-core | core | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Aneumind and TC Structure | business-structure | core | active | codex/taylor-shell-claim-scenario | clean | no-upstream | c1a02f2 | Add onboarding pack |
| App Builder | platform-product | adjacent | active | codex/project-manager-scaffold | untracked:5 | ahead:3 behind:0 | 89b7045 | Update Resume Builder repository path |
| Archiavellian | archive-incubator | peripheral | active | codex/archiavellian-report-to-project-manager | untracked:6 | ahead:0 behind:0 | b6e90ed | Add Archiavellian narrative architecture batch; GitHub archiavellian (private) |
| Archiavellian-Archive | recovery-core | core | archive | main | untracked:335 | ahead:0 behind:0 | 55e146d | Clean archive index batch note formatting |
| Bankruptcy | recovery-core | core | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | platform-product | adjacent | active | main | clean | ahead:1 behind:0 | cee8dc9 | Add implementation baseline and delivery planning; parent Project Manager; GitHub CIMPT (private) |
| Divorce | - | - | active | main | clean | no-upstream | 9a208c9 | Initial commit: litigation workspace, handoff maps, and PM delivery scaffold. |
| MJS Financial Dash | recovery-core | core | active | codex/finance-snapshot-onboarding | untracked:56 | ahead:0 behind:0 | 8ac9660 | Refresh finance snapshot pipeline, retire generated outputs from version control, and extend reporting and Google sources. |
| MJS Financial Dash Backup | archive-incubator | peripheral | archive | main | clean | ahead:0 behind:0 | e82856a | Reconcile main with rewritten default-branch history after secret purge. |
| MJSDS Dashboard | platform-product | peripheral | active | main | untracked:5 | ahead:0 behind:0 | 4133068 | Align dashboard scaffold with deprecated status |
| MJSDS Website | platform-product | peripheral | onboarding | main | untracked:5 | no-upstream | 138378e | Keep website README project-scoped |
| Momentum-OS | platform-product | adjacent | active | main | untracked:5 | ahead:0 behind:0 | cc1bff2 | Remove stale Momentum-OS snapshot files; GitHub momentum-os (private) |
| provider-access-hub | platform-product | adjacent | active | main | untracked:5 | ahead:0 behind:0 | eded0c5 | Add client-facing delivery scaffold docs |
| Resume Builder | platform-product | adjacent | onboarding | main | untracked:5 | no-upstream | 6e950f5 | Update repo paths after extraction |
| Teach - Home Learning Playbook | family-outcomes | adjacent | active | main | untracked:9 | ahead:1 behind:0 | 8f6ccf5 | Update playbook templates and add production/onboarding docs. |
| Teach - Zahmeir Learning System | family-outcomes | adjacent | active | feat/lesson-1-direct-launch | clean | ahead:1 behind:0 | a8bce64 | Add project onboarding pack |
| TuneFab | archive-incubator | peripheral | archive | main | untracked:1 | no-upstream | 0ccf7a6 | Convert TuneFab into archive workspace |
| Wayne Strain | archive-incubator | peripheral | active | codex/milestone-1-jurisdiction-research | untracked:5 | ahead:1 behind:0 | ea8ebaf | Add onboarding milestone docs |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
