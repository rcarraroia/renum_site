-- Migration 013: Create SICC Indexes
-- Índices otimizados para performance do SICC
-- Data: 2025-12-07

-- ============================================================================
-- AGENT DNA - Índices
-- ============================================================================

CREATE INDEX idx_agent_dna_agent_id 
    ON agent_dna(agent_id) 
    WHERE is_active = true;

CREATE INDEX idx_agent_dna_version 
    ON agent_dna(agent_id, version DESC);

-- ============================================================================
-- AGENT MEMORY CHUNKS - Índices
-- ============================================================================

-- Índice principal: agent + ativo
CREATE INDEX idx_memory_agent_active 
    ON agent_memory_chunks(agent_id, is_active) 
    WHERE is_active = true;

-- Índice para isolamento multi-tenant
CREATE INDEX idx_memory_client_id 
    ON agent_memory_chunks(client_id);

-- Índice por tipo de chunk
CREATE INDEX idx_memory_chunk_type 
    ON agent_memory_chunks(chunk_type);

-- Índice para ordenação por uso
CREATE INDEX idx_memory_usage_count 
    ON agent_memory_chunks(usage_count DESC) 
    WHERE is_active = true;

-- Índice para busca por confidence
CREATE INDEX idx_memory_confidence 
    ON agent_memory_chunks(confidence_score DESC) 
    WHERE is_active = true;

-- Índice para last_used_at
CREATE INDEX idx_memory_last_used 
    ON agent_memory_chunks(last_used_at DESC NULLS LAST) 
    WHERE is_active = true;

-- Índice CRÍTICO: Vector similarity search (IVFFlat)
-- Usando cosine distance para similarity search
CREATE INDEX idx_memory_embedding_ivfflat 
    ON agent_memory_chunks 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Índice alternativo: HNSW (mais rápido, mais memória)
-- Descomentar se performance for crítica e houver RAM disponível
-- CREATE INDEX idx_memory_embedding_hnsw 
--     ON agent_memory_chunks 
--     USING hnsw (embedding vector_cosine_ops)
--     WITH (m = 16, ef_construction = 64);

-- Índice composto para queries comuns
CREATE INDEX idx_memory_agent_type_active 
    ON agent_memory_chunks(agent_id, chunk_type, is_active) 
    WHERE is_active = true;

-- ============================================================================
-- AGENT BEHAVIOR PATTERNS - Índices
-- ============================================================================

-- Índice principal: agent + ativo
CREATE INDEX idx_behavior_agent_active 
    ON agent_behavior_patterns(agent_id, is_active) 
    WHERE is_active = true;

-- Índice para isolamento multi-tenant
CREATE INDEX idx_behavior_client_id 
    ON agent_behavior_patterns(client_id);

-- Índice por tipo de padrão
CREATE INDEX idx_behavior_pattern_type 
    ON agent_behavior_patterns(pattern_type);

-- Índice para ordenação por success_rate
CREATE INDEX idx_behavior_success_rate 
    ON agent_behavior_patterns(success_rate DESC) 
    WHERE is_active = true;

-- Índice para last_applied_at
CREATE INDEX idx_behavior_last_applied 
    ON agent_behavior_patterns(last_applied_at DESC NULLS LAST) 
    WHERE is_active = true;

-- Índice GIN para busca em trigger_context (JSONB)
CREATE INDEX idx_behavior_trigger_context 
    ON agent_behavior_patterns USING gin(trigger_context);

-- Índice composto para queries comuns
CREATE INDEX idx_behavior_agent_type_active 
    ON agent_behavior_patterns(agent_id, pattern_type, is_active) 
    WHERE is_active = true;

-- ============================================================================
-- AGENT LEARNING LOGS - Índices
-- ============================================================================

-- Índice principal: agent + status
CREATE INDEX idx_learning_agent_status 
    ON agent_learning_logs(agent_id, status);

-- Índice para isolamento multi-tenant
CREATE INDEX idx_learning_client_id 
    ON agent_learning_logs(client_id);

