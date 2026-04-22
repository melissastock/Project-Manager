# PM-as-Client Full Review

Date: `2026-04-21`  
Scope mode: `one-time full program`  
Coverage: `risk-weighted representative sample`  
Automation target: `high automation with exception-based human review`

---

## 1) Executive Outcome

`Project Manager` is now structurally close to the target operating model (private control plane, classification-aware manifest, archive safety controls), but it is not yet fully execution-safe for high automation at scale.

Top gaps to close for a true PM-as-client operating standard:

1. Role/accountability is not consistently explicit in child project intake artifacts.
2. Onboarding metadata in some sampled projects drifts from manifest truth.
3. Packaging/sending flow exists as fragments across workflows, but no single, gated outbound handoff standard exists.
4. Governance/security checks are present, but not yet orchestrated as one deterministic daily/weekly automation pipeline.

---

## 2) Governance and Doctrine Audit

### What is strong

- Manifest now includes policy-critical fields (`visibility_tier`, `data_class`, `ip_class`, `public_sync_allowed`) in [config/repos.json](config/repos.json).
- Status generation surfaces governance class and sync posture in [STATUS.md](STATUS.md) via [scripts/portfolio_status.py](scripts/portfolio_status.py).
- Public/private architecture and operating doctrine are now explicit in:
  - [docs/pm-public-private-git-architecture.md](docs/pm-public-private-git-architecture.md)
  - [docs/git-operating-model-policy.md](docs/git-operating-model-policy.md)
- Backup remote collision risk has technical controls (`canonical-readonly`, blocked push path, collision script).

### Material gaps

- Branch protection/rulesets are not yet uniformly enforced on canonical default branches (from earlier audit artifact).
- No single PM command currently executes full governance gate sequence (status + collisions + readiness + review-gate summary).
- Policy is documented, but exception logging and approval path are not standardized in one runbook.

### Governance verdict

- **Doctrine alignment:** `Mostly aligned`
- **Operational enforceability:** `Partially enforceable`
- **Automation readiness:** `Moderate (needs orchestration and exception protocol)`

---

## 3) Managed Project Sanity Check (Risk-Weighted Sample)

Sample selected by risk profile:

- legal/financial restricted: `Divorce`, `MJS Financial Dash`
- regulated-sensitive: `provider-access-hub`
- public-facing: `MJSDS Dashboard`
- archive/backup: `MJS Financial Dash Backup`

## Findings by project

### A) `Divorce` (legal/financial restricted)

Strengths:
- Properly lane-assigned and classified in manifest (`recovery-core`, `private-client`, restricted classes).
- Delivery scaffold files exist (`docs/delivery/*`, intake present).

Resolved (post-review execution):
- Intake updated for remote created, role ownership, and disabled non-applicable GTM/investor defaults for litigation posture.
- Remote recorded as `https://github.com/melissastock/PLP.git` (manifest + git).

### B) `MJS Financial Dash` (legal/financial restricted)

Strengths:
- Correctly marked as canonical recovery-core finance repository.
- Onboarding/delivery docs exist.

Resolved (post-review execution):
- `docs/project-intake.md` added/aligned with remote created, role ownership, and workflow flags appropriate to recovery-core finance work.

### C) `provider-access-hub` (regulated-sensitive)

Strengths:
- Delivery scaffolds exist and PM-managed structure is in place.

Resolved (post-review execution):
- Intake aligned to `regulated-sensitive` and manifest lane/priority/classification fields; role ownership recorded.

### D) `MJSDS Dashboard` (public-facing)

Strengths:
- Public-safe framing is explicit in intake and manifest (`public-open`).
- Maintains clearer product-vs-PM boundary than most sampled repos.

Gaps:
- Public release path should explicitly reference redaction/publication gate dependencies from PM policy.

### E) `MJS Financial Dash Backup` (archive/backup)

Strengths:
- Archive posture now explicit; remote separation controls are in place.
- Correctly classified as `private-archive`, `public_sync_allowed: false`.

Gaps:
- Archive-specific onboarding profile is minimal (acceptable but should be codified as intentional archive profile).

---

## 4) Onboarding -> Implementation -> Packaging -> Sending Flow Review

Current process artifacts exist but are distributed:

- Intake: [docs/new-project-intake-template.md](docs/new-project-intake-template.md)
- Onboarding: [docs/new-project-onboarding-checklist.md](docs/new-project-onboarding-checklist.md)
- Delivery standards: [docs/agile-production-process.md](docs/agile-production-process.md)
- Review gates: [docs/REVIEW_GATES.md](docs/REVIEW_GATES.md)
- GTM/Investor packaging (conditional):
  - [docs/gtm-repeatable-workflow.md](docs/gtm-repeatable-workflow.md)
  - [docs/investor-book-repeatable-workflow.md](docs/investor-book-repeatable-workflow.md)

### Flow breakpoints

1. **Metadata drift breakpoint**  
   Child `docs/project-intake.md` values can diverge from manifest policy values.
