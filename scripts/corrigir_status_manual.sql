-- MISSÃO: Correção Wizard - PASSO 1
-- Adicionar coluna 'status' à tabela agents
-- Executar no SQL Editor do Supabase

-- 1. Criar enum agent_status (se não existir)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'agent_status') THEN
        CREATE TYPE agent_status AS ENUM ('draft', 'active', 'paused', 'inactive');
        RAISE NOTICE 'Enum agent_status criado com sucesso';
    ELSE
        RAISE NOTICE 'Enum agent_status já existe';
    END IF;
END $$;

-- 2. Adicionar coluna status (se não existir)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'agents' AND column_name = 'status'
    ) THEN
        ALTER TABLE agents ADD COLUMN status agent_status DEFAULT 'draft';
        RAISE NOTICE 'Coluna status adicionada com sucesso';
    ELSE
        RAISE NOTICE 'Coluna status já existe';
    END IF;
END $$;

-- 3. Atualizar agentes existentes que têm status NULL
UPDATE agents SET status = 'draft' WHERE status IS NULL;

-- 4. Validação - Mostrar resultado
SELECT 
    'Validação' as tipo,
    COUNT(*) as total_agentes,
    COUNT(CASE WHEN status IS NOT NULL THEN 1 END) as com_status,
    COUNT(CASE WHEN status IS NULL THEN 1 END) as sem_status
FROM agents;

-- 5. Mostrar agentes com seus status
SELECT id, name, status, created_at 
FROM agents 
ORDER BY created_at DESC 
LIMIT 10;