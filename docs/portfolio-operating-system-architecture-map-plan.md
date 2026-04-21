# Portfolio Operating System

## Architecture, Lane Map, and Implementation Plan

Version: `v0.1`  
Owner: `Melissa Stock`  
System steward: `Project Manager` repository  
Last updated: `2026-04-20`

---

## 1) System Mission

Create a trustworthy personal operating system for high-stakes legal, financial, business, and family decisions by linking source evidence, analysis workflows, and action-ready outputs across repos without losing boundaries or context.

This operating system must do three things consistently:

1. Preserve truth (source discipline and traceability).
2. Support decisions (clear next actions and owners).
3. Reduce chaos (explicit boundaries between lanes).

---

## 2) Operating Model (Control Plane + Lanes)

### Control Plane

`Project Manager` is the control plane:

- portfolio manifest and status visibility (`config/repos.json`, `STATUS.md`)
- intake and onboarding standards
- reusable process scaffolds (delivery, GTM, investor pack)
- readiness gates and rollout scripts

### Domain Lanes

Each child repo belongs to one lane with one primary mission.

- **Recovery Core lane**: legal/financial stabilization and filing support
- **Business Structure lane**: entity and ownership separation work
- **Family Outcomes lane**: education and family support systems
- **Platform/Product lane**: build-ready products and services
- **Archive/Incubator lane**: preserve-only or exploratory work

---

## 3) Portfolio Lane Map

## Recovery Core (highest priority)

- `Divorce`
- `Bankruptcy`
- `2024 Taxes`
- `MJS Financial Dash`
- `Archiavellian-Archive`

Primary output:
- filing-safe facts, reconstructed obligations, evidence-bound decisions

## Business Structure

- `Aneumind and TC Structure`

Primary output:
- separation decisions, ownership/risk clarity, evidence routing

## Family Outcomes (adjacent but important)

- `App Builder/Teach/home-learning-playbook`
- `App Builder/Teach/zahmeir-learning-system`

Primary output:
- repeatable learning workflows, student-specific execution, progress evidence

## Platform/Product

- `Momentum-OS`
- `provider-access-hub`
- `Combat Injury Post-Incident Medical Tracking & VA Claims Documentation System`
- `Resume Builder`
- `App Builder/App Builder`
- `GitHub/mjsds_dashboard`
- `mjsds-website`

Primary output:
- product specs, delivery artifacts, implementation milestones

## Archive/Incubator or Deprioritized

- `Producer`
- `Wayne Strain`
- `TuneFab`
- `MJS Financial Dash backup 20260310_153810`

Primary output:
- preserved context, bounded exploration, no interference with core lanes

---

## 4) Architecture Layers

## Layer A: Source of Truth

Goal: preserve raw and first-order evidence.

- raw records, statements, filings, communications, exports
- explicit sensitivity posture
- non-destructive retention

Primary repos: `Bankruptcy`, `Archiavellian-Archive`, lane-specific evidence folders in `Divorce`, `Aneumind and TC Structure`, and `MJS Financial Dash`.

## Layer B: Analysis and Synthesis

Goal: convert source evidence into defensible conclusions.

- chronology, issue maps, theory maps, ledgers, reconstructions
- proof labels (documented fact vs inference)
- open-questions tracking

Primary repos: `Divorce`, `MJS Financial Dash`, `Aneumind and TC Structure`, selected docs in `2024 Taxes`.

## Layer C: Action Outputs

Goal: generate action-ready artifacts for next steps.

- attorney packets
- decision memos
- filing support packages
- milestone plans and delivery plans

Primary repos: `Divorce`, `MJS Financial Dash`, `2024 Taxes`, plus product repos where execution follows.

## Layer D: Portfolio Governance

Goal: keep lane boundaries, prioritization, and execution discipline intact.

- intake, onboarding, lane assignment
- sprint/backlog/testing readiness
- status dashboard and drift control

Primary repo: `Project Manager`.

---

## 5) Cross-Repo Routing Rules

1. **Single-home rule**  
   Every decision-critical artifact has one canonical home repo.

2. **Derived-not-duplicate rule**  
   If copied into another repo, label as derived and link to canonical source.

3. **Lane ownership rule**  
   Each repo has one primary lane owner and one backup reviewer.

