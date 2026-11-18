-- ============================================================================
-- Rollback da Migração Inicial do Dojo de Lógica
-- ATENÇÃO: remove todas as tabelas do Dojo e os dados salvos nelas.
-- ============================================================================

drop table if exists public.dojo_simulados cascade;
drop table if exists public.dojo_bugs cascade;
drop table if exists public.dojo_padroes cascade;
drop table if exists public.dojo_progresso cascade;
drop table if exists public.dojo_perfis cascade;

drop function if exists public.dojo_proteger_plano();
drop function if exists public.dojo_set_atualizado_em();
