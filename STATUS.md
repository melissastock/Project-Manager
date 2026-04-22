# Portfolio Status

Generated: 2026-04-22 00:24:37 MDT

## Summary

- Managed repositories: 19
- Clean repositories: 16
- Repositories with local changes: 1
- Repositories in onboarding: 2
- Public repositories: 1
- Restricted repositories: 18

## Repository Snapshot

| Project | Lane | Priority | Visibility | Data Class | IP Class | Public Sync | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024 Taxes | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Aneumind and TC Structure | business-structure | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | no-upstream | 56dab4f | Add architecture scale-fit baseline and downstream governance intake metadata. |
| App Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | unstaged:3 | ahead:1 behind:0 | aac003d | Expand project-manager governance and financial KPI tracking surfaces. |
| Archiavellian | archive-incubator | peripheral | private-internal | ip-restricted | personal-os-protected | no | active | codex/archiavellian-report-to-project-manager | clean | ahead:2 behind:0 | ad2c871 | Add architecture scale-fit baseline and downstream governance intake metadata.; GitHub archiavellian (private) |
| Archiavellian-Archive | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | clean | ahead:1 behind:0 | ed842ee | Ignore local evidence drops; add portfolio delivery and GTM scaffold docs. |
| Bankruptcy | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | main | clean | ahead:2 behind:0 | 0b95417 | Add architecture scale-fit baseline and downstream governance intake metadata.; parent Project Manager; GitHub CIMPT (private) |
| Divorce | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | clean | ahead:1 behind:0 | 88c559f | Add architecture scale-fit baseline and downstream governance intake metadata.; GitHub PLP (private) |
| MJS Financial Dash | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/finance-snapshot-onboarding | clean | ahead:1 behind:0 | 69a1e2b | Add architecture scale-fit baseline and downstream governance intake metadata.; GitHub MJS-Financial-Dash (private) |
| MJS Financial Dash Backup | archive-incubator | peripheral | private-archive | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | clean | ahead:1 behind:0 | fcba9ea | Add delivery scaffold docs for archive parity.; GitHub MJS-Financial-Dash-backup (private) |
| MJSDS Dashboard | platform-product | peripheral | public | public-open | internal-standard | yes | active | codex/readiness-checklist-compliance | clean | ahead:2 behind:0 | 35c9a5a | Add architecture scale-fit baseline and downstream governance intake metadata. |
| MJSDS Website | platform-product | peripheral | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | 16e8c69 | Add architecture scale-fit baseline and downstream governance intake metadata. |
| Momentum-OS | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 9f5af4a | Add architecture scale-fit baseline and downstream governance intake metadata.; GitHub momentum-os (private) |
| provider-access-hub | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 506645e | Add architecture scale-fit baseline and downstream governance intake metadata. |
| Resume Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | 36c6443 | Add architecture scale-fit baseline and downstream governance intake metadata. |
| Teach - Home Learning Playbook | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:2 behind:0 | 42d24c3 | Add architecture scale-fit baseline and downstream governance intake metadata. |
| Teach - Zahmeir Learning System | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | ahead:1 behind:0 | 0210a1a | Add architecture scale-fit baseline and downstream governance intake metadata. |
| TuneFab | archive-incubator | peripheral | private-archive | archive-sensitive | internal-standard | no | archive | main | clean | no-upstream | 76d70a3 | Add portfolio docs scaffold under docs/. |
| Wayne Strain | archive-incubator | peripheral | private-internal | research-sensitive | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:2 behind:0 | 4f1fc20 | Add architecture scale-fit baseline and downstream governance intake metadata. |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
