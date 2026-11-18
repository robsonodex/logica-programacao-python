-- ============================================================================
-- Dojo de Lógica — Migração Inicial (Supabase / PostgreSQL)
-- Projeto alvo: logica-programacao-python (afqxpeqdtupzzmjijwix)
-- Executar no SQL Editor do Supabase. Script idempotente.
-- ============================================================================

create extension if not exists pgcrypto;

-- Função genérica de timestamp atualizado_em
create or replace function public.dojo_set_atualizado_em()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  new.atualizado_em = now();
  return new;
end;
$$;

-- Protege a coluna `plano` contra auto-upgrade pelo cliente (pronto para monetização SaaS)
create or replace function public.dojo_proteger_plano()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  if current_setting('request.jwt.claim.role', true) <> 'service_role' then
    if tg_op = 'INSERT' then
      new.plano = 'free';
    elsif tg_op = 'UPDATE' and new.plano is distinct from old.plano then
      new.plano = old.plano;
    end if;
  end if;
  return new;
end;
$$;

-- 1. Perfis de alunos (base multiusuário / planos futuros)
create table if not exists public.dojo_perfis (
  user_id uuid primary key references auth.users(id) on delete cascade,
  nome text default '',
  plano text not null default 'free' check (plano in ('free', 'pro', 'enterprise')),
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now()
);

drop trigger if exists trg_dojo_perfis_updated on public.dojo_perfis;
create trigger trg_dojo_perfis_updated
  before update on public.dojo_perfis
  for each row execute function public.dojo_set_atualizado_em();

drop trigger if exists trg_dojo_perfis_plano on public.dojo_perfis;
create trigger trg_dojo_perfis_plano
  before insert or update on public.dojo_perfis
  for each row execute function public.dojo_proteger_plano();

-- 2. Progresso completo sincronizado (fonte de verdade na nuvem)
create table if not exists public.dojo_progresso (
  user_id uuid primary key references auth.users(id) on delete cascade,
  dados jsonb not null default '{}'::jsonb,
  versao int not null default 1,
  xp int not null default 0,
  estagio_atual int not null default 1,
  estagio_max int not null default 1,
  atualizado_em timestamptz not null default now()
);

drop trigger if exists trg_dojo_progresso_updated on public.dojo_progresso;
create trigger trg_dojo_progresso_updated
  before update on public.dojo_progresso
  for each row execute function public.dojo_set_atualizado_em();

-- 3. Caderno de Padrões Mentais (Pensar Antes de Codar + Feynman)
create table if not exists public.dojo_padroes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  questao_id text not null,
  modelo_id text not null,
  titulo text not null,
  estagio int not null,
  contrato text not null default '',
  edge_cases text not null default '',
  plano text not null default '',
  feynman text not null default '',
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now(),
  unique (user_id, questao_id)
);

create index if not exists idx_dojo_padroes_user_estagio
  on public.dojo_padroes (user_id, estagio, atualizado_em desc);

drop trigger if exists trg_dojo_padroes_updated on public.dojo_padroes;
create trigger trg_dojo_padroes_updated
  before update on public.dojo_padroes
  for each row execute function public.dojo_set_atualizado_em();

-- 4. Museu dos Meus Bugs (histórico classificado de falhas)
create table if not exists public.dojo_bugs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  categoria text not null,
  tipo_erro text not null default '',
  modelo_id text not null default '',
  estagio int not null default 1,
  detalhe text not null default '',
  criado_em timestamptz not null default now()
);

create index if not exists idx_dojo_bugs_user_cat
  on public.dojo_bugs (user_id, categoria, criado_em desc);

-- 5. Simulados de Entrevista Técnica
create table if not exists public.dojo_simulados (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  simulado_local_id text not null,
  trilha text not null,
  duracao_seg int not null default 0,
  nota_geral int not null default 0,
  nota_correcao int not null default 0,
  nota_eficiencia int not null default 0,
  nota_qualidade int not null default 0,
  nota_edge_cases int not null default 0,
  veredito text not null default '',
  resumo jsonb not null default '{}'::jsonb,
  criado_em timestamptz not null default now(),
  unique (user_id, simulado_local_id)
);