2. **Conditional packaging ambiguity**  
   GTM/investor-book requirements can be set by template defaults rather than project reality.
3. **Sending/handoff gap**  
   No single PM-wide outbound sending standard with explicit recipient class, sensitivity class, and release approval record.

---

## 5) Agent/Automation Opportunity Map

## High-automation candidates (recommended now)

1. **Daily governance sweep**
   - Trigger: daily or pre-PR
   - Tools: `portfolio_status.py`, `check_remote_collisions.py`, `review_gate.py`
   - Guardrails: fail on missing classification/unsafe collisions
   - Exception: manual override entry in session handoff

2. **Intake consistency validator**
   - Trigger: when `docs/project-intake.md` or `config/repos.json` changes
   - Check: lane, priority, visibility/data/IP consistency
   - Exception: approved temporary mismatch with due-date

3. **Packaging gate orchestrator**
   - Trigger: pre-release / pre-send event
   - Check: review gates + readiness docs + sensitivity class
   - Exception: legal/counsel urgent override with signoff

4. **Public mirror eligibility gate**
   - Trigger: publish candidate change
   - Check: allowlist + classification constraints
   - Exception: none for restricted classes

## Human-required boundaries (never fully automated)

- Legal strategy interpretation and filing judgment.
- Financial claim interpretation where evidence quality is disputed.
- External outbound sending to counsel/court/investor audiences when restricted data is involved.

---

## 6) Tools and Roles Sanity Check (RACI-like)

Core PM service functions and proposed role ownership:

- **Governance Steward (A/R):** policy updates, classification schema, gate decisions.
- **Lane Operator (R):** lane backlog hygiene and project-specific metadata correctness.
- **Release/Packaging Owner (R):** package composition and release notes completeness.
- **Compliance Reviewer (A/R):** publication safety, privacy/legal constraints, outbound release approval.
- **Automation Maintainer (R):** scripts, validators, CI hooks, failure triage.
- **Principal Owner (A):** final exception approval and risk acceptance.

Resolved (post-review execution): explicit role fields are now present in manifest defaults and intake template; child intakes for sampled high-risk repos were updated accordingly.

---

## 7) Project-Type Fitness Sanity Check

Project types in portfolio require different default workflows. Recommended defaults:

- **Legal/financial restricted (`recovery-core`)**
  - Delivery required: yes
  - GTM default: no
  - Investor-book default: no
  - Sending requires compliance reviewer signoff: yes

- **Regulated-sensitive platform/client**
  - Delivery required: yes
  - GTM/investor: conditional
  - Sending signoff: yes

- **Public-facing product**
  - Delivery required: yes
  - Public mirror/publication checks: mandatory

- **Archive/backup**
  - Delivery required: no (archive profile)
  - Canonical/remote safety checks: mandatory
  - Sending: disabled unless approved extraction package

---

## 8) 90-Day PM-as-Client Program

### Phase 1 (Days 1-21): Stabilize Governance

- Add explicit role fields and ownership fields to manifest and intake standards.
- Implement intake-vs-manifest drift check script.
- Create outbound sending standard (recipient class + data class + approval record).
- Baseline branch protection/ruleset checklist for all canonical repos.

Exit criteria:
- No unresolved manifest/intake policy mismatches in sampled high-risk repos.
- Daily governance sweep runs clean or with tracked exceptions.

### Phase 2 (Days 22-56): Operationalize Automation

- Add orchestration script for governance sweep.
- Add packaging gate command that consolidates readiness + compliance checks.
- Enforce conditional workflows by project type (GTM/investor required only when policy says yes).

Exit criteria:
- Deterministic pre-send/pre-release gate pass/fail outputs.
- Exception log format adopted across sessions.

### Phase 3 (Days 57-90): Scale and Lock

- Expand sanity checks from representative sample to all managed repos.
- Publish PM-as-client runbook and quarterly control checklist.
- Run final doctrine compliance audit and close open exceptions.

Exit criteria:
- Full portfolio passes governance baseline checks.
- PM operates as service model with repeatable roles, gates, and automation.

---

## 9) Once-and-Done Deliverables (This Engagement)

1. This review document.
2. PM-as-client implementation backlog: [docs/pm-as-client-implementation-backlog-2026-04-21.md](docs/pm-as-client-implementation-backlog-2026-04-21.md).
3. PM daily/weekly governance runbook: [docs/pm-governance-runbook.md](docs/pm-governance-runbook.md) plus sweep script [scripts/run_pm_governance_sweep.sh](scripts/run_pm_governance_sweep.sh).
4. Role assignment register: [docs/manifests/pm-role-register-2026-04-21.csv](docs/manifests/pm-role-register-2026-04-21.csv).

---

## 10) Recommended Immediate Next Actions

1. Enforce branch protection/rulesets on canonical default branches for all managed GitHub repos.
2. Implement intake-vs-manifest drift validator (script + optional CI hook).
3. Add outbound sending checklist and wire it into pre-send runbook section.
4. Expand representative sample checks to full portfolio in Phase 3 of the 90-day program.

