# Portfolio Status

Generated: 2026-04-22 02:04:34 MDT

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
| Aneumind and TC Structure | business-structure | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | no-upstream | 353b41b | Add persona research scaffolds to project intake governance metadata. |
| App Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 9aa0b4f | Add intake process visibility and completion checks to portal UI. |
| Archiavellian | archive-incubator | peripheral | private-internal | ip-restricted | personal-os-protected | no | active | codex/archiavellian-report-to-project-manager | clean | ahead:1 behind:0 | 6c41a6d | Add persona research scaffolds to project intake governance metadata.; GitHub archiavellian (private) |
| Archiavellian-Archive | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | unstaged:2, untracked:1 | ahead:1 behind:0 | ed842ee | Ignore local evidence drops; add portfolio delivery and GTM scaffold docs. |
| Bankruptcy | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | main | clean | ahead:1 behind:0 | 44f8495 | Add persona research scaffolds to project intake governance metadata.; parent Project Manager; GitHub CIMPT (private) |
| Divorce | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | clean | ahead:1 behind:0 | 5cca571 | Add persona research scaffolds to project intake governance metadata.; GitHub PLP (private) |
| MJS Financial Dash | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/finance-snapshot-onboarding | clean | ahead:1 behind:0 | 9c03a4b | Add persona research scaffolds to project intake governance metadata.; GitHub MJS-Financial-Dash (private) |
| MJS Financial Dash Backup | archive-incubator | peripheral | private-archive | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | clean | ahead:1 behind:0 | fcba9ea | Add delivery scaffold docs for archive parity.; GitHub MJS-Financial-Dash-backup (private) |
| MJSDS Dashboard | platform-product | peripheral | public | public-open | internal-standard | yes | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 5480770 | Add persona research scaffolds to project intake governance metadata. |
| MJSDS Website | platform-product | peripheral | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | 1835ed4 | Add persona research scaffolds to project intake governance metadata. |
| Momentum-OS | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 69eb6fb | Add persona research scaffolds to project intake governance metadata.; GitHub momentum-os (private) |
| provider-access-hub | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 2286e18 | Add persona research scaffolds to project intake governance metadata. |
| Resume Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | 8584edc | Add persona research scaffolds to project intake governance metadata. |
| Teach - Home Learning Playbook | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 757305d | Add persona research scaffolds to project intake governance metadata. |
| Teach - Zahmeir Learning System | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | ahead:1 behind:0 | bc9fce4 | Add persona research scaffolds to project intake governance metadata. |
| TuneFab | archive-incubator | peripheral | private-archive | archive-sensitive | internal-standard | no | archive | main | clean | no-upstream | 76d70a3 | Add portfolio docs scaffold under docs/. |
| Wayne Strain | archive-incubator | peripheral | private-internal | research-sensitive | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 7274e12 | Add persona research scaffolds to project intake governance metadata. |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
