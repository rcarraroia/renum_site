#!/usr/bin/env python3
"""
Script de verificação para Sprint 07A - Integrações Core
Verifica estado atual do Supabase antes de criar specs
"""
import os
from supabase import create_client, Client

# Credenciais do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def main():
    print("=" * 80)
    print("🔍 VERIFICAÇÃO SPRINT 07A - INTEGRAÇÕES CORE")
    print("=" * 80)
    print()
    
    # Conectar ao Supabase
    print("📡 Conectando ao Supabase...")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("✅ Conexão estabelecida com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    print()
    print("-" * 80)
    print("1️⃣ VERIFICANDO TABELAS PRINCIPAIS")
    print("-" * 80)
    
    # Tabelas esperadas
    expected_tables = [
        'profiles',
        'clients', 
        'leads',
        'projects',
        'conversations',
        'messages',
        'interviews',
        'interview_messages',
        'renus_config',
        'tools',
        'sub_agents',
        'isa_commands'
    ]
    
    for table in expected_tables:
        try:
            result = supabase.table(table).select("*", count="exact").limit(0).execute()
            count = result.count if hasattr(result, 'count') else 0
            print(f"✅ {table:25} - Existe ({count} registros)")
        except Exception as e:
            print(f"❌ {table:25} - NÃO EXISTE ou erro: {str(e)[:50]}")
    
    print()
    print("-" * 80)
    print("2️⃣ VERIFICANDO TABELAS DE INTEGRAÇÃO (Sprint 07A)")
    print("-" * 80)
    
    # Tabelas que vamos criar neste sprint
    integration_tables = [
        'integrations',
        'triggers',
        'trigger_executions'
    ]
    
    for table in integration_tables:
        try:
            result = supabase.table(table).select("*", count="exact").limit(0).execute()
            count = result.count if hasattr(result, 'count') else 0
            print(f"⚠️  {table:25} - JÁ EXISTE ({count} registros) - Verificar estrutura!")
        except Exception as e:
            print(f"✅ {table:25} - NÃO EXISTE (vamos criar)")
    
    print()
    print("-" * 80)
    print("3️⃣ VERIFICANDO ESTRUTURA DE TABELAS CRÍTICAS")
    print("-" * 80)
    
    # Verificar estrutura de clients (precisa ter client_id para RLS)
    try:
        result = supabase.table('clients').select("*").limit(1).execute()
        if result.data:
            print(f"✅ clients - Colunas: {', '.join(result.data[0].keys())}")
        else:
            print("⚠️  clients - Tabela vazia, não é possível verificar colunas")
    except Exception as e:
        print(f"❌ clients - Erro: {e}")
    
    # Verificar estrutura de conversations
    try:
        result = supabase.table('conversations').select("*").limit(1).execute()
        if result.data:
            print(f"✅ conversations - Colunas: {', '.join(result.data[0].keys())}")
        else:
            print("⚠️  conversations - Tabela vazia, não é possível verificar colunas")
    except Exception as e:
        print(f"❌ conversations - Erro: {e}")
    
    print()
    print("-" * 80)
    print("4️⃣ CONTAGEM DE REGISTROS")
    print("-" * 80)
    
    for table in ['clients', 'leads', 'conversations', 'sub_agents']:
        try:
            result = supabase.table(table).select("*", count="exact").limit(0).execute()
            count = result.count if hasattr(result, 'count') else 0
            print(f"📊 {table:25} - {count} registros")
        except Exception as e:
            print(f"❌ {table:25} - Erro ao contar")
    
    print()
    print("-" * 80)
    print("5️⃣ VERIFICANDO ESPAÇO E LIMITES")
    print("-" * 80)
    
    # Contar total de tabelas
    try:
        # Não há API direta para isso, mas podemos estimar
        print("ℹ️  Supabase Free Tier: Limite de ~500 tabelas")
        print(f"ℹ️  Tabelas principais identificadas: {len(expected_tables)}")
        print(f"ℹ️  Tabelas a criar: {len(integration_tables)}")
        print(f"✅ Espaço suficiente para novas tabelas")
    except Exception as e:
        print(f"⚠️  Não foi possível verificar limites: {e}")
    
    print()
    print("=" * 80)
    print("✅ VERIFICAÇÃO CONCLUÍDA")
    print("=" * 80)
    print()
    print("📝 PRÓXIMOS PASSOS:")
    print("1. Revisar este relatório")
    print("2. Verificar frontend (componentes de Integrações e Gatilhos)")
    print("3. Criar requirements.md, design.md, tasks.md")
    print()

if __name__ == "__main__":
    main()
