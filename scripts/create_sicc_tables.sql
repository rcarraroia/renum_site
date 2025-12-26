-- ============================================================================
-- SCRIPT PARA CRIAR TABELAS SICC NO SUPABASE
-- Execute este arquivo no SQL Editor do Supabase Dashboard
-- ============================================================================

-- 1. TABELA MEMORY_CHUNKS
-- Armazena memórias/conhecimento do agente
CREATE TABLE IF NOT EXISTS memory_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL,
    client_id UUID NOT NULL,
    content TEXT NOT NULL,
    chunk_type VARCHAR(50) NOT NULL CHECK (chunk_type IN (
        'business_term', 'process', 'faq', 'product', 
        'objection', 'pattern', 'insight'
    )),
    embedding VECTOR(384),
    metadata JSONB DEFAULT '{}',
    source VARCHAR(500),
    confidence_score FLOAT DEFAULT 1.0 CHECK (confidence_score >= 0 AND confidence_score <= 1),
    usage_count INT DEFAULT 0,
    last_accessed_at TIMESTAMP WITH TIME ZONE,
    version INT DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 2. TABELA LEARNING_LOGS
-- Armazena aprendizados pendentes de aprovação
CREATE TABLE IF NOT EXISTS learning_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL,
    client_id UUID NOT NULL,
    learning_type VARCHAR(100) NOT NULL,
    source_data JSONB NOT NULL,
    analysis JSONB NOT NULL,
    action_taken TEXT,
    confidence FLOAT DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'approved', 'rejected', 'auto_approved', 'needs_review'
    )),
    reviewed_by UUID,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 3. TABELA BEHAVIOR_PATTERNS
-- Armazena padrões comportamentais do agente
CREATE TABLE IF NOT EXISTS behavior_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL,
    client_id UUID NOT NULL,
    pattern_type VARCHAR(50) NOT NULL CHECK (pattern_type IN (
        'response_strategy', 'tone_adjustment', 'flow_optimization', 'objection_handling'
    )),
    trigger_context JSONB NOT NULL,
    action_config JSONB NOT NULL,
    success_rate FLOAT DEFAULT 0.0 CHECK (success_rate >= 0 AND success_rate <= 1),
    application_count INT DEFAULT 0,
    confidence FLOAT DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    is_active BOOLEAN DEFAULT true,
    last_used_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 4. TABELA AGENT_SNAPSHOTS
-- Armazena snapshots do conhecimento do agente
CREATE TABLE IF NOT EXISTS agent_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL,
    name VARCHAR(255),
    memories_count INT DEFAULT 0,
    patterns_count INT DEFAULT 0,
    total_interactions INT DEFAULT 0,
    success_rate FLOAT DEFAULT 0.0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 5. TABELA SICC_SETTINGS
-- Configurações do SICC por agente
CREATE TABLE IF NOT EXISTS sicc_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL UNIQUE,
    auto_approve_threshold FLOAT DEFAULT 0.9 CHECK (auto_approve_threshold >= 0 AND auto_approve_threshold <= 1),
    manual_review_threshold FLOAT DEFAULT 0.7 CHECK (manual_review_threshold >= 0 AND manual_review_threshold <= 1),
    consolidation_frequency_hours INT DEFAULT 24,
    min_learnings_for_consolidation INT DEFAULT 10,
    max_memory_chunks INT DEFAULT 10000,
    memory_importance_threshold FLOAT DEFAULT 0.3,
    memory_retention_days INT DEFAULT 365,
    max_behavior_patterns INT DEFAULT 1000,
    pattern_min_usage_count INT DEFAULT 5,
    pattern_success_threshold FLOAT DEFAULT 0.6,
    auto_snapshot_enabled BOOLEAN DEFAULT true,
    snapshot_frequency_days INT DEFAULT 7,
    max_snapshots INT DEFAULT 52,
    learn_from_conversations BOOLEAN DEFAULT true,
    learn_from_documents BOOLEAN DEFAULT true,
    learn_from_feedback BOOLEAN DEFAULT true,
    learn_from_patterns BOOLEAN DEFAULT true,
    embedding_model VARCHAR(50) DEFAULT 'gte-small',
    similarity_algorithm VARCHAR(50) DEFAULT 'cosine',
    custom_config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- 6. TABELA AGENT_METRICS
-- Métricas diárias do agente
CREATE TABLE IF NOT EXISTS agent_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL,
    metric_date DATE NOT NULL,
    total_memories INT DEFAULT 0,
    active_memories INT DEFAULT 0,
    total_patterns INT DEFAULT 0,
    active_patterns INT DEFAULT 0,
    learning_velocity FLOAT DEFAULT 0.0,
    avg_confidence FLOAT DEFAULT 0.0,
    success_rate FLOAT DEFAULT 0.0,
    interactions_count INT DEFAULT 0,
    auto_approved_learnings INT DEFAULT 0,
    manual_approved_learnings INT DEFAULT 0,
    rejected_learnings INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    
    UNIQUE(agent_id, metric_date)
);

-- ============================================================================
-- CRIAR ÍNDICES PARA PERFORMANCE
-- ============================================================================

-- Índices para memory_chunks
CREATE INDEX IF NOT EXISTS idx_memory_chunks_agent_id ON memory_chunks(agent_id);
CREATE INDEX IF NOT EXISTS idx_memory_chunks_client_id ON memory_chunks(client_id);
CREATE INDEX IF NOT EXISTS idx_memory_chunks_chunk_type ON memory_chunks(chunk_type);
CREATE INDEX IF NOT EXISTS idx_memory_chunks_is_active ON memory_chunks(is_active);

