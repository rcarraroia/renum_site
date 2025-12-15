-- Migration 010: Migrate Sub-Agents to Agents
-- Sprint 09 - Fase B
-- Data: 2025-12-06
-- Objetivo: Migrar 12 registros existentes de sub_agents para agents e alterar estrutura

-- ============================================================================
-- PARTE 1: MIGRAR DADOS DE SUB_AGENTS PARA AGENTS
-- ============================================================================

-- Copiar registros de sub_agents para agents
-- Apenas registros que têm client_id (os 12 existentes)
-- Mapear 'site' para 'web' para compatibilidade com constraint
INSERT INTO agents (
    id,
    client_id,
    name,
    description,
    slug,
    model,
    system_prompt,
    channel,
    template_type,
    status,
    is_public,
    public_url,
    config,
    access_count,
    created_at,
    updated_at
)
SELECT 
    id,
    client_id,
    name,
    description,
    slug,
    model,
    system_prompt,
    CASE 
        WHEN channel = 'site' THEN 'web'
        ELSE channel
    END as channel,
    template_type,
    status,
    is_public,
    public_url,
    config,
    access_count,
    created_at,
    updated_at
FROM sub_agents
WHERE client_id IS NOT NULL;

-- Verificar quantos registros foram copiados
DO $$
DECLARE
    agents_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO agents_count FROM agents;
    RAISE NOTICE '✅ % registros copiados para agents', agents_count;
END $$;

-- ============================================================================
-- PARTE 2: LIMPAR SUB_AGENTS (DELETAR REGISTROS MIGRADOS)
-- ============================================================================

-- Deletar registros que foram migrados para agents
DELETE FROM sub_agents WHERE client_id IS NOT NULL;

-- Verificar quantos registros restam
DO $$
DECLARE
    remaining_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO remaining_count FROM sub_agents;
    RAISE NOTICE '✅ % registros restantes em sub_agents', remaining_count;
END $$;

-- ============================================================================
-- PARTE 3: ADICIONAR COLUNA agent_id EM SUB_AGENTS
-- ============================================================================

-- Adicionar coluna agent_id (nullable por enquanto)
ALTER TABLE sub_agents ADD COLUMN IF NOT EXISTS agent_id UUID;

-- Criar FK para agents
ALTER TABLE sub_agents 
    ADD CONSTRAINT fk_sub_agents_agent_id 
    FOREIGN KEY (agent_id) 
    REFERENCES agents(id) 
    ON DELETE CASCADE;

DO $$
BEGIN
    RAISE NOTICE '✅ Coluna agent_id adicionada em sub_agents';
END $$;

-- ============================================================================
-- PARTE 4: REMOVER COLUNA client_id DE SUB_AGENTS
-- ============================================================================

-- Remover FK antiga (se existir)
ALTER TABLE sub_agents DROP CONSTRAINT IF EXISTS fk_sub_agents_client_id;
ALTER TABLE sub_agents DROP CONSTRAINT IF EXISTS sub_agents_client_id_fkey;

-- Remover coluna client_id
ALTER TABLE sub_agents DROP COLUMN IF EXISTS client_id;

DO $$
BEGIN
    RAISE NOTICE '✅ Coluna client_id removida de sub_agents';
END $$;

-- ============================================================================
-- PARTE 5: MANTER agent_id NULLABLE
-- ============================================================================

-- NÃO tornar agent_id obrigatório porque há 2 registros sem client_id
-- que permanecerão em sub_agents sem agent_id (são sub-agents "órfãos")
-- Futuramente, quando todos sub-agents tiverem agent_id, podemos tornar NOT NULL

DO $$
DECLARE
    orphan_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO orphan_count FROM sub_agents WHERE agent_id IS NULL;
    RAISE NOTICE '⚠️  % sub-agents sem agent_id (órfãos)', orphan_count;
    RAISE NOTICE '✅ Coluna agent_id permanece NULLABLE';
END $$;

-- ============================================================================
-- PARTE 6: RECRIAR ÍNDICES
-- ============================================================================

-- Remover índice antigo de client_id (se existir)
DROP INDEX IF EXISTS idx_sub_agents_client_id;

-- Criar índice para agent_id
CREATE INDEX IF NOT EXISTS idx_sub_agents_agent_id ON sub_agents(agent_id);

-- Índice composto para queries comuns
CREATE INDEX IF NOT EXISTS idx_sub_agents_agent_active ON sub_agents(agent_id, is_active);

DO $$
BEGIN
    RAISE NOTICE '✅ Índices recriados';
END $$;

