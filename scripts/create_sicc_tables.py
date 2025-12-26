#!/usr/bin/env python3
"""
Script para criar tabelas SICC no Supabase
"""
import os
import sys
from supabase import create_client, Client

# Credenciais
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# Criar cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=" * 80)
print("CRIANDO TABELAS SICC NO SUPABASE")
print("=" * 80)
print()

# SQL para criar tabelas SICC
sql_commands = [
    # 1. Tabela memory_chunks
    """
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
    """,
    
    # 2. Tabela learning_logs
    """
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
    """,
    
    # 3. Tabela behavior_patterns
    """
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
    """,
    
    # 4. Tabela agent_snapshots
    """
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
    """,
    
    # 5. Tabela sicc_settings
    """
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
    """,
    
    # 6. Tabela agent_metrics
    """
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
    """
]

# Executar comandos SQL
for i, sql in enumerate(sql_commands, 1):
    table_name = sql.split("CREATE TABLE IF NOT EXISTS ")[1].split(" (")[0].strip()
    print(f"{i}. Criando tabela {table_name}...")
    
    try:
        # Executar SQL via RPC (se disponível) ou via REST
        result = supabase.rpc('exec_sql', {'sql': sql}).execute()
        print(f"   ✅ {table_name} criada com sucesso")
    except Exception as e:
        print(f"   ❌ Erro ao criar {table_name}: {e}")
        # Tentar método alternativo
        try:
            # Método alternativo usando postgrest
            print(f"   🔄 Tentando método alternativo...")
            # Para este caso, vamos usar uma abordagem diferente
            print(f"   ⚠️  Execute manualmente no SQL Editor do Supabase")
        except Exception as e2:
            print(f"   ❌ Erro alternativo: {e2}")

print()
print("=" * 80)
print("CRIANDO ÍNDICES...")
print("=" * 80)

# Índices
index_commands = [
    "CREATE INDEX IF NOT EXISTS idx_memory_chunks_agent_id ON memory_chunks(agent_id);",
    "CREATE INDEX IF NOT EXISTS idx_memory_chunks_client_id ON memory_chunks(client_id);",
    "CREATE INDEX IF NOT EXISTS idx_memory_chunks_chunk_type ON memory_chunks(chunk_type);",
    "CREATE INDEX IF NOT EXISTS idx_memory_chunks_is_active ON memory_chunks(is_active);",
    
    "CREATE INDEX IF NOT EXISTS idx_learning_logs_agent_id ON learning_logs(agent_id);",
    "CREATE INDEX IF NOT EXISTS idx_learning_logs_client_id ON learning_logs(client_id);",
    "CREATE INDEX IF NOT EXISTS idx_learning_logs_status ON learning_logs(status);",
    "CREATE INDEX IF NOT EXISTS idx_learning_logs_created_at ON learning_logs(created_at);",
    
    "CREATE INDEX IF NOT EXISTS idx_behavior_patterns_agent_id ON behavior_patterns(agent_id);",
    "CREATE INDEX IF NOT EXISTS idx_behavior_patterns_pattern_type ON behavior_patterns(pattern_type);",
    "CREATE INDEX IF NOT EXISTS idx_behavior_patterns_is_active ON behavior_patterns(is_active);",
    
    "CREATE INDEX IF NOT EXISTS idx_agent_snapshots_agent_id ON agent_snapshots(agent_id);",
    "CREATE INDEX IF NOT EXISTS idx_agent_snapshots_created_at ON agent_snapshots(created_at);",
    
    "CREATE INDEX IF NOT EXISTS idx_sicc_settings_agent_id ON sicc_settings(agent_id);",
    
    "CREATE INDEX IF NOT EXISTS idx_agent_metrics_agent_id ON agent_metrics(agent_id);",
    "CREATE INDEX IF NOT EXISTS idx_agent_metrics_date ON agent_metrics(metric_date);"
]

for idx_sql in index_commands:
    index_name = idx_sql.split("CREATE INDEX IF NOT EXISTS ")[1].split(" ON")[0]
    print(f"Criando índice {index_name}...")
    try:
        result = supabase.rpc('exec_sql', {'sql': idx_sql}).execute()
        print(f"   ✅ {index_name} criado")
    except Exception as e:
        print(f"   ⚠️  Execute manualmente: {idx_sql}")

print()
print("=" * 80)
print("VERIFICANDO TABELAS CRIADAS...")
print("=" * 80)

# Verificar se tabelas foram criadas
tables_to_check = [
    'memory_chunks', 'learning_logs', 'behavior_patterns',
    'agent_snapshots', 'sicc_settings', 'agent_metrics'
]

created_tables = []
for table in tables_to_check:
    try:
        result = supabase.table(table).select("*").limit(1).execute()
        created_tables.append(table)
        print(f"✅ {table:25} - CRIADA")
    except Exception as e:
        print(f"❌ {table:25} - NÃO CRIADA: {e}")

print()
print("=" * 80)
print(f"RESUMO: {len(created_tables)}/6 tabelas criadas com sucesso")
print("=" * 80)

if len(created_tables) < 6:
    print()
    print("⚠️  ALGUMAS TABELAS NÃO FORAM CRIADAS AUTOMATICAMENTE")
    print("📋 EXECUTE OS COMANDOS SQL MANUALMENTE NO SUPABASE:")
    print()
    print("1. Acesse: https://supabase.com/dashboard/project/vhixvzaxswphwoymdhgg")
    print("2. Vá em 'SQL Editor'")
    print("3. Execute os comandos CREATE TABLE acima")
    print("4. Execute os comandos CREATE INDEX")
    print("5. Execute novamente: python scripts/check_supabase_tables.py")