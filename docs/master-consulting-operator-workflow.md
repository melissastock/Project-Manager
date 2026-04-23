# Master Consulting Operator Workflow

Single source of truth for how to sell, deliver, package, secure, and get paid for consulting engagements.

**Posture:** consulting-first. The client is not expected to self-operate the system.

---

## 1) Offer architecture (what you sell)

### SKU A — Clarity Sprint Diagnostic

| | |
| --- | --- |
| **Standard** | $3,500 |
| **Fast-track** | $5,000 |
| **Timeline** | 7–10 business days |

**Promise:** turn fragmented legal, financial, and operational work into a decision-ready 30-day action plan.

**Deliverables:**

- Current-state workflow map
- Risk and bottleneck register
- Prioritized decision packet
- 30-day implementation roadmap
- Executive readout

### SKU B — Execution OS Build Sprint

| | |
| --- | --- |
| **Price** | $12,000–$25,000 (scope-based) |
| **Timeline** | 90 days (phased) |

**Promise:** install repeatable execution workflow, reporting, and governance cadence.

**Deliverables:**

- Intake and evidence routing workflow
- Dashboard and tracking baseline
- Standardized reporting outputs
- Team operating cadence and governance loop
- Handoff and enablement package

---

## 2) Marketing USP (how you position)

**Primary USP:** We convert high-risk operational chaos into decision-ready execution in 10 business days, then operationalize it into a repeatable 90-day system.

**Proof anchors:**

- MJS Financial Dash
- Legal workflow orchestration
- CIMPT architecture

**Website hero:**

- **Headline:** From operational chaos to decision-ready execution in 10 business days.
- **CTA:** Book a 30-minute fit call
- **Secondary CTA:** See a sample decision packet

---

## 3) Consulting workflow: end-to-end stage gates

Move through these stages in order. Do not skip gates.

### Stage 0 — Setup (one-time)

**Keep these templates ready:**

- Fit call script
- SOW
- Kickoff checklist
- Weekly status update
- Final package checklist
- Invoice template

**Payment policy:**

- SKU A: 100% upfront
- SKU B: 50% kickoff, 30% midpoint, 20% final handoff

**Stop rules:**

- No signed SOW → no work
- No payment milestone → no milestone delivery
- No scope change without change order

**Exit gate:** Sales and delivery templates are live and versioned.

### Stage 1 — Qualification

- Run 30-minute fit call.

**Score Yes/No:**

- Urgent pain now
- Decision owner present
- Data visibility available
- Weekly cadence commitment
- Scoped objective is clear

**Decide:**

- 4–5 Yes → proceed
- 3 Yes → constrained scope only
- 0–2 Yes → defer or decline

**Exit gate:** Go / No-Go documented with next action.

### Stage 2 — Scope and close

- Send scoped offer (SKU A or B).
- Send SOW with: objective; scope in/out; deliverables; timeline; payment milestones; change-order terms.
- Run one live SOW review.
- Send signature and kickoff invoice.
- Confirm payment receipt.

**Exit gate:** Signed SOW + payment received + kickoff date set.

### Stage 3 — Kickoff and security controls

- Create client engagement record.
- Set communication channel and decision owner.
- Classify sensitivity: legal; financial; medical; IP/confidential.
- Configure secure storage path and access roles.
- Register intake artifacts and source systems.
- Lock baseline scope after intake complete.

**Exit gate:** Intake complete, access controlled, scope locked.

### Stage 4 — Delivery

- Execute sprint plan.
- **Weekly updates to client:** work completed; risks/blockers; decisions needed; next week plan.
- **Track requests:** in-scope → schedule; out-of-scope → change order.
- **Enforce data placement:** source truth → `recovery-core`; processing workflows → `execution-*`; sanitized outputs → `narrative-output`.

**Exit gate:** Contracted deliverables drafted and internally reviewed.

### Stage 5 — Packaging and readout

**Final package:**

- Executive summary
- Deliverables index
- Decisions made
- Remaining risks
- 30-day next action plan

- Verify package against SOW line-by-line.
- Redact sensitive non-required content.
- Run executive readout.
- Obtain written acceptance.

**Exit gate:** Written acceptance received.

### Stage 6 — Invoice, payment, and close

- Send final milestone invoice same day as acceptance.

**Follow-up rhythm:**

- Day 0: send
- Day 3: reminder
- Day 7: escalation reminder
- Day 10: direct owner call

**After payment clears:**

- Release unrestricted final assets
- Send close memo
- Archive inactive materials
- Capture sanitized case proof

**Exit gate:** Funds received, closeout complete, project marked closed.

---

## 4) Payment operations (recommended setup)

**Two-lane payment stack:**

- **Stripe Payment Links / Invoices (default):** card + ACH; clear invoice status; easy links for deposits and milestones.
- **Wire/ACH fallback** for larger engagements.

**Implementation:**

- **Stripe products:** Clarity Sprint Standard — $3,500; Clarity Sprint Fast-track — $5,000; Execution OS Build Sprint — custom invoice.
- **Invoice templates:** kickoff deposit; midpoint milestone; final milestone.
- **SOW policy:** work starts only after initial payment clears; milestone delivery tied to milestone payment; late fees/escalation clause if applicable.

---

## 5) mjsdigitalstrategy.com

**Yes** — add as a controlled consulting funnel, not a self-serve product.

**Minimum pages:**

- Home (USP + CTA)
- Offers (SKU A / B with range pricing and outcomes)
- Proof (sanitized case snapshots)
- Security and process (how consulting delivery works)
- Book call

**Minimum CTAs:**

- Book a fit call
- Request scope
- Pay deposit (private link after scope confirmation)

---

## 6) Client portal (v1)

**Yes** — keep v1 minimal and consultant-operated.

**Portal v1 scope:**

- **Client dashboard:** stage; current milestone; next meeting
- **Shared status feed:** weekly updates; decisions needed
- **Deliverables list:** accepted outputs; pending approvals
- **Invoices:** issued; paid; outstanding
- **Secure file handoff links** (no raw sensitive sprawl)

**Portal v1 should NOT include:**

- Client self-configuration
- Open-ended workflow editing
- Broad document dumping

---

## 7) 14-day implementation plan (operator)

**Days 1–3**

- Finalize website copy from USP doc.
- Publish Offer page with pricing ranges and outcomes.
- Configure Stripe products + invoice templates.

**Days 4–7**

- Add fit call booking flow.
- Add security/process explainer page.
- Add internal rule: no kickoff before signed SOW + payment.

**Days 8–10**

- Launch client portal v1 pages: status; deliverables; invoices.
- Connect weekly status template into portal update cadence.

**Days 11–14**

- Run first live client through full stage-gated workflow.
- Capture friction notes.
- Update templates and scripts.
- Freeze v1 process for consistency.

---

## 8) Non-negotiable anti-spin rules

- No work without signed SOW and cleared payment milestone.
- No unapproved scope expansion.
- No hidden work streams outside tracker.
- No final unrestricted handoff before final payment.
- No open project after closeout checklist is complete.

**When stuck, ask:**

1. What stage am I in?
2. What is the stage exit gate?
3. What single action gets me through that gate today?
