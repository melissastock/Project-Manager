create table if not exists public.client_agreements (
  id text primary key,
  project text not null,
  client_name text not null,
  package_name text not null default '',
  product_brief text not null default '',
  scope_definition text not null default '',
  deliverables_summary text not null default '',
  pricing_model text not null default 'fixed',
  price_terms_json jsonb not null default '{}'::jsonb,
  agreement_status text not null default 'draft',
  is_locked boolean not null default false,
  locked_at timestamptz,
  locked_by text not null default '',
  lock_reason text not null default '',
  owner_role text not null default 'business_owner',
  neuro_worker_type text not null default 'unspecified',
  intake jsonb not null default '{}'::jsonb,
  deliverables jsonb not null default '[]'::jsonb,
  source text not null default 'pm-portal',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists client_agreements_project_idx
  on public.client_agreements (project);

create table if not exists public.agreement_messages (
  id text primary key,
  agreement_id text not null references public.client_agreements(id) on delete cascade,
  project text not null,
  author_name text not null,
  author_role text not null default 'client',
  message text not null,
  visibility text not null default 'client_and_team',
  created_at timestamptz not null default now()
);

create index if not exists agreement_messages_agreement_id_idx
  on public.agreement_messages (agreement_id, created_at);

create table if not exists public.agreement_change_orders (
  id text primary key,
  agreement_id text not null references public.client_agreements(id) on delete cascade,
  project text not null,
  requested_by text not null,
  requested_scope_delta text not null,
  requested_price_delta text not null default '',
  requested_timeline_delta text not null default '',
  status text not null default 'requested',
  approver text not null default '',
  decision_note text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists agreement_change_orders_agreement_id_idx
  on public.agreement_change_orders (agreement_id, created_at desc);

create table if not exists public.agreement_audit_events (
  id text primary key,
  agreement_id text not null references public.client_agreements(id) on delete cascade,
  project text not null,
  event_type text not null,
  actor text not null default '',
  actor_role text not null default '',
  details jsonb not null default '{}'::jsonb,
  data_class text not null default 'CONFIDENTIAL',
  created_at timestamptz not null default now()
);

create index if not exists agreement_audit_events_agreement_id_idx
  on public.agreement_audit_events (agreement_id, created_at);

alter table public.client_agreements enable row level security;
alter table public.agreement_messages enable row level security;
alter table public.agreement_change_orders enable row level security;
alter table public.agreement_audit_events enable row level security;

drop policy if exists "client_agreements_select_anon" on public.client_agreements;
drop policy if exists "client_agreements_insert_anon" on public.client_agreements;
drop policy if exists "client_agreements_update_anon" on public.client_agreements;
drop policy if exists "agreement_messages_select_anon" on public.agreement_messages;
drop policy if exists "agreement_messages_insert_anon" on public.agreement_messages;
drop policy if exists "agreement_change_orders_select_anon" on public.agreement_change_orders;
drop policy if exists "agreement_change_orders_insert_anon" on public.agreement_change_orders;
drop policy if exists "agreement_change_orders_update_anon" on public.agreement_change_orders;
drop policy if exists "agreement_audit_events_select_anon" on public.agreement_audit_events;
drop policy if exists "agreement_audit_events_insert_anon" on public.agreement_audit_events;

create policy "client_agreements_select_anon"
  on public.client_agreements for select to anon using (true);
create policy "client_agreements_insert_anon"
  on public.client_agreements for insert to anon with check (true);
create policy "client_agreements_update_anon"
  on public.client_agreements for update to anon using (true) with check (true);

create policy "agreement_messages_select_anon"
  on public.agreement_messages for select to anon using (true);
create policy "agreement_messages_insert_anon"
  on public.agreement_messages for insert to anon with check (true);

create policy "agreement_change_orders_select_anon"
  on public.agreement_change_orders for select to anon using (true);
create policy "agreement_change_orders_insert_anon"
  on public.agreement_change_orders for insert to anon with check (true);
create policy "agreement_change_orders_update_anon"
  on public.agreement_change_orders for update to anon using (true) with check (true);

create policy "agreement_audit_events_select_anon"
  on public.agreement_audit_events for select to anon using (true);
create policy "agreement_audit_events_insert_anon"
  on public.agreement_audit_events for insert to anon with check (true);
