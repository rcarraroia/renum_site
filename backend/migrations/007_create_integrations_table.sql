-- Migration 007: Create Agent Integrations Table
-- Sprint 3: Integrations
-- Data: 2025-12-15
-- Objetivo: Criar tabela para armazenar credenciais de integração (Uazapi, Chatwoot, Google, etc)

-- ============================================================================
-- 1. CREATE TABLE agent_integrations
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent_integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE, -- Nullable: Se NULL, é uma integração Global do Cliente via Wizard
    
    provider TEXT NOT NULL CHECK (provider IN ('uazapi', 'evolution', 'chatwoot', 'google_calendar', 'google_drive', 'whatsapp_official')),
    
    -- Configuração e Credenciais (Alguns campos sensíveis devem ser criptografados na aplicação)
    config JSONB NOT NULL DEFAULT '{}',
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Auditoria
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- ============================================================================
-- 2. CREATE INDEXES & CONSTRAINTS
-- ============================================================================

-- Garante que um cliente só tenha UMA integração global por provedor
CREATE UNIQUE INDEX idx_unique_client_global_integration 
ON agent_integrations(client_id, provider) 
WHERE agent_id IS NULL;

-- Garante que um agente só tenha UMA integração específica por provedor
CREATE UNIQUE INDEX idx_unique_agent_specific_integration 
ON agent_integrations(agent_id, provider) 
WHERE agent_id IS NOT NULL;

-- Index para buscar integrações de um cliente rapidamente
CREATE INDEX idx_agent_integrations_client ON agent_integrations(client_id);

-- ============================================================================
-- 3. ENABLE ROW LEVEL SECURITY (RLS)
-- ============================================================================

ALTER TABLE agent_integrations ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 4. CREATE RLS POLICIES
-- ============================================================================

-- Política 1: Clients podem ver apenas suas próprias integrações
CREATE POLICY "Clients can view own integrations"
    ON agent_integrations
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

-- Política 2: Clients podem criar integrações
CREATE POLICY "Clients can create own integrations"
    ON agent_integrations
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

-- Política 3: Clients podem atualizar suas integrações
CREATE POLICY "Clients can update own integrations"
    ON agent_integrations
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

-- Política 4: Clients podem deletar suas integrações
CREATE POLICY "Clients can delete own integrations"
    ON agent_integrations
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

-- ============================================================================
-- 5. CREATE TRIGGER FOR updated_at
-- ============================================================================

CREATE TRIGGER update_agent_integrations_updated_at
    BEFORE UPDATE ON agent_integrations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 6. GRANT PERMISSIONS
-- ============================================================================

GRANT SELECT, INSERT, UPDATE, DELETE ON agent_integrations TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON agent_integrations TO service_role;

-- ============================================================================
-- 7. COMMENTS
-- ============================================================================

COMMENT ON TABLE agent_integrations IS 'Armazena credenciais e configurações de integração externa. Suporta herança Global (Cliente) ou Override (Agente).';
COMMENT ON COLUMN agent_integrations.agent_id IS 'Se NULL, esta integração é aplicada a todos os agentes do cliente (padrão Wizard). Se preenchido, é um override específico para este agente.';
COMMENT ON COLUMN agent_integrations.config IS 'JSON com tokens, urls e instance_ids. Campos sensíveis devem ser tratados pelo Backend.';
