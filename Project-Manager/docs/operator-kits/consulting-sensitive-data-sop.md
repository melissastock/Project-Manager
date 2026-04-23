# Consulting SOP: Sensitive Client Data Handling

This SOP is for internal operator use while delivering consulting engagements. It is not a self-serve client workflow.

Use this when handling legal, financial, medical, HR, identity, or any other restricted client data.

## 1) Classification Before Intake (Mandatory)

Before receiving files, classify each data stream:

- `public`: safe for external sharing
- `internal`: restricted to consulting team
- `confidential`: limited to named roles, requires tracked access
- `restricted`: highest sensitivity, strict least-privilege + enhanced logging

If uncertain, classify as `restricted`.

## 2) Approved Storage Pattern (System of Record)

For consulting delivery, store by function:

1. **Source truth** -> `recovery-core`
   - Legal and financial source records only
   - No editing unless explicitly required and documented
2. **Execution artifacts** -> `execution-finance` / `execution-legal`
   - Working outputs, transformations, analysis artifacts
   - No duplicate source truth snapshots
3. **Client-facing sanitized outputs** -> `narrative-output`
   - No raw sensitive materials
4. **Control metadata and status** -> `Project-Manager`
   - Tracker state, scope, cadence, owner decisions

## 3) Intake Controls (Do This First)

Before any production work:

1. Confirm signed SOW/NDA and named client decision owner.
2. Confirm approved transfer channel (no ad hoc personal inbox transfer).
3. Create engagement data register with:
   - source
   - classification
   - owner
   - retention target
   - allowed roles
4. Register each sensitive file in controlled vault workflow (if PM-portal vault is in use, register first, then upload via signed URL).
5. Record checksum/hash for high-risk evidence bundles.

No intake-complete status until steps 1-5 are done.

## 4) Access Model (Least Privilege)

Use role-based access at minimum:

- Operator Lead: workflow control, no blanket raw-data rights by default
- Data Steward: source ingestion and verification authority
- Delivery Analyst: processed dataset access only unless explicitly approved
- Client Decision Owner: read access to approved deliverables

Rules:

- Grant minimum access required for current stage.
- Time-box elevated access.
- Revoke access at stage close or role change.
- Never share unrestricted links to restricted data.

## 5) Environment and Handling Rules

Mandatory handling controls:

1. Keep sensitive materials in approved storage only.
2. No local desktop copies unless explicitly approved and tracked.
3. No sensitive content in tickets, chat logs, or presentation drafts.
4. Use record IDs and references in working notes instead of raw payloads.
5. Encrypt in transit and at rest using platform defaults and managed keys.
6. Keep audit trails for access, upload, download, and mutation actions.

## 6) Processing Workflow (Consulting Team)

For each engagement:

1. Ingest -> validate completeness and integrity.
2. Normalize -> transform into analysis-ready format.
3. Reconcile -> resolve conflicts and missing data.
4. Analyze -> generate decision outputs.
5. Package -> produce sanitized client-facing deliverables.
6. Link -> attach references back to source records in `recovery-core`.

Do not move source truth into slide decks or narrative docs.

## 7) Client Reporting Rules (Security-Aware)

Client updates must include:

- what changed
- what decisions are pending
- what risks are open
- what controls were applied this cycle

Client updates must not include:

- full raw dumps
- unrestricted sensitive file links
- credentials, secrets, or personal identifiers unless contractually required and securely transmitted

## 8) Incident Response (If Data Exposure Risk Appears)

Trigger incident mode immediately if any unauthorized access, mistaken share, or uncertain exposure occurs.

1. Contain: revoke links/permissions and stop distribution.
2. Preserve: retain audit logs and event timeline.
3. Assess: determine data scope, affected records, and recipients.
4. Notify: follow contractual and legal notice obligations.
5. Remediate: rotate credentials, re-baseline permissions, document controls update.

No normal delivery resumes until containment is confirmed.

## 9) Retention, Closeout, and Archive

At project close:

1. Deliver final package (sanitized) and acceptance summary.
2. Confirm retention obligations per contract.
3. Archive inactive execution artifacts to `archive` if no longer operationally active.
4. Keep source-truth links and required records in `recovery-core`.
5. Revoke non-essential access across all systems.
6. Log closeout completion date and accountable owner.

## 10) Operator Checklist (Per Engagement)

- [ ] SOW/NDA verified
- [ ] Data classification complete
- [ ] Intake register complete
- [ ] Allowed roles approved
- [ ] Sensitive files registered and uploaded securely
- [ ] Hash/checksum captured where required
- [ ] Weekly control review completed
- [ ] Final package sanitized and approved
- [ ] Access revoked at close
- [ ] Retention + archive actions completed

