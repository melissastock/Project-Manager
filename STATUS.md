# Portfolio Status

Generated: 2026-04-21 18:46:55 MDT

## Summary

- Managed repositories: 19
- Clean repositories: 17
- Repositories with local changes: 0
- Repositories in onboarding: 2
- Public repositories: 1
- Restricted repositories: 18

## Repository Snapshot

| Project | Lane | Priority | Visibility | Data Class | IP Class | Public Sync | Stage | Branch | Status | Sync | Head | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024 Taxes | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Aneumind and TC Structure | business-structure | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | no-upstream | 1938bf5 | Ignore local Archive originals; keep separation artifacts out of git. |
| App Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 8652ba6 | Add monetization planning and readiness scaffold docs. |
| Archiavellian | archive-incubator | peripheral | private-internal | ip-restricted | personal-os-protected | no | active | codex/archiavellian-report-to-project-manager | clean | ahead:1 behind:0 | ad67ce4 | Add Signal Noise narrative source file.; GitHub archiavellian (private) |
| Archiavellian-Archive | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | clean | ahead:1 behind:0 | ed842ee | Ignore local evidence drops; add portfolio delivery and GTM scaffold docs. |
| Bankruptcy | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | unborn | unborn | - | - | Repository exists but has no commits yet |
| Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | main | clean | ahead:1 behind:0 | cee8dc9 | Add implementation baseline and delivery planning; parent Project Manager; GitHub CIMPT (private) |
| Divorce | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | main | clean | ahead:0 behind:0 | cc7ce56 | Update litigation intake roles and disable non-applicable GTM/investor workflows.; GitHub PLP (private) |
| MJS Financial Dash | recovery-core | core | private-client | legal-financial-restricted | client-invention-protected | no | active | codex/finance-snapshot-onboarding | clean | ahead:0 behind:0 | d37b91f | Add automated handoff readiness gates and CI enforcement.; GitHub MJS-Financial-Dash (private) |
| MJS Financial Dash Backup | archive-incubator | peripheral | private-archive | legal-financial-restricted | client-invention-protected | no | archive | codex/archive-readiness-annotation | clean | ahead:1 behind:0 | fcba9ea | Add delivery scaffold docs for archive parity.; GitHub MJS-Financial-Dash-backup (private) |
| MJSDS Dashboard | platform-product | peripheral | public | public-open | internal-standard | yes | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 125dd94 | Add portfolio delivery and GTM scaffold docs for readiness gating. |
| MJSDS Website | platform-product | peripheral | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | e76c138 | Add portfolio delivery and GTM scaffold docs for readiness gating. |
| Momentum-OS | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 2fc8bdf | Add monetization docs and intake gating artifacts.; GitHub momentum-os (private) |
| provider-access-hub | platform-product | adjacent | private-client | regulated-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:0 behind:0 | 55570d5 | Add monetization planning and readiness scaffold docs. |
| Resume Builder | platform-product | adjacent | private-internal | internal-ops | personal-os-protected | no | onboarding | codex/readiness-checklist-compliance | clean | no-upstream | 63aa2e3 | Add portfolio delivery and GTM scaffold docs for readiness gating. |
| Teach - Home Learning Playbook | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | 2e83f14 | Track sprint and tracker templates; ignore local intake and student profiles. |
| Teach - Zahmeir Learning System | family-outcomes | adjacent | private-client | family-sensitive | client-invention-protected | no | active | codex/delivery-gates-baseline | clean | ahead:0 behind:0 | 4a53e72 | Add baseline delivery docs for portfolio readiness gating. |
| TuneFab | archive-incubator | peripheral | private-archive | archive-sensitive | internal-standard | no | archive | main | clean | no-upstream | 76d70a3 | Add portfolio docs scaffold under docs/. |
| Wayne Strain | archive-incubator | peripheral | private-internal | research-sensitive | personal-os-protected | no | active | codex/readiness-checklist-compliance | clean | ahead:1 behind:0 | eb1bc7d | Add portfolio delivery and GTM scaffold docs for readiness gating. |

## Intake And Onboarding

Use this repo as the portfolio control plane:

- Create a new project intake doc from `docs/new-project-intake-template.md`.
- Add the new repo to `config/repos.json` once the location and role are confirmed.
- Run `python3 scripts/portfolio_status.py` to refresh this dashboard.
- Commit the manifest and dashboard changes from the top-level `Project Manager` repo.
