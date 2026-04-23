# Portfolio Status

Generated: 2026-04-23 13:22:27 MDT

## Summary

- Managed repositories: 21
- Clean repositories: 16
- Repositories with local changes: 4
- Repositories in onboarding: 3
- Public repositories: 1
- Restricted repositories: 20

## Repository Snapshot

| Project | Lane | Priority | Visibility | Data Class | IP Class | Public Sync | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024 Taxes | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | clean | no-upstream | 64bf64a | Initialize 2024 Taxes repository baseline. |
| Aneumind and TC Structure | business-structure | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | no-upstream | ddb39dd | Sync os-registry snapshots and file manifests. |
| App Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | bc6a0cd | Sync os-registry snapshots and file manifests. |
| Archiavellian | archive-incubator | peripheral | private-internal | ip-restricted | personal-os-protected | no | active | codex/archiavellian-report-to-project-manager | untracked:1 | ahead:0 behind:0 | b6aebe8 | Sync os-registry snapshots and file manifests.; GitHub archiavellian (private) |
| Archiavellian-Archive | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | untracked:1 | ahead:2 behind:0 | c1f9a1d | Add Case Files archive intake inventory |
| Bankruptcy | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | clean | no-upstream | 6b630cf | Initialize Bankruptcy repository baseline. |
| Case Files | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | not-initialized | unborn | - | - | Folder exists but is not initialized as a git repository |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | main | clean | ahead:0 behind:0 | f8b711c | Sync os-registry snapshots and file manifests.; parent Project Manager; GitHub CIMPT (private) |
| Divorce | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | untracked:1 | ahead:1 behind:0 | 5cca571 | Add persona research scaffolds to project intake governance metadata.; GitHub PLP (private) |
| MJS Financial Dash | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/finance-snapshot-onboarding | untracked:1 | ahead:1 behind:0 | 9c03a4b | Add persona research scaffolds to project intake governance metadata.; GitHub MJS-Financial-Dash (private) |
| MJS Financial Dash Backup | archive-incubator | peripheral | private-archive | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | clean | ahead:0 behind:0 | f54939e | Sync os-registry snapshots and file manifests.; GitHub MJS-Financial-Dash-backup (private) |
| MJSDS Dashboard | platform-product | peripheral | public | public-open | internal-standard | yes | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 1a2c7b1 | Sync os-registry snapshots and file manifests. |
| MJSDS Website | platform-product | peripheral | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | 11ef61e | Sync os-registry snapshots and file manifests. |
| Momentum-OS | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | e1de0de | Sync os-registry snapshots and file manifests.; GitHub momentum-os (private) |
| provider-access-hub | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 11b3c0a | Sync os-registry snapshots and file manifests. |
| Resume Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | 062a4fa | Sync os-registry snapshots and file manifests. |
| Teach - Home Learning Playbook | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 62a9a9f | Sync os-registry snapshots and file manifests. |
| Teach - Zahmeir Learning System | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | ahead:0 behind:0 | fcf5f01 | Sync os-registry snapshots and file manifests. |
| TuneFab | archive-incubator | peripheral | private-archive | archive-sensitive | internal-standard | no | archive | main | clean | no-upstream | 703c93c | Sync os-registry snapshots and file manifests. |
| Wayne Strain | archive-incubator | peripheral | private-internal | research-sensitive | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 7898993 | Sync os-registry snapshots and file manifests. |
| os-registry | platform-product | core | private-internal | internal-ops | personal-os-protected | no | onboarding | main | clean | no-upstream | dbab96d | Initialize os-registry data foundation and sync tooling. |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
