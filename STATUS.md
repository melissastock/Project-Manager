# Portfolio Status

Generated: 2026-04-21 11:11:24 MDT

## Summary

- Managed repositories: 19
- Clean repositories: 5
- Repositories with local changes: 12
- Repositories in onboarding: 2
- Public repositories: 1
- Restricted repositories: 18

## Repository Snapshot

| Project | Lane | Priority | Visibility | Data Class | IP Class | Public Sync | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024 Taxes | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Aneumind and TC Structure | business-structure | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/taylor-shell-claim-scenario | clean | no-upstream | c1a02f2 | Add onboarding pack |
| App Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/project-manager-scaffold | untracked:5 | ahead:3 behind:0 | 89b7045 | Update Resume Builder repository path |
| Archiavellian | archive-incubator | peripheral | private-internal | ip-restricted | personal-os-protected | no | active | codex/archiavellian-report-to-project-manager | untracked:1 | ahead:0 behind:0 | 742d72e | Run Archiavellian through PM governance intake and readiness workflow.; GitHub archiavellian (private) |
| Archiavellian-Archive | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | archive | main | untracked:335 | ahead:0 behind:0 | 55e146d | Clean archive index batch note formatting |
| Bankruptcy | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | main | clean | ahead:1 behind:0 | cee8dc9 | Add implementation baseline and delivery planning; parent Project Manager; GitHub CIMPT (private) |
| Divorce | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | clean | no-upstream | cc7ce56 | Update litigation intake roles and disable non-applicable GTM/investor workflows. |
| MJS Financial Dash | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/finance-snapshot-onboarding | untracked:55 | ahead:0 behind:0 | 8d2fb0a | Set PM role ownership in intake and disable non-applicable GTM/investor defaults. |
| MJS Financial Dash Backup | archive-incubator | peripheral | private-archive | legal-financial-restricted | client-invention-protected | no | archive | main | clean | ahead:0 behind:0 | 9da2182 | Clarify backup repository as archive-only and non-canonical.; GitHub MJS-Financial-Dash-backup (private) |
| MJSDS Dashboard | platform-product | peripheral | public | public-open | internal-standard | yes | active | main | untracked:5 | ahead:0 behind:0 | 4133068 | Align dashboard scaffold with deprecated status |
| MJSDS Website | platform-product | peripheral | private-internal | internal-ops | personal-os-protected | no | onboarding | main | untracked:5 | no-upstream | 138378e | Keep website README project-scoped |
| Momentum-OS | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | main | untracked:5 | ahead:0 behind:0 | cc1bff2 | Remove stale Momentum-OS snapshot files; GitHub momentum-os (private) |
| provider-access-hub | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | main | untracked:5 | ahead:0 behind:0 | a4e9ba8 | Align intake metadata with regulated-sensitive PM classification and role ownership. |
| Resume Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | onboarding | main | untracked:5 | no-upstream | 6e950f5 | Update repo paths after extraction |
| Teach - Home Learning Playbook | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | main | untracked:9 | ahead:1 behind:0 | 8f6ccf5 | Update playbook templates and add production/onboarding docs. |
| Teach - Zahmeir Learning System | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | feat/lesson-1-direct-launch | clean | ahead:1 behind:0 | a8bce64 | Add project onboarding pack |
| TuneFab | archive-incubator | peripheral | private-archive | archive-sensitive | internal-standard | no | archive | main | untracked:1 | no-upstream | 0ccf7a6 | Convert TuneFab into archive workspace |
| Wayne Strain | archive-incubator | peripheral | private-internal | research-sensitive | personal-os-protected | no | active | codex/milestone-1-jurisdiction-research | untracked:5 | ahead:1 behind:0 | ea8ebaf | Add onboarding milestone docs |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
