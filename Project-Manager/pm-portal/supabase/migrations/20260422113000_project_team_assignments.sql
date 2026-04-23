create table if not exists public.project_team_assignments (
  id text primary key,
  project text not null,
  role_key text not null,
  role_label text not null,
  raci_tags text[] not null default '{}',
  assignee_name text not null default '',
  assignee_type text not null default 'human',
  workstream text not null default '',
  narrative text not null default '',
  status text not null default 'proposed',
  approved_by text not null default '',
  approved_at timestamptz,
  approval_note text not null default '',
  source text not null default 'pm-portal',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create unique index if not exists project_team_assignments_project_role_key_idx
  on public.project_team_assignments (project, role_key);

alter table public.project_team_assignments enable row level security;

drop policy if exists "project_team_assignments_select_anon" on public.project_team_assignments;
drop policy if exists "project_team_assignments_insert_anon" on public.project_team_assignments;
drop policy if exists "project_team_assignments_update_anon" on public.project_team_assignments;

create policy "project_team_assignments_select_anon"
  on public.project_team_assignments for select to anon using (true);

create policy "project_team_assignments_insert_anon"
  on public.project_team_assignments for insert to anon with check (true);

create policy "project_team_assignments_update_anon"
  on public.project_team_assignments for update to anon using (true) with check (true);
