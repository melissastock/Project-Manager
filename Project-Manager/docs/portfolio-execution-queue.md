# Portfolio Execution Queue

Canonical owner-approved queue for batch execution. **Current baseline:** 2026-04-21, 14:37 MDT PM standup artifact set.

## Operating Rules

- Security work first.
- Then drift containment.
- Then planning and packaging gaps.
- Then readiness and release gates.
- Maximum active projects in execution: 3.
- Every action needs owner decision status (`approved`, `rejected`, or `defer`).
- Drift containment comes before backlog, sprint, or feature work.
- Do not bulk commit untracked files. Classify first, then decide whether each item is source, generated output, local-only noise, secret or sensitive material, or archive evidence.
- Treat archive-stage repositories as evidence-preservation workspaces. Prefer holdback notes and manifest-style documentation over broad refactors.
- Run the focused readiness gate only after drift and planning artifacts have been corrected.
- Re-run the PM standup after each batch so score changes are based on live repository state.

## Source Of Truth

Use these artifacts from the Project Manager workspace root:

- `docs/session-artifacts/standup/STANDUP_SUMMARY-20260421_143723.md`
- `docs/session-artifacts/standup/READINESS_SCORECARD-20260421_143723.md`
- `docs/session-artifacts/standup/NEXT_STEPS_PROPOSAL-20260421_143723.md`
- `docs/session-artifacts/standup/DECISION_LOG-20260421_143723.md`

From inside the `docs/` directory, the same files are:

- `session-artifacts/standup/STANDUP_SUMMARY-20260421_143723.md`
- `session-artifacts/standup/READINESS_SCORECARD-20260421_143723.md`
- `session-artifacts/standup/NEXT_STEPS_PROPOSAL-20260421_143723.md`
- `session-artifacts/standup/DECISION_LOG-20260421_143723.md`

Do not execute actions from the 11:47 MDT artifact set except as historical comparison.

## Blocking Owner Decisions

1. Rotate any credentials previously exposed in `token.json` or `credentials.json` history. The git rewrite reduced repository exposure, but it did not invalidate live credentials.
2. Mark each proposed action in `docs/session-artifacts/standup/DECISION_LOG-20260421_143723.md` as `approved`, `rejected`, or `defer`.
3. After each standup regeneration, record the authoritative artifact timestamp in the latest handoff addendum.

## Command Templates

Run commands from the Project Manager workspace root unless noted.

Drift classification:

```sh
git -C "<repo-path>" status --short --untracked-files=all
git -C "<repo-path>" status --branch --short
git -C "<repo-path>" log -1 --oneline
```

Planning gate:

```sh
python3 scripts/check_production_readiness.py --target "<repo-path>"
```

Standup regeneration:

```sh
python3 scripts/run_pm_standup.py
```

Expected per-repo exit criteria:

- `git status --short --untracked-files=all` is clean, or every remaining item is documented as an explicit holdback.
- `docs/delivery/backlog.md` exists and includes grooming metadata plus prioritized items.
- `docs/delivery/sprint-plan.md` exists and includes sprint goal plus committed scope.
- `docs/delivery/test-report.md` exists and includes pass, fail, and not tested notes.
- `docs/delivery/pr-readiness.md` exists and its checklist is either complete or has owner-accepted blockers.
- `python3 scripts/check_production_readiness.py --target "<repo-path>"` passes, or any failure is captured as an explicit deferred decision.

## Queue

