# Daily Client Ops Autopilot (Operator-Controlled)

This is the automation layer that tells you:

- where each client is in the project
- what you are waiting on
- what is overdue
- what to do next today
- what to prep for tomorrow

## What powers it

- Tracker data: `config/client-ops-tracker.json`
- Generator script: `scripts/generate_client_ops_brief.py`
- Runner script: `scripts/run_client_ops_brief.sh`
- Daily output: `docs/client-engagements/client-ops-daily-brief.md`

## Daily operating sequence (5 minutes)

1. Update `config/client-ops-tracker.json`:
   - stage per client (`1-8`)
   - current milestone
   - waiting-on items
   - task statuses and due dates
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
0 8 * * 1-5 cd /workspace/Project-Manager && /bin/bash scripts/run_client_ops_brief.sh
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

