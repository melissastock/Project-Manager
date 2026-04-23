# Daily Client Ops Autopilot (Operator-Controlled)

This is the automation layer that tells you:

- where each client is in the project
- what you are waiting on
- what is overdue
- what to do next today
- what to prep for tomorrow

## What powers it

- Tracker data: `config/client-ops-tracker.json`
- Optional PM-portal merge: `scripts/sync_client_ops_from_pm_portal.py` (tickets → `tasks[]`)
- Generator script: `scripts/generate_client_ops_brief.py`
- Runner script: `scripts/run_client_ops_brief.sh` (runs sync then brief)
- Daily output: `docs/client-engagements/client-ops-daily-brief.md`

## PM-portal sync (optional)

For each client entry you can enable automatic task import from PM-portal tickets.

1. In `config/client-ops-tracker.json`, add:

```json
"portal_sync": {
  "enabled": true,
  "portal_project": "MJS Financial Dash",
  "merge_blocked_as_waiting": true
}
```

- `portal_project` must match the **project** field on tickets in PM-portal (same string as in `config/repos.json` / portal UI).

2. Data source order (per client):

- **HTTP**: `GET {PM_PORTAL_URL}/api/tickets?project=<portal_project>` when the portal API is reachable.
- **Fallback**: `pm-portal/data/tickets.json` (local JSON cache used when Supabase is off).

3. Environment variables:

- `PM_PORTAL_URL` — default `http://127.0.0.1:8080` if unset.
- `SKIP_PORTAL_SYNC=1` — run only the brief generator (no HTTP / no merge).
- `FILE_ONLY_SYNC=1` — skip HTTP; merge from `pm-portal/data/tickets.json` only.

4. Manual sync (without running the full brief):

```bash
cd Project-Manager
python3 scripts/sync_client_ops_from_pm_portal.py
```

When sync runs, the brief includes a **PM-portal sync** line under each merged client (project, ticket count, source).

## Daily operating sequence (5 minutes)

1. Update `config/client-ops-tracker.json` for fields **not** supplied by the portal:
   - stage per client (`1-8`)
   - current milestone
   - next meeting
   - waiting-on items (manual dependencies; portal can append blocked-ticket rows if `merge_blocked_as_waiting` is true)
   - if `portal_sync` is off, also maintain task statuses and due dates
2. Run:

```bash
cd Project-Manager
./scripts/run_client_ops_brief.sh
```

3. Open:
   - `docs/client-engagements/client-ops-daily-brief.md`
4. Execute the **Today Command Queue** from top to bottom.

## Scheduler setup (optional, recommended)

Run automatically every weekday morning (08:00 local server time):

```bash
crontab -e
```

Add:

```cron
0 8 * * 1-5 cd /path/to/Project-Manager && /bin/bash scripts/run_client_ops_brief.sh
```

## Tracker rules (keep this strict)

1. Every active client must have:
   - `stage`
   - `current_milestone`
   - at least one open task with due date
2. Every waiting item must include:
   - owner
   - due date
   - impact statement
3. Task status vocabulary:
   - `todo`, `in_progress`, `blocked`, `awaiting`, `done`
4. No empty next action:
   - if no due tasks exist, create one dated next action immediately.

## Stage mapping used by automation

1. Qualification
2. Scope and close
3. Kickoff and controls
4. Delivery
5. Packaging
6. Readout/acceptance
7. Invoicing/collection
8. Closeout

## What this does NOT replace

- It does not replace client judgment or approvals.
- It does not replace secure-data SOP controls.
- It does not auto-send client updates; you still send your weekly packet.

It exists to stop drift and tell you the next highest-value action every day.

