# PM Portal

Phase 1 dedicated portal for project readiness intelligence.

**Stuck on Supabase keys, `.env` not “taking”, port 8080 busy, or CLI scan errors?** See the portfolio log: [`docs/operator-friction-log.md`](../docs/operator-friction-log.md) (repo root).

## Stack
- Backend: FastAPI (`backend/`)
- Frontend: React + Vite (`frontend/`)
- ORM (optional, frontend workspace): **Prisma 5** + PostgreSQL (`frontend/prisma/`) for typed access to Supabase Postgres (pooled `DATABASE_URL` + `DIRECT_URL` for migrations). Do **not** import `PrismaClient` in browser bundles—use it from Node scripts, a server, or future API routes only.

## Prisma + Supabase Postgres (`frontend/`)

1. `cd frontend && npm install` (installs `prisma` and `@prisma/client`).
2. Copy **`.env.example`** to **`.env`** (Prisma CLI reads `.env` by default). Optionally also copy the same keys to **`.env.local`** for Vite-only vars—**never** expose `DATABASE_URL` / `DIRECT_URL` as `VITE_*` variables.
3. Replace placeholders using **Supabase → Project Settings → Database → Connection string** (URI). Pooler host and region are **project-specific**; do not assume a region.
4. `npm run prisma:generate` — generates the client into `node_modules/@prisma/client`.
5. `npm run prisma:migrate` — creates/applies migrations (uses `DIRECT_URL`).

Starter model: `RecommendationDecision` maps to `public.recommendation_decisions` (same table as the FastAPI portal uses via PostgREST).

### Optional: Supabase agent skills

Interactive installer (pick skills with space / enter):

```bash
cd frontend
npx skills add supabase/agent-skills
```

To skip prompts when supported: `npx skills add supabase/agent-skills --yes` (see `skills --help`).

## Quickstart
1. Backend:
   - `cd backend`
   - `python3 -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
   - Copy `backend/.env.example` to `backend/.env` and fill in Supabase (see below), or omit keys to use local `data/decisions.json` only.
   - `uvicorn app.main:app --reload --port 8080`
2. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

Set `VITE_API_BASE_URL` if backend is not `http://localhost:8080`.

## Supabase (decisions + runtime observations)

1. Ensure `recommendation_decisions` exists (decision state persistence).
2. Add `project_runtime_observations` so runtime repo visibility can be compared across environments:

```sql
create table if not exists public.project_runtime_observations (
  id bigint generated always as identity primary key,
  project_name text not null,
  project_path text not null,
  intake_stage text not null default '',
  registry_status text not null default 'registered',
  runtime_status text not null,
  runtime_note text not null default '',
  exists boolean not null default false,
  is_git_repo boolean not null default false,
  branch text not null default '',
  head text not null default '',
  summary text not null default '',
  source text not null default 'pm-portal-backend',
  observed_at timestamptz not null default now()
);
```
2. **Project Settings** → **API**: copy **Project URL** and **anon public** key into `backend/.env` as `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
3. **Save** `backend/.env`, **restart** the API (reload alone may not reload env), then open `http://localhost:8080/health/supabase` — `status` should be `ok`. If it is `error`, read `detail` and cross-check [`docs/operator-friction-log.md`](../docs/operator-friction-log.md) (keys, rotation, URL vs JWT `ref`).

When those variables are unset, the portal keeps working using `data/decisions.json` under the portal root.

## Ticketing API (Phase 1)

PM Portal now includes internal ticket lifecycle endpoints (works with local JSON fallback and can use Supabase table `project_tickets` when available):

- `GET /api/tickets?project=<name>&state=<state>`
- `POST /api/tickets`
- `PATCH /api/tickets/{ticket_id}`

`project_tickets` migration is included under:

- `supabase/migrations/20260422103000_project_tickets.sql`

Columns:

- `id` (primary key)
- `project`
- `title`
- `description`
- `state` (`new|triaged|in_progress|blocked|done|deferred`)
- `priority` (`P0|P1|P2|P3`)
- `owner`
- `lane`
- `scope_label` (`all-repos|selected-lanes|pm-portal-only`)
- `due_date`
- `source`
- `created_at`
- `updated_at`

## Team assignments + human approval

Portal now reports team structure directly in each project detail view so operators can see exactly who is carrying each workstream and approve the team composition.

API:

- `GET /api/team-assignments?project=<name>`
- `PATCH /api/team-assignments/{project_name}/{role_key}`
- `POST /api/team-assignments/{project_name}/approve`

Supabase migration:

- `supabase/migrations/20260422113000_project_team_assignments.sql`

This table stores role cards, RACI tags, assignee details, and owner approval metadata (`status`, `approved_by`, `approved_at`, `approval_note`) for transparent governance and trust.

## Supabase CLI (optional)

From the `pm-portal` directory, after [installing the Supabase CLI](https://supabase.com/docs/guides/cli):

1. `supabase login` — opens a browser; completes account access for the CLI.
2. `supabase link --project-ref <ref>` — `<ref>` is the subdomain in `https://<ref>.supabase.co`.
3. `supabase db push` — applies migrations under `supabase/migrations/` to the linked project (includes `recommendation_decisions`).

`supabase init` has already been run here, so you only need login + link on your machine, then `db push` when you want schema changes applied remotely.

If the CLI prints **`failed to scan line: expected newline`**, it is usually **interactive input** (not a bad SQL file): run `supabase login` / `supabase link` in a normal terminal window, complete the browser login, and answer prompts **one line at a time**—do not paste multi-line text into password prompts. Alternatively set a one-line **`SUPABASE_ACCESS_TOKEN`** from your Supabase account (Dashboard → Account → Access Tokens) in the environment before `supabase link`.

## Mobile store governance (Apple + Android)

For compliance before mobile submission, use:

- Policy guide: `docs/mobile-compliance-governance.md`
- Machine-readable gate config: `backend/config/mobile-compliance-governance.json`
- Privacy/disclosure copy (mobile-adapted from website governance): `docs/mobile-privacy-and-disclosures.md`
- Machine-readable store disclosures: `backend/config/mobile-store-disclosures.json`

This governance separates shared controls (privacy/security/data handling) from platform-specific release gates for App Store and Google Play.
