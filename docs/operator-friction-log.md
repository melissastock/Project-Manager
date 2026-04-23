# Operator friction log

Purpose: capture recurring rough spots so collaborators (human or AI) can **preempt confusion**, use **plain-language steps**, and **verify outcomes** instead of assuming prior context.

Last updated: 2026-04-22

## Where this is referenced

- Root overview: `README.md` (intro + Notes).
- PM Portal setup and Supabase: `pm-portal/README.md`.
- New project onboarding: `docs/new-project-onboarding-checklist.md`.
- Intake form: `docs/new-project-intake-template.md`.
- Local env template: `pm-portal/backend/.env.example`.
- Conda GitHub Action: `.github/workflows/python-package-conda.yml` (header comment).
- PM standup workflow: `.github/workflows/pm-standup-loop.yml` (header comment).
- Portfolio execution queue and batch rules: `docs/portfolio-execution-queue.md`.

Add a link here when you create another “first stop” doc so the log stays discoverable.

---

## Git and GitHub

| Friction | What helps |
| --- | --- |
| Local vs remote / “do repos match?” | Separate **committed history** (compare `HEAD` to `origin/<branch>`) from **working tree** (modified / untracked files). PR **head SHA** on GitHub should match local `git rev-parse HEAD` when the branch is pushed. |
| What to stage / commit | Prefer **explicit file lists** or “everything except X” so nothing accidental lands in a commit (especially submodules with “untracked content”). |
| Root `.gitignore` uses `*` + allowlist | New root files (e.g. `environment.yml`, `.github/`) need **`!path`** entries or they look untrackable; `git add -f` works but fixing `.gitignore` is clearer long-term. |

---

## CI and environments

| Friction | What helps |
| --- | --- |
| Workflow runs on **`main`** but changes only on a **feature branch** | CI fails for “file not found” until the change is **on the branch the workflow runs against** (often `main`). Cherry-pick / merge, then push. |
| Conda / `environment.yml` | Keep **one canonical `environment.yml`**, valid YAML (empty `pip: []` instead of a lone `#` list item). |

---

## Supabase (portal + keys)

| Friction | What helps |
| --- | --- |
| **Which value is the API key** | Only from **Project Settings → API**: **`anon` `public`** (long JWT, usually starts with `eyJ`) or **`sb_publishable_...`**. Not a UUID, not “project ref” alone, not a random dashboard id. |
| **`SUPABASE_ANON_KEY` name vs `service_role`** | Variable says **anon** → use **anon** key for normal portal behavior (RLS applies). **`service_role`** bypasses RLS; reserve for tightly controlled server-only use, never browsers or chat. |
| **401 Invalid API key** | Check: **full** one-line paste, **no** truncated token, **URL host `ref`** matches JWT `ref` claim, key **not rotated** since copy. After any key paste in an insecure channel, **rotate** in the dashboard. |
| **Editor vs disk** | Cursor buffer can **differ from saved file**. After editing `.env`, **Save** (`⌘S`); verify with a **length / prefix** check (not pasting the secret) or hit **`/health/supabase`**. |
| **Supabase CLI** (`login`, `link`) | **`failed to scan line: expected newline`** → usually **non-interactive stdin** or bad paste into prompts. Use a real terminal + browser login, or **`SUPABASE_ACCESS_TOKEN`** for non-interactive link. |
| **CLI vs app** | **`supabase db push`** / migrations are optional if SQL was already run in the **SQL Editor**. App health is **`/health/supabase`** once `backend/.env` is correct. |

---

## Prisma (frontend workspace)

| Friction | What helps |
| --- | --- |
| **Prisma 7 vs Supabase `directUrl`** | This repo pins **Prisma 5** so `schema.prisma` can use `url` + `directUrl` exactly as Supabase documents. |
| **`.env` vs `.env.local`** | Prisma CLI loads **`.env`** by default. Put `DATABASE_URL` / `DIRECT_URL` in **`.env`** for `prisma migrate` / `generate`, or use a wrapper that loads `.env.local` first. Never prefix DB URLs with `VITE_`. |

## Running the PM portal backend

| Friction | What helps |
| --- | --- |
| **`Address already in use` (8080)** | Something is still bound: `lsof -nP -iTCP:8080 -sTCP:LISTEN` then `kill $(lsof -t -iTCP:8080)` (or use another `--port`). |
| **“Restart with new `.env`”** | **Stop** uvicorn (`Ctrl+C` or kill port), **start again** from `pm-portal/backend`; `--reload` only picks up **code** changes reliably—**env** changes need a **process restart**. |
| **Health checks** | **`GET /health`** (process up) and **`GET /health/supabase`** (credentials + table reachability). |

---

## Communication preferences (from sessions)

| Preference | What helps |
| --- | --- |
| Dense jargon / assumed sequencing | Use **numbered steps**, name **exact UI paths** (e.g. Supabase: *Settings → API*), and **one success criterion** per block (“you should see JSON with `status: ok`”). |
| “Done” / “Save” | Explicitly separate **IDE save**, **git commit**, and **deploy / restart** so nothing is ambiguous. |

---

## How to use this log

- When starting a similar task, **skim this file** and apply the workarounds first.
- After a painful session, add a **short new row** (friction + fix); keep it factual, not blame-oriented.
