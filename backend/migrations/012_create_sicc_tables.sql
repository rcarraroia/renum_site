-- Migration 012: Create SICC Tables
-- Sistema de Inteligência Corporativa Contínua
-- Data: 2025-12-07

-- ============================================================================
-- 1. AGENT DNA (Núcleo Cognitivo Fixo)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_dna (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    function TEXT NOT NULL,
    principles JSONB NOT NULL DEFAULT '[]'::jsonb,
    restrictions JSONB NOT NULL DEFAULT '[]'::jsonb,
    tone_of_voice TEXT NOT NULL,
    operational_limits JSONB NOT NULL DEFAULT '{}'::jsonb,
    security_policies JSONB NOT NULL DEFAULT '{}'::jsonb,
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT agent_dna_version_positive CHECK (version > 0)
);

-- Unique constraint parcial (apenas um DNA ativo por agente)
CREATE UNIQUE INDEX agent_dna_unique_active 
    ON agent_dna(agent_id) 
    WHERE is_active = true;

COMMENT ON TABLE agent_dna IS 'DNA cognitivo fixo dos agentes - não modificado por aprendizado automático';
COMMENT ON COLUMN agent_dna.function IS 'Função principal do agente';
COMMENT ON COLUMN agent_dna.principles IS 'Princípios fundamentais (array de strings)';
COMMENT ON COLUMN agent_dna.restrictions IS 'Restrições operacionais (array de strings)';
COMMENT ON COLUMN agent_dna.version IS 'Versão do DNA para auditoria';

-- ============================================================================
-- 2. AGENT MEMORY CHUNKS (Memória Adaptativa)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_memory_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    chunk_type TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384), -- GTE-small dimension
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    source TEXT,
    confidence_score FLOAT NOT NULL DEFAULT 1.0,
    usage_count INTEGER NOT NULL DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    version INTEGER NOT NULL DEFAULT 1,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT memory_chunk_type_valid CHECK (
        chunk_type IN ('business_term', 'process', 'faq', 'product', 'objection', 'pattern', 'insight')
    ),
    CONSTRAINT memory_source_valid CHECK (
        source IS NULL OR source IN ('conversation', 'document', 'manual', 'isa_analysis', 'interview')
    ),
    CONSTRAINT memory_confidence_range CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    CONSTRAINT memory_usage_count_positive CHECK (usage_count >= 0),
    CONSTRAINT memory_version_positive CHECK (version > 0)
);

COMMENT ON TABLE agent_memory_chunks IS 'Memória adaptativa dos agentes - conhecimento aprendido';
COMMENT ON COLUMN agent_memory_chunks.chunk_type IS 'Tipo de conhecimento armazenado';
COMMENT ON COLUMN agent_memory_chunks.embedding IS 'Vector embedding para similarity search';
COMMENT ON COLUMN agent_memory_chunks.confidence_score IS 'Confiança no conhecimento (0.0-1.0)';
COMMENT ON COLUMN agent_memory_chunks.usage_count IS 'Quantas vezes foi usado';

-- ============================================================================
-- 3. AGENT BEHAVIOR PATTERNS (Heurísticas Comportamentais)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_behavior_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    pattern_type TEXT NOT NULL,
    trigger_context JSONB NOT NULL,
    action_config JSONB NOT NULL,
    success_rate FLOAT NOT NULL DEFAULT 0.0,
    total_applications INTEGER NOT NULL DEFAULT 0,
    successful_applications INTEGER NOT NULL DEFAULT 0,
    last_applied_at TIMESTAMPTZ,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT pattern_type_valid CHECK (
        pattern_type IN ('response_strategy', 'tone_adjustment', 'flow_optimization', 'objection_handling')
    ),
    CONSTRAINT pattern_success_rate_range CHECK (success_rate >= 0.0 AND success_rate <= 1.0),
    CONSTRAINT pattern_applications_positive CHECK (total_applications >= 0),
    CONSTRAINT pattern_successful_positive CHECK (successful_applications >= 0),
    CONSTRAINT pattern_successful_lte_total CHECK (successful_applications <= total_applications)
);

