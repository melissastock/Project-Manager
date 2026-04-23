# Master Consulting Operator Workflow

Use this as the single source of truth for how to sell, deliver, package, secure, and get paid for consulting engagements.

This is consulting-first. The client is not expected to self-operate the system.

---

## 1) Your Offer Architecture (What You Sell)

## SKU A — Clarity Sprint Diagnostic

- Price:
  - Standard: `$3,500`
  - Fast-track: `$5,000`
- Timeline: `7-10 business days`
- Promise: turn fragmented legal/financial/operational work into a decision-ready 30-day action plan.

Deliverables:

1. Current-state workflow map
2. Risk + bottleneck register
3. Prioritized decision packet
4. 30-day implementation roadmap
5. Executive readout

## SKU B — Execution OS Build Sprint

- Price: `$12,000-$25,000` (scope-based)
- Timeline: `90 days` (phased)
- Promise: install repeatable execution workflow, reporting, and governance cadence.

Deliverables:

1. Intake/evidence routing workflow
2. Dashboard and tracking baseline
3. Standardized reporting outputs
4. Team operating cadence and governance loop
5. Handoff and enablement package

---

## 2) Marketing USP (How You Position)

Primary USP:

We convert high-risk operational chaos into decision-ready execution in 10 business days, then operationalize it into a repeatable 90-day system.

Proof anchors:

- MJS Financial Dash
- Legal workflow orchestration
- CIMPT architecture

Website hero:

- Headline: `From operational chaos to decision-ready execution in 10 business days.`
- CTA: `Book a 30-minute fit call`
- Secondary CTA: `See a sample decision packet`

---

## 3) Consulting Workflow: End-to-End Stage Gates

Move through these stages in order. Do not skip gates.

### Stage 0 — Setup (one-time)

1. Keep these templates ready:
   - fit call script
   - SOW
   - kickoff checklist
   - weekly status update
   - final package checklist
   - invoice template
2. Set payment policy:
   - SKU A: 100% upfront
   - SKU B: 50% kickoff, 30% midpoint, 20% final handoff
3. Set stop rules:
   - no signed SOW -> no work
   - no payment milestone -> no milestone delivery
   - no scope change without change order

Exit gate:

- Sales and delivery templates are live and versioned.

### Stage 1 — Qualification

1. Run 30-minute fit call.
2. Score Yes/No:
   - urgent pain now
   - decision owner present
   - data visibility available
   - weekly cadence commitment
   - scoped objective is clear
3. Decide:
   - 4-5 Yes -> proceed
   - 3 Yes -> constrained scope only
   - 0-2 Yes -> defer/decline

Exit gate:

- Go/No-Go documented with next action.

### Stage 2 — Scope and Close

1. Send scoped offer (SKU A or B).
2. Send SOW with:
   - objective
   - scope in/out
   - deliverables
   - timeline
   - payment milestones
   - change-order terms
3. Run one live SOW review.
4. Send signature and kickoff invoice.
5. Confirm payment receipt.

Exit gate:

- Signed SOW + payment received + kickoff date set.

### Stage 3 — Kickoff and Security Controls

1. Create client engagement record.
2. Set communication channel and decision owner.
3. Classify sensitivity:
   - legal
   - financial
   - medical
   - IP/confidential
4. Configure secure storage path and access roles.
5. Register intake artifacts and source systems.
6. Lock baseline scope after intake complete.

Exit gate:

- Intake complete, access controlled, scope locked.

### Stage 4 — Delivery

1. Execute sprint plan.
2. Weekly updates to client:
   - work completed
   - risks/blockers
   - decisions needed
   - next week plan
3. Track requests:
   - in-scope -> schedule
   - out-of-scope -> change order
4. Enforce data placement:
   - source truth -> `recovery-core`
   - processing workflows -> `execution-*`
   - sanitized outputs -> `narrative-output`

Exit gate:

- Contracted deliverables drafted and internally reviewed.

### Stage 5 — Packaging and Readout

1. Build final package:
   - executive summary
   - deliverables index
   - decisions made
   - remaining risks
   - 30-day next action plan
2. Verify package against SOW line-by-line.
3. Redact sensitive non-required content.
4. Run executive readout.
5. Obtain written acceptance.

Exit gate:

- Written acceptance received.

### Stage 6 — Invoice, Payment, and Close

1. Send final milestone invoice same day as acceptance.
2. Follow-up rhythm:
   - Day 0 send
   - Day 3 reminder
   - Day 7 escalation reminder
   - Day 10 direct owner call
3. After payment clears:
   - release unrestricted final assets
   - send close memo
   - archive inactive materials
   - capture sanitized case proof

Exit gate:

- Funds received, closeout complete, project marked closed.

---

## 4) Payment Operations (Exact Setup Recommendation)

Use a simple two-lane payment stack:

1. **Stripe Payment Links / Invoices** (default)
   - card + ACH
   - clear invoice status
   - easy links for deposits/milestones
2. **Wire/ACH fallback instructions** for larger engagements

Implementation:

1. Create products in Stripe:
   - `Clarity Sprint Standard - $3,500`
   - `Clarity Sprint Fast-track - $5,000`
   - `Execution OS Build Sprint - custom invoice`
2. Create invoice templates:
   - kickoff deposit
   - midpoint milestone
   - final milestone
3. Add policy to SOW:
   - work starts only after initial payment clears
   - milestone delivery tied to milestone payment
   - late fees/escalation clause if applicable

---

## 5) Should You Add This to mjsdigitalstrategy.com?

Yes. Add it as a controlled consulting funnel, not a self-serve product.

Minimum pages:

1. Home (USP + CTA)
2. Offers (SKU A / SKU B with range pricing and outcomes)
3. Proof (sanitized case snapshots)
4. Security and process page (how consulting delivery works)
5. Book call page

Minimum CTAs:

- `Book a Fit Call`
- `Request Scope`
- `Pay Deposit` (private link after scope confirmation)

---

## 6) Should You Run a Simple Client Portal There?

Yes, but keep v1 minimal and consultant-operated.

Portal v1 scope:

1. Client dashboard:
   - stage
   - current milestone
   - next meeting
2. Shared status feed:
   - weekly updates
   - decisions needed
3. Deliverables list:
   - accepted outputs
   - pending approvals
4. Invoices:
   - issued
   - paid
   - outstanding
5. Secure file handoff links (no raw sensitive sprawl)

Portal v1 should NOT include:

- client self-configuration
- open-ended workflow editing
- broad document dumping

---

## 7) 14-Day Implementation Plan (Operator)

### Days 1-3

1. Finalize website copy from USP doc.
2. Publish Offer page with pricing ranges and outcomes.
3. Configure Stripe products + invoice templates.

### Days 4-7

1. Add fit call booking flow.
2. Add security/process explainer page.
3. Add internal rule: no kickoff before signed SOW + payment.

### Days 8-10

1. Launch client portal v1 pages:
   - status
   - deliverables
   - invoices
2. Connect weekly status template into portal update cadence.

### Days 11-14

1. Run first live client through full stage-gated workflow.
2. Capture friction notes.
3. Update templates and scripts.
4. Freeze v1 process for consistency.

---

## 8) Non-Negotiable Anti-Spin Rules

1. No work without signed SOW and cleared payment milestone.
2. No unapproved scope expansion.
3. No hidden work streams outside tracker.
4. No final unrestricted handoff before final payment.
5. No open project after closeout checklist is complete.

When stuck, ask:

1. What stage am I in?
2. What is the stage exit gate?
3. What single action gets me through that gate today?