-- Índice por tipo de aprendizado
CREATE INDEX idx_learning_type 
    ON agent_learning_logs(learning_type);

-- Índice para ordenação por data
CREATE INDEX idx_learning_created_at 
    ON agent_learning_logs(created_at DESC);

-- Índice para confidence
CREATE INDEX idx_learning_confidence 
    ON agent_learning_logs(confidence DESC);

-- Índice para pending reviews (query comum)
CREATE INDEX idx_learning_pending 
    ON agent_learning_logs(agent_id, created_at DESC) 
    WHERE status = 'pending';

-- Índice para reviewed_by (auditoria)
CREATE INDEX idx_learning_reviewed_by 
    ON agent_learning_logs(reviewed_by, reviewed_at DESC) 
    WHERE reviewed_by IS NOT NULL;

-- Índice GIN para busca em source_data e analysis (JSONB)
CREATE INDEX idx_learning_source_data 
    ON agent_learning_logs USING gin(source_data);

CREATE INDEX idx_learning_analysis 
    ON agent_learning_logs USING gin(analysis);

-- ============================================================================
-- AGENT KNOWLEDGE SNAPSHOTS - Índices
-- ============================================================================

-- Índice principal: agent + data
CREATE INDEX idx_snapshot_agent_date 
    ON agent_knowledge_snapshots(agent_id, created_at DESC);

-- Índice para isolamento multi-tenant
CREATE INDEX idx_snapshot_client_id 
    ON agent_knowledge_snapshots(client_id);

-- Índice por tipo de snapshot
CREATE INDEX idx_snapshot_type 
    ON agent_knowledge_snapshots(snapshot_type);

-- Índice para buscar último snapshot
CREATE INDEX idx_snapshot_latest 
    ON agent_knowledge_snapshots(agent_id, created_at DESC);

-- Índice GIN para busca em snapshot_data (JSONB)
CREATE INDEX idx_snapshot_data 
    ON agent_knowledge_snapshots USING gin(snapshot_data);

-- ============================================================================
-- AGENT PERFORMANCE METRICS - Índices
-- ============================================================================

-- Índice principal: agent + data (UNIQUE já cria índice)
-- Mas criamos um adicional para ordenação DESC
CREATE INDEX idx_metrics_agent_date_desc 
    ON agent_performance_metrics(agent_id, metric_date DESC);

-- Índice para isolamento multi-tenant
CREATE INDEX idx_metrics_client_id 
    ON agent_performance_metrics(client_id);

-- Índice para buscar métricas recentes
CREATE INDEX idx_metrics_recent 
    ON agent_performance_metrics(metric_date DESC);

-- Índice para análise de conversão
CREATE INDEX idx_metrics_conversion 
    ON agent_performance_metrics(agent_id, conversion_rate DESC NULLS LAST);

-- Índice GIN para busca em metadata (JSONB)
CREATE INDEX idx_metrics_metadata 
    ON agent_performance_metrics USING gin(metadata);

-- ============================================================================
-- AGENT LEARNING SETTINGS - Índices
-- ============================================================================

-- Índice para isolamento multi-tenant
CREATE INDEX idx_settings_client_id 
    ON agent_learning_settings(client_id);

-- Índice para agentes com learning habilitado
CREATE INDEX idx_settings_learning_enabled 
    ON agent_learning_settings(agent_id) 
    WHERE learning_enabled = true;

-- Índice GIN para busca em enabled_learning_types (JSONB)
CREATE INDEX idx_settings_learning_types 
    ON agent_learning_settings USING gin(enabled_learning_types);

-- ============================================================================
-- ESTATÍSTICAS
-- ============================================================================

-- Atualizar estatísticas para o query planner
ANALYZE agent_dna;
ANALYZE agent_memory_chunks;
ANALYZE agent_behavior_patterns;
ANALYZE agent_learning_logs;
ANALYZE agent_knowledge_snapshots;
ANALYZE agent_performance_metrics;
ANALYZE agent_learning_settings;

-- ============================================================================
-- FIM DA MIGRATION 013
-- ============================================================================
