-- Starter governance/evidence tables for portal-scale operations.
-- Use this in your Postgres environment (for example Supabase SQL editor)
-- when you want auditable governance checks and release evidence records.

create table if not exists public.governance_checks (
  id bigint generated always as identity primary key,
  check_name text not null,
  scope_label text not null,
  target text not null,
  status text not null check (status in ('pass', 'fail', 'warn', 'skip')),
  details text not null default '',
  run_id text not null default '',
  source text not null default 'pm-governance-sweep',
  checked_at timestamptz not null default now()
);

create index if not exists governance_checks_checked_at_idx
  on public.governance_checks (checked_at desc);

create index if not exists governance_checks_target_idx
  on public.governance_checks (target, checked_at desc);

create table if not exists public.release_evidence (
  id bigint generated always as identity primary key,
  release_id text not null,
  project_name text not null,
  channel text not null check (channel in ('web', 'mobile', 'backend', 'portfolio')),
  artifact_type text not null,
  artifact_path text not null default '',
  ci_run_url text not null default '',
  reviewer text not null default '',
  decision text not null default '',
  notes text not null default '',
  recorded_at timestamptz not null default now()
);

create index if not exists release_evidence_release_idx
  on public.release_evidence (release_id, recorded_at desc);

create index if not exists release_evidence_project_idx
  on public.release_evidence (project_name, recorded_at desc);
