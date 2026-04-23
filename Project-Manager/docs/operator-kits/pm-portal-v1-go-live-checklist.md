# PM-Portal V1 Go-Live Checklist (Within Days)

Use this to launch a consultant-operated client portal quickly without building extra product complexity.

This checklist assumes:

- public marketing/front door stays on `mjsdigitalstrategy.com`
- private delivery visibility runs through PM-portal
- sensitive source truth remains in `recovery-core`

---

## 1) V1 Scope Lock (Do Not Expand)

Ship only these 5 client-visible modules:

1. Client dashboard
2. Shared status feed
3. Deliverables list
4. Invoice tracker
5. Secure file handoff links

Anything outside this list goes to backlog after go-live.

---

## 2) Module Specs (Exact V1 Fields)

## A. Client Dashboard

Required fields:

- `client_name`
- `engagement_type` (`SKU-A` / `SKU-B`)
- `current_stage` (fit, scoped, active, readout, invoicing, closed)
- `current_milestone`
- `milestone_due_date`
- `next_meeting_datetime`
- `engagement_owner`

Client sees:

- stage
- current milestone
- next meeting

## B. Shared Status Feed

Required fields per update:

- `update_date`
- `week_label`
- `summary`
- `completed_items[]`
- `decisions_needed[]` (owner + due date)
- `risks_blockers[]`
- `next_week_plan[]`

Client sees:

- weekly updates
- decisions needed

## C. Deliverables List

Required fields per deliverable:

- `deliverable_name`
- `deliverable_type`
- `status` (`draft` / `pending_approval` / `accepted`)
- `owner`
- `date_shared`
- `date_accepted` (nullable)
- `notes`

Client sees:

- accepted outputs
- pending approvals

## D. Invoice Tracker

Required fields per invoice:

- `invoice_id`
- `milestone_label`
- `amount`
- `issued_date`
- `due_date`
- `status` (`issued` / `paid` / `outstanding`)
- `payment_link` (or reference)

Client sees:

- issued
- paid
- outstanding

## E. Secure File Handoff

Required fields per file handoff:

- `file_label`
- `data_class` (`financial` / `legal` / `medical` / `ip` / `ops`)
- `access_roles[]`
- `link_type` (`upload` / `download`)
- `expires_at`
- `checksum_required` (`true` / `false`)
- `audit_reference`

Client sees:

- active secure handoff links
- expiration notice

---

## 3) PM-Portal Endpoint Mapping (Use Existing Surface)

- Shared status + stage visibility:
  - use project agreement + project status records in portal workflows
- Deliverables/work tracking:
  - `/api/tickets` for deliverable cards and approval states
- Team/accountability:
  - `/api/team-assignments` for owner visibility
- Contract and scope lock:
  - `/api/client-agreements`
  - `/api/client-agreements/{id}/intake-complete`
  - change-order routes for post-lock scope edits
- Secure handoff:
  - `/api/secure-vault/files`
  - signed URL endpoints
  - checksum verification + audit endpoints

---

## 4) Payment Operations Model (V1)

Use external payment processor links (Stripe/QuickBooks) in v1 instead of custom gateway build.

Default payment terms:

- SKU A: 100% upfront before kickoff
- SKU B: 50% kickoff / 30% midpoint / 20% final handoff

Workflow:

1. Issue invoice same day milestone is reached.
2. Add invoice status row in portal.
3. Attach payment link.
4. Update to `paid` when funds clear.

Collection rhythm:

- Day 0: invoice sent
- Day 3: reminder
- Day 7: escalation reminder
- Day 10+: decision-owner call

---

## 5) Security Controls (V1 Non-Negotiables)

1. No raw sensitive file sharing over email attachments.
2. Use only secure-vault signed links for sensitive transfers.
3. Signed links must expire.
4. Role-limit links by client-approved access list.
5. Keep legal/financial source truth in `recovery-core` only.
6. No final editable handoff before final payment clears.

---

## 6) Go-Live-in-Days Plan

## Day 1: Configure + internal dry run

1. Confirm backend/frontend up and healthy.
2. Configure client agreement, ticket, and secure-vault flows.
3. Create one internal test project with all 5 modules populated.
4. Validate one upload and one download signed-link cycle.
5. Validate invoice status lifecycle (`issued` -> `paid`).

Exit criteria:

- all 5 modules render usable values
- secure transfer path validated end-to-end

## Day 2: First client pilot

1. Create client engagement record.
2. Publish dashboard summary and first weekly status feed entry.
3. Add current deliverables and approval states.
4. Add invoice row and payment link.
5. Send client portal walkthrough (15-minute call).

Exit criteria:

- client can access and understand all 5 modules
- first decisions and approvals captured through portal flow

## Day 3: Stabilize + standardize

1. Capture friction points from pilot.
2. Adjust labels/field naming for clarity.
3. Finalize your weekly operator cadence:
  - Monday: status update + dashboard refresh
  - Wednesday: blockers + decisions check
  - Friday: deliverable/invoice state reconciliation
4. Freeze v1 and move new asks to backlog.

Exit criteria:

- repeatable weekly operation with no ad hoc process changes

---

## 7) Client Walkthrough Script (15 Minutes)

1. "This portal is consultant-operated; you are not expected to manage tooling."
2. "Dashboard shows your stage, current milestone, and next meeting."
3. "Status feed shows progress and decisions we need from you."
4. "Deliverables list shows pending approvals and accepted outputs."
5. "Invoice tracker shows issued/paid/outstanding with payment links."
6. "Sensitive files are exchanged through secure time-limited links only."

Close with:

"Your role is to make decisions quickly; our role is to run the system."

---

## 8) Done Definition for V1 Launch

V1 is live when:

1. At least one active client is operating in portal flow.
2. Weekly status updates are sent from portal structure.
3. Deliverable approvals are tracked explicitly.
4. Invoice states are visible and reconciled weekly.
5. Sensitive file transfer uses secure-vault signed links only.