# Client Delivery Tracking System (Operational + Client-Shareable)

Use this system to run every client engagement end-to-end with visibility, accountability, and fast closeout.

This tracking system is designed to:

1. keep you out of spin
2. show the client exactly where things stand
3. improve close rate and payment velocity

## 1) System Architecture

Run work in three synchronized layers:

1. **Internal operator board** (detailed control)
2. **Client-facing status packet** (clean summary)
3. **Milestone + payment ledger** (commercial control)

If all three are updated weekly, projects stay on rails.

## 2) Stage Model (Use As Canonical Pipeline)

Every project must be in one and only one stage:

1. `Lead Qualified`
2. `Scoped Offer Sent`
3. `SOW + Deposit Pending`
4. `Active Delivery`
5. `Final Package Ready`
6. `Client Acceptance Pending`
7. `Invoice Issued`
8. `Payment Received`
9. `Closed + Archived`

Rule: no custom stages unless you version this file.

## 3) Internal Operator Board Schema

Track each client engagement row with these fields:

- Client name
- Offer SKU (`SKU-A` or `SKU-B`)
- Current stage (from canonical stage list)
- Stage owner (single accountable owner)
- Current blocker
- Next milestone
- Milestone due date
- Acceptance criteria (for current stage)
- Invoice status (`not-issued`, `issued`, `partial`, `paid`, `overdue`)
- Payment due date
- Last client update sent date
- Next client update due date
- Risk severity (`low`, `medium`, `high`)
- Change-order required (`yes`/`no`)

## 4) Client-Facing Weekly Packet (Template)

Send this once per week on a fixed day.

Subject line:

`[Client Name] Weekly Execution Packet - Week of YYYY-MM-DD`

Body:

1. **Current stage**
   - Example: `Active Delivery`
2. **What was completed this week**
   - 3-5 bullet points
3. **Current blockers**
   - include owner and decision needed
4. **Decisions needed from client**
   - explicit owner + due date
5. **Next milestone**
   - milestone + exact date
6. **Commercial status**
   - invoice status + due date (if applicable)
7. **Confidence**
   - `green`, `yellow`, or `red`

## 5) Milestone Acceptance Template

Use this to close each stage before moving forward.

`Milestone:`
`Deliverables reviewed: yes/no`
`Acceptance decision: accepted / accepted-with-edits / pending`
`If pending, required edits + owner + due date:`
`Commercial trigger activated (invoice/change-order): yes/no`
`Next stage:`

No stage transition until this is filled.

## 6) Payment Control Workflow

Trigger points:

- Deposit invoice: immediately after SOW signature
- Final invoice: immediately after acceptance event

Follow-up cadence:

- `T+0` issue invoice
- `Due date` reminder
- `Due +3` reminder
- `Due +7` escalation note
- `Due +14` pause work / enforce terms

Rule: collections is a workflow, not an emotional conversation.

## 7) Project Closure Checklist

Project is only closed when all are complete:

- Final deliverable package sent
- Acceptance recorded
- Final invoice paid
- Handoff docs delivered
- Proof artifact extracted (client-safe)
- Inactive files moved to archive
- Closeout note logged

## 8) File and Data Routing Rules

- Legal/financial source truth -> `recovery-core`
- Workflow execution artifacts -> `execution-finance` / `execution-legal`
- Client-safe weekly packets + sanitized proof -> `narrative-output`
- Control docs + stage tracking -> `Project-Manager`
- Inactive engagement materials -> `archive`

## 9) Minimum Weekly Rhythm (Non-Negotiable)

Every week for every active client:

1. update internal board
2. send client packet
3. close/open milestones
4. reconcile invoice/payment status
5. escalate unresolved blockers

If this rhythm runs, engagements remain predictable and close faster.

