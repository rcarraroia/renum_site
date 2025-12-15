-- Migration 014: Create SICC RLS Policies
-- Row Level Security para isolamento multi-tenant
-- Data: 2025-12-07

-- ============================================================================
-- HABILITAR RLS EM TODAS AS TABELAS SICC
-- ============================================================================

ALTER TABLE agent_dna ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_memory_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_behavior_patterns ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_learning_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_knowledge_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_learning_settings ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- AGENT DNA - Políticas RLS
-- ============================================================================

-- Admins têm acesso total
CREATE POLICY "Admins have full access to agent_dna"
    ON agent_dna
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Clientes podem ver DNA de seus próprios agentes
CREATE POLICY "Clients can view own agents DNA"
    ON agent_dna
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM agents
            WHERE agents.id = agent_dna.agent_id
            AND agents.client_id IN (
                SELECT id FROM clients
            )
        )
    );

-- ============================================================================
-- AGENT MEMORY CHUNKS - Políticas RLS
-- ============================================================================

-- Admins têm acesso total
CREATE POLICY "Admins have full access to memory_chunks"
    ON agent_memory_chunks
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Clientes podem gerenciar memórias de seus agentes
CREATE POLICY "Clients can manage own agents memories"
    ON agent_memory_chunks
    FOR ALL
    TO authenticated
    USING (
        client_id IN (SELECT id FROM clients)
    )
    WITH CHECK (
        client_id IN (SELECT id FROM clients)
    );

-- ============================================================================
-- AGENT BEHAVIOR PATTERNS - Políticas RLS
-- ============================================================================

-- Admins têm acesso total
CREATE POLICY "Admins have full access to behavior_patterns"
    ON agent_behavior_patterns
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Clientes podem gerenciar padrões de seus agentes
CREATE POLICY "Clients can manage own agents patterns"
    ON agent_behavior_patterns
    FOR ALL
    TO authenticated
    USING (
        client_id IN (SELECT id FROM clients)
    )
    WITH CHECK (
        client_id IN (SELECT id FROM clients)
    );

-- ============================================================================
-- AGENT LEARNING LOGS - Políticas RLS
-- ============================================================================

-- Admins têm acesso total
CREATE POLICY "Admins have full access to learning_logs"
    ON agent_learning_logs
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Clientes podem ver e aprovar logs de seus agentes
CREATE POLICY "Clients can manage own agents learning_logs"
    ON agent_learning_logs
    FOR ALL
    TO authenticated
    USING (
        client_id IN (SELECT id FROM clients)
    )
    WITH CHECK (
        client_id IN (SELECT id FROM clients)
    );

-- ============================================================================
-- AGENT KNOWLEDGE SNAPSHOTS - Políticas RLS
-- ============================================================================

-- Admins têm acesso total
CREATE POLICY "Admins have full access to snapshots"
    ON agent_knowledge_snapshots
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Clientes podem ver snapshots de seus agentes
CREATE POLICY "Clients can view own agents snapshots"
    ON agent_knowledge_snapshots
    FOR SELECT
    TO authenticated
    USING (
        client_id IN (SELECT id FROM clients)
    );

-- Clientes podem criar snapshots manuais
CREATE POLICY "Clients can create manual snapshots"
    ON agent_knowledge_snapshots
    FOR INSERT
    TO authenticated
    WITH CHECK (
        client_id IN (SELECT id FROM clients)
        AND snapshot_type = 'manual'
    );

-- ============================================================================
-- AGENT PERFORMANCE METRICS - Políticas RLS
-- ============================================================================

-- Admins têm acesso total
CREATE POLICY "Admins have full access to metrics"
    ON agent_performance_metrics
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Clientes podem ver métricas de seus agentes
CREATE POLICY "Clients can view own agents metrics"
    ON agent_performance_metrics
    FOR SELECT
    TO authenticated
    USING (
        client_id IN (SELECT id FROM clients)
    );

-- Sistema pode inserir métricas (service_role)
-- Não precisa de política explícita pois service_role bypassa RLS

-- ============================================================================
-- AGENT LEARNING SETTINGS - Políticas RLS
-- ============================================================================

-- Admins têm acesso total
CREATE POLICY "Admins have full access to learning_settings"
    ON agent_learning_settings
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Clientes podem gerenciar configurações de seus agentes
CREATE POLICY "Clients can manage own agents settings"
    ON agent_learning_settings
    FOR ALL
    TO authenticated
    USING (
        client_id IN (SELECT id FROM clients)
    )
    WITH CHECK (
        client_id IN (SELECT id FROM clients)
    );

-- ============================================================================
-- GRANTS - Permissões de tabela
-- ============================================================================

-- Authenticated users podem acessar (RLS controla o que veem)
GRANT SELECT, INSERT, UPDATE, DELETE ON agent_dna TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON agent_memory_chunks TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON agent_behavior_patterns TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON agent_learning_logs TO authenticated;
GRANT SELECT, INSERT ON agent_knowledge_snapshots TO authenticated;
GRANT SELECT ON agent_performance_metrics TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON agent_learning_settings TO authenticated;

-- Service role tem acesso total (bypassa RLS)
GRANT ALL ON agent_dna TO service_role;
GRANT ALL ON agent_memory_chunks TO service_role;
GRANT ALL ON agent_behavior_patterns TO service_role;
GRANT ALL ON agent_learning_logs TO service_role;
GRANT ALL ON agent_knowledge_snapshots TO service_role;
GRANT ALL ON agent_performance_metrics TO service_role;
GRANT ALL ON agent_learning_settings TO service_role;

-- ============================================================================
-- TESTES DE RLS (Comentados - descomentar para testar)
-- ============================================================================

-- Para testar RLS, execute como usuário específico:
-- SET ROLE authenticated;
-- SET request.jwt.claim.sub = '<user_uuid>';
-- SELECT * FROM agent_memory_chunks; -- Deve retornar apenas dados do cliente
-- RESET ROLE;

-- ============================================================================
-- FIM DA MIGRATION 014
-- ============================================================================
