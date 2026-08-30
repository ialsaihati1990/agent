create table if not exists public.booth_state (
  id bigint primary key,
  payload jsonb not null default '{}'::jsonb
);
insert into public.booth_state(id,payload) values(1,'{}'::jsonb)
on conflict(id) do nothing;
