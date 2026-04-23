# PM-Portal Operator Kit

This kit is the operating manual for running delivery through `Project-Manager/pm-portal` as the control tower for active client work.

## 1) What PM-Portal Is For

PM-portal is the control layer for:

- client intake and agreement capture
- decision/risk visibility
- ticket and workflow tracking
- team assignment and approval
- secure vault registration and auditability

PM-portal is not the source of legal/financial truth. Truth remains in `recovery-core`; portal stores workflow state and execution metadata.

## 2) Environment Setup (One-Time)

From `Project-Manager/pm-portal`:

1. Backend setup
  - `cd backend`
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
  - `cp .env.example .env` and populate required keys
2. Frontend setup
  - `cd ../frontend`
  - `npm install`
  - `cp .env.example .env` if Prisma workflows are needed
3. Local run
  - backend: `uvicorn app.main:app --reload --port 8080`
  - frontend: `npm run dev`
4. Health check
  - open `http://localhost:8080/health/supabase`
  - confirm `status: ok` when Supabase keys are configured

## 3) Required Runtime Config

Minimum for Supabase-backed operations in backend `.env`:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`

For secure vault signed URL and protected-file workflows:

- `SUPABASE_SERVICE_ROLE_KEY`
- `SUPABASE_SECURE_VAULT_BUCKET` (default `secure-client-vault`)

If unset, some features fall back to local JSON (reduced governance fidelity).

## 4) Daily Operator Runbook

### Morning open (20-30 min)

1. Start backend + frontend.
2. Confirm health endpoint.
3. Review project list and runtime observations.
4. Process new client agreements and intake completion states.
5. Triage new tickets by:
  - state (`new` -> `triaged`)
  - priority (`P0`..`P3`)
  - owner assignment
6. Review secure-vault events and unresolved checksum/verifications.

### Midday control check (10-15 min)

1. Identify blocked tickets and aging items.
2. Ensure one owner per active project lane.
3. Confirm no intake-locked agreement has direct scope edits (use change orders only).

### End-of-day close (20 min)

1. Move completed tickets to `done`.
2. Post project-level status note in your client update channel.
3. Log decisions and unresolved risks.
4. Confirm tomorrow's top 3 deliverables per active project.

## 5) Weekly Operator Cadence

Run once per week per active client:

1. **Agreement integrity**
  - validate accepted scope/package and lock status
  - review all approved/rejected change orders
2. **Execution throughput**
  - ticket cycle review (created vs done)
  - blockers by category (data, legal, integration, owner availability)
3. **Governance and trust**
  - team assignment approval status
  - secure-vault access/audit anomalies
  - unresolved high-severity risks
4. **Decision packet update**
  - summarize what changed
  - rank next actions
  - link outputs in `execution-`* and truth references in `recovery-core`

## 6) Core Endpoints To Use Operationally

Primary workflows (from existing PM-portal API surface):

- Tickets:
  - `GET /api/tickets`
  - `POST /api/tickets`
  - `PATCH /api/tickets/{ticket_id}`
- Team assignments:
  - `GET /api/team-assignments`
  - `PATCH /api/team-assignments/{project_name}/{role_key}`
  - `POST /api/team-assignments/{project_name}/approve`
- Client agreements:
  - `GET /api/client-agreements`
  - `POST /api/client-agreements`
  - `POST /api/client-agreements/{agreement_id}/intake-complete`
  - change-order routes for post-lock scope/pricing changes
- Secure vault:
  - file registration
  - signed upload/download URL issuance
  - checksum verification
  - vault audit retrieval

## 7) PM-Portal Intake Standard (Per New Client)

Before work starts:

1. Create agreement record with package, scope, timeline, and owner.
2. Verify required data access.
3. Register initial sensitive artifacts in secure vault if needed.
4. Open initial ticket set:
  - discovery/intake
  - workflow map
  - risk register
  - decision packet
5. Assign roles and capture approval.
6. Mark intake complete to lock core fields.

## 8) Guardrails (Non-Negotiable)

1. No direct scope/price edits after intake lock; use change orders.
2. No raw sensitive file sprawl outside vault workflows.
3. No "orphan" tickets (every active ticket has owner + due date).
4. No unresolved P0/P1 risk carried into weekly close without escalation note.
5. PM-portal records workflow/control data; legal/financial truth remains in `recovery-core`.

## 9) KPIs To Track

Track these weekly per client:

- Intake completion lead time
- Ticket cycle time (triaged -> done)
- Blocked ticket count (> 48h)
- Agreement change-order rate
- Decision packet on-time rate
- Secure-vault verification completion rate

## 10) PM-Portal Incident Playbook

If portal instability appears:

1. Check backend health endpoint.
2. Validate `.env` keys and restart backend.
3. Confirm Supabase connectivity and table availability.
4. Fall back to local JSON mode only for temporary continuity.
5. Log incident and reconciliation actions in operator notes.

## 11) Roles And Ownership Model

- Operator lead: owns cadence, triage, and readiness
- Delivery owner: owns output completion quality
- Data steward: owns source integrity and vault handling
- Decision owner: client-side authority for approvals

Keep one accountable owner per role per active client.