create index if not exists idx_dojo_simulados_user_data
  on public.dojo_simulados (user_id, criado_em desc);

-- ============================================================================
-- Row Level Security (RLS) — isolamento estrito por usuário autenticado
-- ============================================================================

alter table public.dojo_perfis enable row level security;
alter table public.dojo_progresso enable row level security;
alter table public.dojo_padroes enable row level security;
alter table public.dojo_bugs enable row level security;
alter table public.dojo_simulados enable row level security;

-- Policies: dojo_perfis
drop policy if exists "dojo_perfis_select_own" on public.dojo_perfis;
create policy "dojo_perfis_select_own" on public.dojo_perfis
  for select using ((select auth.uid()) = user_id);

drop policy if exists "dojo_perfis_insert_own" on public.dojo_perfis;
create policy "dojo_perfis_insert_own" on public.dojo_perfis
  for insert with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_perfis_update_own" on public.dojo_perfis;
create policy "dojo_perfis_update_own" on public.dojo_perfis
  for update using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

-- Policies: dojo_progresso
drop policy if exists "dojo_progresso_select_own" on public.dojo_progresso;
create policy "dojo_progresso_select_own" on public.dojo_progresso
  for select using ((select auth.uid()) = user_id);

drop policy if exists "dojo_progresso_insert_own" on public.dojo_progresso;
create policy "dojo_progresso_insert_own" on public.dojo_progresso
  for insert with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_progresso_update_own" on public.dojo_progresso;
create policy "dojo_progresso_update_own" on public.dojo_progresso
  for update using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_progresso_delete_own" on public.dojo_progresso;
create policy "dojo_progresso_delete_own" on public.dojo_progresso
  for delete using ((select auth.uid()) = user_id);

-- Policies: dojo_padroes
drop policy if exists "dojo_padroes_select_own" on public.dojo_padroes;
create policy "dojo_padroes_select_own" on public.dojo_padroes
  for select using ((select auth.uid()) = user_id);

drop policy if exists "dojo_padroes_insert_own" on public.dojo_padroes;
create policy "dojo_padroes_insert_own" on public.dojo_padroes
  for insert with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_padroes_update_own" on public.dojo_padroes;
create policy "dojo_padroes_update_own" on public.dojo_padroes
  for update using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_padroes_delete_own" on public.dojo_padroes;
create policy "dojo_padroes_delete_own" on public.dojo_padroes
  for delete using ((select auth.uid()) = user_id);

-- Policies: dojo_bugs
drop policy if exists "dojo_bugs_select_own" on public.dojo_bugs;
create policy "dojo_bugs_select_own" on public.dojo_bugs
  for select using ((select auth.uid()) = user_id);

drop policy if exists "dojo_bugs_insert_own" on public.dojo_bugs;
create policy "dojo_bugs_insert_own" on public.dojo_bugs
  for insert with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_bugs_delete_own" on public.dojo_bugs;
create policy "dojo_bugs_delete_own" on public.dojo_bugs
  for delete using ((select auth.uid()) = user_id);

-- Policies: dojo_simulados
drop policy if exists "dojo_simulados_select_own" on public.dojo_simulados;
create policy "dojo_simulados_select_own" on public.dojo_simulados
  for select using ((select auth.uid()) = user_id);

drop policy if exists "dojo_simulados_insert_own" on public.dojo_simulados;
create policy "dojo_simulados_insert_own" on public.dojo_simulados
  for insert with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_simulados_update_own" on public.dojo_simulados;
create policy "dojo_simulados_update_own" on public.dojo_simulados
  for update using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

drop policy if exists "dojo_simulados_delete_own" on public.dojo_simulados;
create policy "dojo_simulados_delete_own" on public.dojo_simulados
  for delete using ((select auth.uid()) = user_id);