-- ============================================================================
-- PARTE 7: ATUALIZAR RLS POLICIES
-- ============================================================================

-- Remover políticas antigas baseadas em client_id
DROP POLICY IF EXISTS "Clients can view own sub_agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can view own sub-agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can create own sub_agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can update own sub_agents" ON sub_agents;
DROP POLICY IF EXISTS "Clients can delete own sub_agents" ON sub_agents;

-- Remover política de admins se existir (para recriar)
DROP POLICY IF EXISTS "Admins have full access to sub_agents" ON sub_agents;

-- Criar novas políticas baseadas em agent_id

-- Política 1: Admins têm acesso total
CREATE POLICY "Admins have full access to sub_agents"
    ON sub_agents
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Política 2: Users podem ver sub_agents de seus agents
CREATE POLICY "Users can view sub_agents of their agents"
    ON sub_agents
    FOR SELECT
    TO authenticated
    USING (
        agent_id IN (
            SELECT id FROM agents
            WHERE client_id IN (
                SELECT id FROM clients
                WHERE clients.id = (
                    SELECT client_id FROM profiles 
                    WHERE profiles.id = auth.uid()
                )
            )
        )
    );

-- Política 3: Users podem criar sub_agents para seus agents
CREATE POLICY "Users can create sub_agents for their agents"
    ON sub_agents
    FOR INSERT
    TO authenticated
    WITH CHECK (
        agent_id IN (
            SELECT id FROM agents
            WHERE client_id IN (
                SELECT id FROM clients
                WHERE clients.id = (
                    SELECT client_id FROM profiles 
                    WHERE profiles.id = auth.uid()
                )
            )
        )
    );

-- Política 4: Users podem atualizar sub_agents de seus agents
CREATE POLICY "Users can update sub_agents of their agents"
    ON sub_agents
    FOR UPDATE
    TO authenticated
    USING (
        agent_id IN (
            SELECT id FROM agents
            WHERE client_id IN (
                SELECT id FROM clients
                WHERE clients.id = (
                    SELECT client_id FROM profiles 
                    WHERE profiles.id = auth.uid()
                )
            )
        )
    );

-- Política 5: Users podem deletar sub_agents de seus agents
CREATE POLICY "Users can delete sub_agents of their agents"
    ON sub_agents
    FOR DELETE
    TO authenticated
    USING (
        agent_id IN (
            SELECT id FROM agents
            WHERE client_id IN (
                SELECT id FROM clients
                WHERE clients.id = (
                    SELECT client_id FROM profiles 
                    WHERE profiles.id = auth.uid()
                )
            )
        )
    );

DO $$
BEGIN
    RAISE NOTICE '✅ Políticas RLS atualizadas';
END $$;

-- ============================================================================
-- PARTE 8: ATUALIZAR COMMENTS
-- ============================================================================

COMMENT ON COLUMN sub_agents.agent_id IS 'Agent principal ao qual este sub-agent pertence';

-- ============================================================================
-- VERIFICAÇÃO FINAL
-- ============================================================================

DO $$
DECLARE
    agents_count INTEGER;
    sub_agents_count INTEGER;
    has_agent_id BOOLEAN;
    has_client_id BOOLEAN;
BEGIN
    -- Contar agents
    SELECT COUNT(*) INTO agents_count FROM agents;
    
    -- Contar sub_agents
    SELECT COUNT(*) INTO sub_agents_count FROM sub_agents;
    
    -- Verificar se agent_id existe
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'sub_agents' AND column_name = 'agent_id'
    ) INTO has_agent_id;
    
    -- Verificar se client_id foi removido
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'sub_agents' AND column_name = 'client_id'
    ) INTO has_client_id;
    
    RAISE NOTICE '';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'VERIFICAÇÃO FINAL';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Agents criados: %', agents_count;
    RAISE NOTICE 'Sub-agents restantes: %', sub_agents_count;
    RAISE NOTICE 'Sub-agents tem agent_id: %', has_agent_id;
    RAISE NOTICE 'Sub-agents tem client_id: %', has_client_id;
    RAISE NOTICE '========================================';
    
    IF agents_count = 0 THEN
        RAISE EXCEPTION '❌ Nenhum agent foi criado!';
    END IF;
    
    IF NOT has_agent_id THEN
        RAISE EXCEPTION '❌ Coluna agent_id não existe em sub_agents!';
    END IF;
    
    IF has_client_id THEN
        RAISE EXCEPTION '❌ Coluna client_id ainda existe em sub_agents!';
    END IF;
    
    RAISE NOTICE '✅ Migration 010 concluída com sucesso!';
END $$;
