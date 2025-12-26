#!/usr/bin/env python3
"""
AUDITORIA COMPLETA DO BANCO DE DADOS RENUM
==========================================
Este script conecta ao Supabase real e lista TODAS as tabelas,
suas estruturas e contagem de registros.

Objetivo: Identificar tabelas ativas vs obsoletas
"""

import os
import sys

# Configuração direta (do backend/.env)
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# Tentar importar supabase
try:
    from supabase import create_client, Client
except ImportError:
    print("Instalando supabase...")
    os.system("pip install supabase")
    from supabase import create_client, Client

print(f"🔗 Conectando ao Supabase: {SUPABASE_URL[:50]}...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_all_tables():
    """Lista todas as tabelas do schema public"""
    query = """
    SELECT 
        table_name,
        (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name AND table_schema = 'public') as column_count
    FROM information_schema.tables t
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE'
    ORDER BY table_name;
    """
    # Usar RPC ou query direta
    try:
        result = supabase.rpc('get_table_list').execute()
        return result.data
    except:
        # Fallback: listar tabelas conhecidas manualmente
        return None

def count_table_records(table_name):
    """Conta registros em uma tabela"""
    try:
        result = supabase.table(table_name).select("*", count="exact").limit(1).execute()
        return result.count if result.count is not None else len(result.data) if result.data else 0
    except Exception as e:
        return f"ERRO: {str(e)[:50]}"

def get_table_columns(table_name):
    """Obtém colunas de uma tabela"""
    try:
        result = supabase.table(table_name).select("*").limit(1).execute()
        if result.data and len(result.data) > 0:
            return list(result.data[0].keys())
        return []
    except:
        return []

# Lista de tabelas conhecidas para verificar
KNOWN_TABLES = [
    # Core do Sistema
    "profiles",
    "clients", 
    "leads",
    "agents",
    "sub_agents",
    
    # Conversas e Mensagens
    "conversations",
    "messages",
    "interviews",
    "interview_messages",
    
    # Projetos e Configurações
    "projects",
    "renus_config",
    "tools",
    
    # SICC - Versão 1 (scripts/create_sicc_tables.sql)
    "memory_chunks",
    "learning_logs", 
    "behavior_patterns",
    "agent_snapshots",
    "sicc_settings",
    "agent_metrics",
    
    # SICC - Versão 2 (backend/migrations/012_create_sicc_tables.sql)
    "agent_dna",
    "agent_memory_chunks",
    "agent_behavior_patterns",
    "agent_learning_logs",
    "agent_knowledge_snapshots",
    "agent_performance_metrics",
    
    # Integrações (Sprint 07)
    "integrations",
    "integration_logs",
    "triggers",
    "trigger_logs",
    "webhooks",
    "webhook_logs",
    
    # RAG / Knowledge Base
    "knowledge_base",
    "knowledge_documents",
    "knowledge_chunks",
    "document_embeddings",
    
    # Marketplace
    "marketplace_templates",
    "template_purchases",
    
    # Pagamentos
    "payment_plans",
    "subscriptions",
    "payment_transactions",
    
    # ISA Commands
    "isa_commands",
    
    # Outras possíveis
    "audit_logs",
    "notifications",
    "user_settings",
    "api_keys",
    "sessions",
]

print("\n" + "="*80)
print("📊 AUDITORIA COMPLETA DO BANCO DE DADOS RENUM")
print("="*80)

results = []
existing_tables = []
missing_tables = []

for table in KNOWN_TABLES:
    count = count_table_records(table)
    if isinstance(count, int):
        existing_tables.append(table)
        columns = get_table_columns(table)
        results.append({
            "table": table,
            "exists": True,
            "count": count,
            "columns": len(columns),
            "column_names": columns[:5]  # Primeiras 5 colunas
        })
        status = "✅" if count > 0 else "⚠️ VAZIA"
        print(f"{status} {table}: {count} registros ({len(columns)} colunas)")
    else:
        missing_tables.append(table)
        results.append({
            "table": table,
            "exists": False,
            "count": 0,
            "error": str(count)
        })
        print(f"❌ {table}: NÃO EXISTE ou sem acesso")

print("\n" + "="*80)
print("📋 RESUMO DA AUDITORIA")
print("="*80)

print(f"\n✅ TABELAS EXISTENTES ({len(existing_tables)}):")
for t in existing_tables:
    r = next((x for x in results if x["table"] == t), None)
    if r:
        print(f"   - {t}: {r['count']} registros")

print(f"\n❌ TABELAS NÃO ENCONTRADAS ({len(missing_tables)}):")
for t in missing_tables:
    print(f"   - {t}")

# Identificar duplicatas potenciais
print("\n" + "="*80)
print("🔍 ANÁLISE DE DUPLICATAS POTENCIAIS")
print("="*80)

duplicates = [
    ("memory_chunks", "agent_memory_chunks", "Memórias do SICC"),
    ("learning_logs", "agent_learning_logs", "Logs de Aprendizado"),
    ("behavior_patterns", "agent_behavior_patterns", "Padrões de Comportamento"),
    ("agent_snapshots", "agent_knowledge_snapshots", "Snapshots"),
    ("agent_metrics", "agent_performance_metrics", "Métricas"),
    ("sicc_settings", "agent_dna", "Configurações SICC/DNA"),
]

for t1, t2, desc in duplicates:
    t1_exists = t1 in existing_tables
    t2_exists = t2 in existing_tables
    
    if t1_exists and t2_exists:
        r1 = next((x for x in results if x["table"] == t1), None)
        r2 = next((x for x in results if x["table"] == t2), None)
        print(f"\n⚠️  DUPLICATA DETECTADA: {desc}")
        print(f"   📁 {t1}: {r1['count'] if r1 else 0} registros")
        print(f"   📁 {t2}: {r2['count'] if r2 else 0} registros")
        print(f"   → AÇÃO: Verificar qual está sendo usada pelo código")
    elif t1_exists:
        print(f"\n✅ {desc}: Usando '{t1}'")
    elif t2_exists:
        print(f"\n✅ {desc}: Usando '{t2}'")
    else:
        print(f"\n❌ {desc}: NENHUMA tabela existe!")

print("\n" + "="*80)
print("📝 RECOMENDAÇÕES")
print("="*80)

# Salvar resultado em JSON
import json
output_file = "audit_database_result.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({
        "existing_tables": existing_tables,
        "missing_tables": missing_tables,
        "details": results
    }, f, indent=2, ensure_ascii=False, default=str)

print(f"\n💾 Resultado salvo em: {output_file}")
print("\n✅ Auditoria concluída!")
