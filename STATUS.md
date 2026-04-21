# Portfolio Status

Generated: 2026-04-21 14:07:23 MDT

## Summary

- Managed repositories: 19
- Clean repositories: 4
- Repositories with local changes: 13
- Repositories in onboarding: 2
- Public repositories: 1
- Restricted repositories: 18

## Repository Snapshot

| Project | Lane | Priority | Visibility | Data Class | IP Class | Public Sync | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024 Taxes | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Aneumind and TC Structure | business-structure | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/delivery-gates-baseline | untracked:1 | no-upstream | 7e95ba2 | Add baseline delivery docs for portfolio readiness gating. |
| App Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | untracked:7 | no-upstream | f35de53 | Complete PR readiness checklist and add governance compliance note. |
| Archiavellian | archive-incubator | peripheral | private-internal | ip-restricted | personal-os-protected | no | active | codex/archiavellian-report-to-project-manager | untracked:1 | ahead:0 behind:0 | 742d72e | Run Archiavellian through PM governance intake and readiness workflow.; GitHub archiavellian (private) |
| Archiavellian-Archive | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | untracked:341 | no-upstream | 913b690 | Annotate archive-stage readiness checklist with policy exemption context. |
| Bankruptcy | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | main | clean | ahead:1 behind:0 | cee8dc9 | Add implementation baseline and delivery planning; parent Project Manager; GitHub CIMPT (private) |
| Divorce | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | clean | ahead:0 behind:0 | cc7ce56 | Update litigation intake roles and disable non-applicable GTM/investor workflows. |
| MJS Financial Dash | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/finance-snapshot-onboarding | clean | ahead:0 behind:0 | d37b91f | Add automated handoff readiness gates and CI enforcement. |
| MJS Financial Dash Backup | archive-incubator | peripheral | private-archive | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | untracked:3 | no-upstream | eb61ba1 | Annotate archive-stage readiness checklist with policy exemption context.; GitHub MJS-Financial-Dash-backup (private) |
| MJSDS Dashboard | platform-product | peripheral | public | public-open | internal-standard | yes | active | codex/readiness-checklist-compliance | untracked:7 | no-upstream | d232d1e | Complete PR readiness checklist and add governance compliance note. |
| MJSDS Website | platform-product | peripheral | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | untracked:7 | no-upstream | 6a7e959 | Complete PR readiness checklist and add governance compliance note. |
| Momentum-OS | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | untracked:7 | no-upstream | 713339f | Complete PR readiness checklist and add governance compliance note.; GitHub momentum-os (private) |
| provider-access-hub | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | untracked:7 | no-upstream | e3e3ef7 | Complete PR readiness checklist and add governance compliance note. |
| Resume Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | untracked:7 | no-upstream | 91ad23e | Complete PR readiness checklist and add governance compliance note. |
| Teach - Home Learning Playbook | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | untracked:9 | no-upstream | 8bb2f94 | Complete PR readiness checklist and add governance compliance note. |
| Teach - Zahmeir Learning System | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | no-upstream | 4a53e72 | Add baseline delivery docs for portfolio readiness gating. |
| TuneFab | archive-incubator | peripheral | private-archive | archive-sensitive | internal-standard | no | archive | main | untracked:1 | no-upstream | 0ccf7a6 | Convert TuneFab into archive workspace |
| Wayne Strain | archive-incubator | peripheral | private-internal | research-sensitive | personal-os-protected | no | active | codex/readiness-checklist-compliance | untracked:7 | no-upstream | 43190f2 | Complete PR readiness checklist and add governance compliance note. |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
