-- Configurações iniciais do PostgreSQL para o sistema de produtos
-- Este arquivo é executado automaticamente durante a inicialização do container

-- Configurar encoding e locale padrão
SET client_encoding = 'UTF8';
SET timezone = 'America/Sao_Paulo';

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Configurações de performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Aplicar configurações
SELECT pg_reload_conf();