COMMENT ON TABLE agent_behavior_patterns IS 'Padrões comportamentais aprendidos pelos agentes';
COMMENT ON COLUMN agent_behavior_patterns.trigger_context IS 'Condições para aplicar o padrão';
COMMENT ON COLUMN agent_behavior_patterns.action_config IS 'Ação a executar quando padrão é aplicado';
COMMENT ON COLUMN agent_behavior_patterns.success_rate IS 'Taxa de sucesso (0.0-1.0)';

-- ============================================================================
-- 4. AGENT LEARNING LOGS (Logs de Aprendizado - ISA)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_learning_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    learning_type TEXT NOT NULL,
    source_data JSONB NOT NULL,
    analysis JSONB NOT NULL,
    action_taken TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    reviewed_by UUID REFERENCES profiles(id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT learning_type_valid CHECK (
        learning_type IN ('memory_added', 'pattern_detected', 'behavior_updated', 'insight_generated')
    ),
    CONSTRAINT learning_confidence_range CHECK (confidence >= 0.0 AND confidence <= 1.0),
    CONSTRAINT learning_status_valid CHECK (
        status IN ('pending', 'approved', 'rejected', 'applied')
    ),
    CONSTRAINT learning_reviewed_consistency CHECK (
        (status IN ('approved', 'rejected') AND reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL) OR
        (status IN ('pending', 'applied'))
    )
);

COMMENT ON TABLE agent_learning_logs IS 'Logs de aprendizado analisados pela ISA';
COMMENT ON COLUMN agent_learning_logs.learning_type IS 'Tipo de aprendizado detectado';
COMMENT ON COLUMN agent_learning_logs.confidence IS 'Confiança da ISA no aprendizado (0.0-1.0)';
COMMENT ON COLUMN agent_learning_logs.status IS 'Status do aprendizado (pending/approved/rejected/applied)';

-- ============================================================================
-- 5. AGENT KNOWLEDGE SNAPSHOTS (Snapshots de Conhecimento)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_knowledge_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    snapshot_type TEXT NOT NULL DEFAULT 'automatic',
    memory_count INTEGER NOT NULL,
    pattern_count INTEGER NOT NULL,
    total_interactions INTEGER NOT NULL,
    avg_success_rate FLOAT,
    snapshot_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT snapshot_type_valid CHECK (
        snapshot_type IN ('automatic', 'manual', 'milestone', 'pre_rollback')
    ),
    CONSTRAINT snapshot_memory_count_positive CHECK (memory_count >= 0),
    CONSTRAINT snapshot_pattern_count_positive CHECK (pattern_count >= 0),
    CONSTRAINT snapshot_interactions_positive CHECK (total_interactions >= 0),
    CONSTRAINT snapshot_success_rate_range CHECK (
        avg_success_rate IS NULL OR (avg_success_rate >= 0.0 AND avg_success_rate <= 1.0)
    )
);

COMMENT ON TABLE agent_knowledge_snapshots IS 'Snapshots do estado de conhecimento dos agentes';
COMMENT ON COLUMN agent_knowledge_snapshots.snapshot_type IS 'Tipo de snapshot (automatic/manual/milestone/pre_rollback)';
COMMENT ON COLUMN agent_knowledge_snapshots.snapshot_data IS 'Dados completos do snapshot para rollback';