| Order | Project | Repo path | Current band | Score | Drift | Required action | Exit criteria |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| 0 | Security rotation | n/a | blocking | n/a | n/a | Rotate exposed credentials from prior `token.json` / `credentials.json` history. | Owner confirms replacement credentials are issued and old credentials are invalidated. |
| 1 | Archiavellian-Archive | `Archiavellian-Archive` | monitor | 70 | 0/0/341 | Classify extreme untracked drift before lower-score repos because it is recovery-core evidence scope. | Untracked files are committed, ignored, removed with approval, or documented as holdback; archive-sensitive disposition noted. |
| 2 | Wayne Strain | `Wayne Strain` | at-risk | 50 | 0/0/7 | Classify drift, refresh missing backlog, confirm sprint, then readiness gate. | Drift contained; backlog exists; sprint remains valid; readiness gate result recorded. |
| 3 | MJS Financial Dash Backup | `MJS Financial Dash backup 20260310_153810` | at-risk | 54 | 0/0/3 | Archive-scoped drift classification plus backlog and sprint docs. | Drift contained; archive-only scope preserved; backlog and sprint docs present; readiness gate result recorded. |
| 4 | MJSDS Dashboard | `GitHub/mjsds_dashboard` | at-risk | 54 | 0/0/7 | Public repo drift classification, backlog and sprint docs, publication safety check, readiness gate. | Drift contained; no private governance or restricted data in public path; planning docs present; readiness gate result recorded. |
| 5 | MJSDS Website | `mjsds-website` | at-risk | 54 | 0/0/7 | Onboarding-scoped drift classification plus backlog and sprint docs. | Drift contained; onboarding scope preserved; planning docs present; readiness gate result recorded. |
| 6 | Teach - Home Learning Playbook | `App Builder/Teach/home-learning-playbook` | at-risk | 57 | 0/0/9 | Family-sensitive drift classification plus backlog and sprint docs. | Drift contained; family-sensitive material handled privately; planning docs present; readiness gate result recorded. |
| 7 | Resume Builder | `Resume Builder` | at-risk | 61 | 0/0/7 | Onboarding-scoped drift classification plus backlog and sprint docs. | Drift contained; planning docs present; readiness gate result recorded. |
| 8 | Archiavellian | `Producer` | at-risk | 56 | 0/0/1 | Classify single untracked item, then backlog and sprint docs. | Drift contained; planning docs present; readiness gate result recorded. |
| 9 | TuneFab | `TuneFab` | at-risk | 56 | 0/0/1 | Archive-scoped single-item drift classification plus backlog and sprint docs. | Drift contained; archive-only scope preserved; planning docs present; readiness gate result recorded. |
| 10 | Aneumind and TC Structure | `Aneumind and TC Structure` | monitor | 84 | 0/0/1 | Core business-structure drift classification and planning docs. | Drift contained; backlog and sprint docs present or explicitly deferred. |
| 11 | Teach - Zahmeir Learning System | `App Builder/Teach/zahmeir-learning-system` | at-risk | 66 | 0/0/0 | Create backlog and sprint docs, then readiness gate. | Planning docs present; readiness gate result recorded. |
| 12 | App Builder | `App Builder/App Builder` | at-risk | 68 | 0/0/0 | Create backlog and sprint docs, then readiness gate. | Planning docs present; readiness gate result recorded. |
| 13 | Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System | `Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System` | at-risk | 68 | 0/0/0 | Create backlog and sprint docs, then readiness gate. | Planning docs present; regulated-sensitive handling confirmed; readiness gate result recorded. |
| 14 | Momentum-OS | `Momentum-OS` | at-risk | 68 | 0/0/0 | Create backlog and sprint docs, then readiness gate. | Planning docs present; readiness gate result recorded. |
| 15 | provider-access-hub | `provider-access-hub` | at-risk | 68 | 0/0/0 | Refresh sprint doc; backlog already detected. | Sprint doc present; regulated-sensitive handling confirmed; readiness gate result recorded. |

## Batch Plan

### Batch A: Security And Evidence Drift

- Rotate exposed credentials.
- Contain `Archiavellian-Archive` drift.

Batch A completion: security item no longer blocks operations, current PM artifacts are governed, and recovery-core archive drift is no longer growing unmanaged.

### Batch B: Highest-Risk Product Drift

- `Wayne Strain`
- `MJS Financial Dash Backup`
- `MJSDS Dashboard`
- `MJSDS Website`

Batch B completion: the lowest-scoring at-risk repos have drift disposition, planning docs, and readiness gate outcomes.

### Batch C: Remaining Drift

- `Teach - Home Learning Playbook`
- `Resume Builder`
- `Archiavellian`
- `TuneFab`
- `Aneumind and TC Structure`

Batch C completion: all currently drift-bearing repos have disposition records.

### Batch D: Planning-Only At-Risk Repos

- `Teach - Zahmeir Learning System`
- `App Builder`
- `Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System`
- `Momentum-OS`
- `provider-access-hub`

Batch D completion: all at-risk repos have backlog/sprint coverage or explicit owner-approved deferrals.

## Final Portfolio Gate

After all approved queue items are complete:

1. Run `python3 scripts/run_pm_standup.py`.
2. Compare the new readiness scorecard to `docs/session-artifacts/standup/READINESS_SCORECARD-20260421_143723.md`.
3. Confirm expected movement:
   - untracked drift decreases or is documented as holdback,
   - at-risk count decreases as planning docs are added,
   - no public repo gains private or restricted material.
4. Write a new handoff addendum naming the new authoritative timestamp.

## Batch Close Checklist

- Re-run `python3 scripts/run_pm_standup.py`.
- Confirm new standup artifacts are timestamped and reviewed.
- Mark the authoritative artifact set in a handoff addendum.
- Capture any deferred actions with rationale and due date.
