#!/usr/bin/env python3
"""
Script para verificar tabelas no Supabase
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
print("VERIFICAÇÃO DE TABELAS NO SUPABASE")
print("=" * 80)
print()

# Query para listar todas as tabelas
query = """
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
"""

try:
    # Executar query via RPC
    result = supabase.rpc('exec_sql', {'query': query}).execute()
    print("Tabelas encontradas:")
    print(result.data)
except Exception as e:
    print(f"Erro ao executar query: {e}")
    print()
    print("Tentando listar tabelas conhecidas...")
    
    # Lista de tabelas esperadas
    tables_to_check = [
        'profiles', 'clients', 'leads', 'projects', 'conversations', 
        'messages', 'interviews', 'agents', 'renus_config', 'tools',
        'sub_agents', 'knowledge_base', 'integrations', 'triggers',
        'webhooks', 'marketplace_templates', 'payments',
        # Tabelas SICC
        'memory_chunks', 'learning_logs', 'behavior_patterns',
        'agent_snapshots', 'sicc_settings', 'agent_metrics'
    ]
    
    print()
    print("Verificando tabelas conhecidas:")
    print("-" * 80)
    
    existing_tables = []
    missing_tables = []
    
    for table in tables_to_check:
        try:
            result = supabase.table(table).select("*").limit(1).execute()
            existing_tables.append(table)
            count_result = supabase.table(table).select("*", count="exact").execute()
            count = count_result.count if hasattr(count_result, 'count') else '?'
            print(f"✅ {table:30} - {count} registros")
        except Exception as e:
            missing_tables.append(table)
            print(f"❌ {table:30} - NÃO EXISTE")
    
    print()
    print("=" * 80)
    print(f"RESUMO:")
    print(f"  Tabelas existentes: {len(existing_tables)}")
    print(f"  Tabelas faltando:   {len(missing_tables)}")
    print("=" * 80)
    
    if missing_tables:
        print()
        print("Tabelas faltando:")
        for table in missing_tables:
            print(f"  - {table}")