-- ============================================================================
-- 6. AGENT PERFORMANCE METRICS (Métricas de Performance)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_performance_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    metric_date DATE NOT NULL,
    total_interactions INTEGER NOT NULL DEFAULT 0,
    successful_interactions INTEGER NOT NULL DEFAULT 0,
    avg_response_time_ms INTEGER,
    user_satisfaction_score FLOAT,
    conversion_rate FLOAT,
    memory_chunks_used INTEGER NOT NULL DEFAULT 0,
    patterns_applied INTEGER NOT NULL DEFAULT 0,
    new_learnings INTEGER NOT NULL DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT metrics_interactions_positive CHECK (total_interactions >= 0),
    CONSTRAINT metrics_successful_positive CHECK (successful_interactions >= 0),
    CONSTRAINT metrics_successful_lte_total CHECK (successful_interactions <= total_interactions),
    CONSTRAINT metrics_response_time_positive CHECK (avg_response_time_ms IS NULL OR avg_response_time_ms >= 0),
    CONSTRAINT metrics_satisfaction_range CHECK (
        user_satisfaction_score IS NULL OR (user_satisfaction_score >= 0.0 AND user_satisfaction_score <= 5.0)
    ),
    CONSTRAINT metrics_conversion_range CHECK (
        conversion_rate IS NULL OR (conversion_rate >= 0.0 AND conversion_rate <= 1.0)
    ),
    CONSTRAINT metrics_memory_used_positive CHECK (memory_chunks_used >= 0),
    CONSTRAINT metrics_patterns_positive CHECK (patterns_applied >= 0),
    CONSTRAINT metrics_learnings_positive CHECK (new_learnings >= 0),
    CONSTRAINT metrics_unique_agent_date UNIQUE (agent_id, metric_date)
);

COMMENT ON TABLE agent_performance_metrics IS 'Métricas diárias de performance dos agentes';
COMMENT ON COLUMN agent_performance_metrics.metric_date IS 'Data das métricas (agregação diária)';
COMMENT ON COLUMN agent_performance_metrics.user_satisfaction_score IS 'Score de satisfação (0.0-5.0)';
COMMENT ON COLUMN agent_performance_metrics.conversion_rate IS 'Taxa de conversão (0.0-1.0)';

-- ============================================================================
-- 7. AGENT LEARNING SETTINGS (Configurações de Aprendizado)
-- ============================================================================
CREATE TABLE IF NOT EXISTS agent_learning_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE UNIQUE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    learning_enabled BOOLEAN NOT NULL DEFAULT true,
    auto_approve_threshold FLOAT NOT NULL DEFAULT 0.8,
    analysis_frequency TEXT NOT NULL DEFAULT 'hourly',
    max_memories_quota INTEGER NOT NULL DEFAULT 10000,
    max_patterns_quota INTEGER NOT NULL DEFAULT 1000,
    enabled_learning_types JSONB NOT NULL DEFAULT '["memory_added", "pattern_detected", "behavior_updated", "insight_generated"]'::jsonb,
    snapshot_frequency TEXT NOT NULL DEFAULT 'daily',
    retention_days INTEGER NOT NULL DEFAULT 90,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT settings_threshold_range CHECK (auto_approve_threshold >= 0.0 AND auto_approve_threshold <= 1.0),
    CONSTRAINT settings_frequency_valid CHECK (
        analysis_frequency IN ('realtime', 'hourly', 'daily', 'weekly', 'manual')
    ),
    CONSTRAINT settings_snapshot_frequency_valid CHECK (
        snapshot_frequency IN ('hourly', 'daily', 'weekly', 'monthly')
    ),
    CONSTRAINT settings_memories_quota_positive CHECK (max_memories_quota > 0),
    CONSTRAINT settings_patterns_quota_positive CHECK (max_patterns_quota > 0),
    CONSTRAINT settings_retention_positive CHECK (retention_days > 0)
);

COMMENT ON TABLE agent_learning_settings IS 'Configurações de aprendizado por agente';
COMMENT ON COLUMN agent_learning_settings.auto_approve_threshold IS 'Threshold para aprovação automática (0.0-1.0)';
COMMENT ON COLUMN agent_learning_settings.analysis_frequency IS 'Frequência de análise ISA';
COMMENT ON COLUMN agent_learning_settings.max_memories_quota IS 'Quota máxima de memórias';

-- ============================================================================
-- TRIGGERS para updated_at
-- ============================================================================

CREATE TRIGGER update_agent_dna_updated_at
    BEFORE UPDATE ON agent_dna
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_memory_chunks_updated_at
    BEFORE UPDATE ON agent_memory_chunks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_behavior_patterns_updated_at
    BEFORE UPDATE ON agent_behavior_patterns
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_learning_settings_updated_at
    BEFORE UPDATE ON agent_learning_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- FIM DA MIGRATION 012
-- ============================================================================