-- Índices para learning_logs
CREATE INDEX IF NOT EXISTS idx_learning_logs_agent_id ON learning_logs(agent_id);
CREATE INDEX IF NOT EXISTS idx_learning_logs_client_id ON learning_logs(client_id);
CREATE INDEX IF NOT EXISTS idx_learning_logs_status ON learning_logs(status);
CREATE INDEX IF NOT EXISTS idx_learning_logs_created_at ON learning_logs(created_at);

-- Índices para behavior_patterns
CREATE INDEX IF NOT EXISTS idx_behavior_patterns_agent_id ON behavior_patterns(agent_id);
CREATE INDEX IF NOT EXISTS idx_behavior_patterns_pattern_type ON behavior_patterns(pattern_type);
CREATE INDEX IF NOT EXISTS idx_behavior_patterns_is_active ON behavior_patterns(is_active);

-- Índices para agent_snapshots
CREATE INDEX IF NOT EXISTS idx_agent_snapshots_agent_id ON agent_snapshots(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_snapshots_created_at ON agent_snapshots(created_at);

-- Índices para sicc_settings
CREATE INDEX IF NOT EXISTS idx_sicc_settings_agent_id ON sicc_settings(agent_id);

-- Índices para agent_metrics
CREATE INDEX IF NOT EXISTS idx_agent_metrics_agent_id ON agent_metrics(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_metrics_date ON agent_metrics(metric_date);

-- ============================================================================
-- HABILITAR RLS (ROW LEVEL SECURITY)
-- ============================================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE memory_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE behavior_patterns ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE sicc_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_metrics ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- CRIAR POLÍTICAS RLS
-- ============================================================================

-- Políticas para ADMINS (acesso total)
CREATE POLICY "Admins have full access to memory_chunks"
    ON memory_chunks FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Admins have full access to learning_logs"
    ON learning_logs FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Admins have full access to behavior_patterns"
    ON behavior_patterns FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Admins have full access to agent_snapshots"
    ON agent_snapshots FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Admins have full access to sicc_settings"
    ON sicc_settings FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

CREATE POLICY "Admins have full access to agent_metrics"
    ON agent_metrics FOR ALL TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM profiles
            WHERE profiles.id = auth.uid()
            AND profiles.role = 'admin'
        )
    );

-- Políticas para CLIENTES (apenas seus dados)
-- Nota: A estrutura atual não tem profile_id em clients
-- Estas políticas serão ajustadas conforme a arquitetura real do sistema
CREATE POLICY "Clients can view own memory_chunks"
    ON memory_chunks FOR SELECT TO authenticated
    USING (client_id = auth.uid());

CREATE POLICY "Clients can view own learning_logs"
    ON learning_logs FOR SELECT TO authenticated
    USING (client_id = auth.uid());

CREATE POLICY "Clients can view own behavior_patterns"
    ON behavior_patterns FOR SELECT TO authenticated
    USING (client_id = auth.uid());

-- ============================================================================
-- CRIAR TRIGGERS PARA UPDATED_AT
-- ============================================================================

-- Trigger para memory_chunks
CREATE TRIGGER update_memory_chunks_updated_at
    BEFORE UPDATE ON memory_chunks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para learning_logs
CREATE TRIGGER update_learning_logs_updated_at
    BEFORE UPDATE ON learning_logs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para behavior_patterns
CREATE TRIGGER update_behavior_patterns_updated_at
    BEFORE UPDATE ON behavior_patterns
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para sicc_settings
CREATE TRIGGER update_sicc_settings_updated_at
    BEFORE UPDATE ON sicc_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- INSERIR CONFIGURAÇÕES PADRÃO PARA AGENTES EXISTENTES
-- ============================================================================

-- Inserir configurações SICC padrão para agentes existentes
INSERT INTO sicc_settings (agent_id, auto_approve_threshold, manual_review_threshold)
SELECT 
    id as agent_id,
    0.9 as auto_approve_threshold,
    0.7 as manual_review_threshold
FROM agents
WHERE id NOT IN (SELECT agent_id FROM sicc_settings)
ON CONFLICT (agent_id) DO NOTHING;

-- ============================================================================
-- VERIFICAR CRIAÇÃO DAS TABELAS
-- ============================================================================

-- Listar tabelas SICC criadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'memory_chunks', 'learning_logs', 'behavior_patterns', 
    'agent_snapshots', 'sicc_settings', 'agent_metrics'
)
ORDER BY table_name;

-- Contar registros em cada tabela
SELECT 
    'memory_chunks' as table_name,
    COUNT(*) as count
FROM memory_chunks
UNION ALL
SELECT 'learning_logs', COUNT(*) FROM learning_logs
UNION ALL
SELECT 'behavior_patterns', COUNT(*) FROM behavior_patterns
UNION ALL
SELECT 'agent_snapshots', COUNT(*) FROM agent_snapshots
UNION ALL
SELECT 'sicc_settings', COUNT(*) FROM sicc_settings
UNION ALL
SELECT 'agent_metrics', COUNT(*) FROM agent_metrics;

-- ============================================================================
-- SCRIPT CONCLUÍDO
-- ============================================================================

-- Se chegou até aqui sem erros, as tabelas SICC foram criadas com sucesso!
-- Execute: python scripts/check_supabase_tables.py para verificar