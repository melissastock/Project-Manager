create table if not exists public.project_tickets (
  id text primary key,
  project text not null,
  title text not null,
  description text not null default '',
  state text not null default 'new',
  priority text not null default 'P2',
  owner text not null default '',
  lane text not null default '',
  scope_label text not null default 'pm-portal-only',
  due_date text not null default '',
  source text not null default 'pm-portal',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists project_tickets_project_state_idx
  on public.project_tickets (project, state, updated_at desc);

alter table public.project_tickets enable row level security;

drop policy if exists "project_tickets_select_anon" on public.project_tickets;
drop policy if exists "project_tickets_insert_anon" on public.project_tickets;
drop policy if exists "project_tickets_update_anon" on public.project_tickets;

create policy "project_tickets_select_anon"
  on public.project_tickets for select to anon using (true);

create policy "project_tickets_insert_anon"
  on public.project_tickets for insert to anon with check (true);

create policy "project_tickets_update_anon"
  on public.project_tickets for update to anon using (true) with check (true);
