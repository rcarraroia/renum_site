-- Migration 009: Create Agents Table
-- Sprint 09 - Fase A
-- Data: 2025-12-06
-- Objetivo: Criar tabela agents para armazenar agentes principais criados via Wizard

-- ============================================================================
-- 1. CREATE TABLE agents
-- ============================================================================

CREATE TABLE IF NOT EXISTS agents (
    -- Identificação
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Informações Básicas
    name TEXT NOT NULL,
    description TEXT,
    slug TEXT UNIQUE NOT NULL,
    
    -- Configuração
    model TEXT NOT NULL DEFAULT 'gpt-4o-mini',
    system_prompt TEXT NOT NULL,
    channel TEXT NOT NULL DEFAULT 'whatsapp',
    template_type TEXT,
    
    -- Status e Publicação
    status TEXT NOT NULL DEFAULT 'draft', -- draft, active, inactive
    is_public BOOLEAN DEFAULT FALSE,
    public_url TEXT,
    
    -- Dados do Wizard (armazena config de todos os steps)
    config JSONB DEFAULT '{}',
    
    -- Métricas
    access_count INTEGER DEFAULT 0,
    
    -- Auditoria
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    
    -- Constraints
    CONSTRAINT agents_status_check CHECK (status IN ('draft', 'active', 'inactive')),
    CONSTRAINT agents_channel_check CHECK (channel IN ('whatsapp', 'web', 'sms', 'email')),
    CONSTRAINT agents_model_check CHECK (model IN ('gpt-4', 'gpt-4-turbo-preview', 'gpt-4o-mini', 'claude-3-5-sonnet-20241022', 'claude-3-opus'))
);

-- ============================================================================
-- 2. CREATE INDEXES
-- ============================================================================

-- Índice para buscar agents por client
CREATE INDEX idx_agents_client_id ON agents(client_id);

-- Índice para filtrar por status
CREATE INDEX idx_agents_status ON agents(status);

-- Índice para buscar por slug (já é UNIQUE, mas explícito para performance)
CREATE INDEX idx_agents_slug ON agents(slug);

-- Índice para filtrar agents públicos
CREATE INDEX idx_agents_is_public ON agents(is_public);

-- Índice composto para queries comuns (client + status)
CREATE INDEX idx_agents_client_status ON agents(client_id, status);

-- ============================================================================
-- 3. ENABLE ROW LEVEL SECURITY (RLS)
-- ============================================================================

ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 4. CREATE RLS POLICIES
-- ============================================================================

-- Política 1: Admins têm acesso total
CREATE POLICY "Admins have full access to agents"
    ON agents
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Política 2: Clients podem ver apenas seus próprios agents
CREATE POLICY "Clients can view own agents"
    ON agents
    FOR SELECT
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE clients.id = (
                SELECT client_id FROM profiles 
                WHERE profiles.id = auth.uid()
            )
        )
    );

-- Política 3: Clients podem criar agents para si mesmos
CREATE POLICY "Clients can create own agents"
    ON agents
    FOR INSERT
    TO authenticated
    WITH CHECK (
        client_id IN (
            SELECT id FROM clients
            WHERE clients.id = (
                SELECT client_id FROM profiles 
                WHERE profiles.id = auth.uid()
            )
        )
    );

-- Política 4: Clients podem atualizar seus próprios agents
CREATE POLICY "Clients can update own agents"
    ON agents
    FOR UPDATE
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE clients.id = (
                SELECT client_id FROM profiles 
                WHERE profiles.id = auth.uid()
            )
        )
    );

-- Política 5: Clients podem deletar seus próprios agents
CREATE POLICY "Clients can delete own agents"
    ON agents
    FOR DELETE
    TO authenticated
    USING (
        client_id IN (
            SELECT id FROM clients
            WHERE clients.id = (
                SELECT client_id FROM profiles 
                WHERE profiles.id = auth.uid()
            )
        )
    );

-- Política 6: Agents públicos podem ser vistos por qualquer um autenticado
CREATE POLICY "Public agents are visible to all authenticated users"
    ON agents
    FOR SELECT
    TO authenticated
    USING (is_public = TRUE AND status = 'active');

-- ============================================================================
-- 5. CREATE TRIGGER FOR updated_at
-- ============================================================================

-- Criar função se não existir (pode já existir de outras tabelas)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar trigger
CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 6. GRANT PERMISSIONS
-- ============================================================================

-- Garantir que authenticated users podem acessar a tabela
GRANT SELECT, INSERT, UPDATE, DELETE ON agents TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON agents TO service_role;

-- ============================================================================
-- 7. COMMENTS (Documentação)
-- ============================================================================

COMMENT ON TABLE agents IS 'Agentes principais criados via Wizard. Cada agent pertence a um client e pode ter múltiplos sub-agents.';
COMMENT ON COLUMN agents.id IS 'Identificador único do agent';
COMMENT ON COLUMN agents.client_id IS 'Cliente dono do agent';
COMMENT ON COLUMN agents.name IS 'Nome do agent (ex: Atendente Virtual)';
COMMENT ON COLUMN agents.description IS 'Descrição do agent';
COMMENT ON COLUMN agents.slug IS 'URL-friendly identifier (ex: atendente-virtual)';
COMMENT ON COLUMN agents.model IS 'Modelo LLM usado (gpt-4o-mini, claude-3-5-sonnet, etc)';
COMMENT ON COLUMN agents.system_prompt IS 'Prompt de sistema que define comportamento do agent';
COMMENT ON COLUMN agents.channel IS 'Canal de comunicação (whatsapp, web, sms, email)';
COMMENT ON COLUMN agents.template_type IS 'Tipo de template usado no wizard (customer_service, sales, etc)';
COMMENT ON COLUMN agents.status IS 'Status do agent: draft (em criação), active (publicado), inactive (desativado)';
COMMENT ON COLUMN agents.is_public IS 'Se true, agent pode ser acessado via URL pública';
COMMENT ON COLUMN agents.public_url IS 'URL pública do agent (ex: https://renum.com/chat/atendente-virtual)';
COMMENT ON COLUMN agents.config IS 'Configuração completa do wizard (step_1_data, step_2_data, etc)';
COMMENT ON COLUMN agents.access_count IS 'Contador de acessos via URL pública';
COMMENT ON COLUMN agents.created_at IS 'Data de criação';
COMMENT ON COLUMN agents.updated_at IS 'Data da última atualização';

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Verificar criação
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'agents') THEN
        RAISE NOTICE '✅ Tabela agents criada com sucesso';
    ELSE
        RAISE EXCEPTION '❌ Erro: Tabela agents não foi criada';
    END IF;
    
    IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'agents' AND rowsecurity = true) THEN
        RAISE NOTICE '✅ RLS habilitado em agents';
    ELSE
        RAISE EXCEPTION '❌ Erro: RLS não foi habilitado em agents';
    END IF;
END $$;