4. **Priority rule**  
   Recovery Core work preempts adjacent/peripheral work unless explicitly overridden.

5. **Readiness rule**  
   Work is not PR-ready until backlog, sprint plan, and test/report evidence exist (where applicable).

---

## 6) Decision Cadence

## Weekly operating review

Owner: Melissa  
Source: `STATUS.md` + lane-specific blocker notes

Agenda:

1. Recovery Core blockers and deadlines
2. Business Structure dependencies
3. Family Outcomes progress and constraints
4. Product lane carryover and deferrals
5. Archive/incubator parking decisions

## Daily triage (lightweight)

- What changed in Recovery Core?
- What action is due in the next 72 hours?
- What can be deferred safely?

---

## 7) 90-Day Implementation Plan

## Phase 1 (Days 1-14): Normalize and Label

Objective: make the operating system explicit and visible.

Tasks:

1. Add lane tag to each managed repo in `config/repos.json`.
2. Add `lane`, `canonical-owner`, and `priority-class` fields to intake docs.
3. Create a cross-repo canonical artifact index for Recovery Core:
   - artifact id
   - canonical path
   - derived paths (if any)
   - last review date
4. Mark `MJS Financial Dash backup 20260310_153810` as archive-only in status notes.

Success criteria:

- every managed repo has a lane assignment
- Recovery Core has a canonical artifact index baseline
- weekly review can be run from one dashboard + one map doc

## Phase 2 (Days 15-45): Enforce Routing and Readiness

Objective: reduce ambiguity and accidental drift.

Tasks:

1. Add a lane validation check to PM scripts (warn on missing/invalid lane tags).
2. Add canonical-link requirement in selected core repos:
   - legal/financial synthesis docs must reference source anchors
3. Run backbone rollout on all active repos and verify readiness gate behavior.
4. Define backlog for each Recovery Core repo with top 3 decision-critical outcomes.

Success criteria:

- no core repo without lane metadata
- no new synthesis doc without source anchors
- core readiness checks pass before PR/open handoff updates

## Phase 3 (Days 46-90): Optimize Throughput and Handoffs

Objective: increase decision velocity without reducing evidence quality.

Tasks:

1. Add `next-decision-due` tracking to `STATUS.md` generation.
2. Standardize handoff templates for:
   - legal lane updates
   - financial reconstruction updates
   - business-separation updates
3. Establish Recovery Core monthly close-out artifact:
   - key decisions made
   - unresolved blockers
   - required evidence pull list
4. Reclassify peripheral repos explicitly as:
   - parked
   - incubating
   - active-by-exception

Success criteria:

- decisions can be reviewed by lane from one monthly close artifact
- unresolved blockers are visible with owner + due date
- peripheral work no longer competes with core work by default

---

## 8) Metrics

Track monthly:

- `% of repos with complete lane metadata`
- `% of core artifacts with canonical source links`
- `count of unresolved core blockers > 14 days`
- `time from evidence arrival to decision-ready memo`
- `core vs non-core work ratio`

Target direction:

- higher metadata/source-link coverage
- lower blocker age
- faster evidence-to-decision cycle

---

## 9) Risks and Mitigations

- **Risk:** cross-repo duplication causes conflicting truths  
  **Mitigation:** single-home + derived-not-duplicate rule

- **Risk:** adjacent projects consume core bandwidth  
  **Mitigation:** explicit priority class and weekly lane review

- **Risk:** evidence cleanup loses legal/financial context  
  **Mitigation:** preserve-first rule; archive rather than delete

- **Risk:** process overhead slows execution  
  **Mitigation:** keep daily triage lightweight and only enforce critical gates

---

## 10) Immediate Next Actions (This Week)

1. Approve this architecture and lane map as `v0.1`.
2. Update `config/repos.json` with lane metadata.
3. Add lane fields to `docs/new-project-intake-template.md`.
4. Generate refreshed `STATUS.md` with lane-aware notes.
5. Create first Recovery Core canonical artifact index draft.

---

## 11) Definition of Done for OS v1

The operating system is at `v1` when:

- all managed repos are lane-classified
- Recovery Core has canonical artifact indexing
- weekly review is run from `STATUS.md` + this architecture doc
- readiness gates are used consistently for active build repos
- no critical decision is made without source-linked evidence

