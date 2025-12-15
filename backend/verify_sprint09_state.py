"""
Script de Verificação de Estado Atual - Sprint 09
Verifica estrutura do banco de dados Supabase antes de criar SPEC
"""
import os
from supabase import create_client, Client
from datetime import datetime

# Credenciais
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# Conectar ao Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=" * 80)
print("VERIFICAÇÃO DE ESTADO ATUAL - SPRINT 09")
print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print()

# Lista de tabelas para verificar
tables_to_check = [
    'agents',
    'sub_agents',
    'conversations',
    'messages',
    'clients',
    'leads',
    'profiles',
    'projects',
    'renus_config',
    'tools'
]

results = {}

for table_name in tables_to_check:
    print(f"\n{'=' * 80}")
    print(f"TABELA: {table_name}")
    print('=' * 80)
    
    try:
        # 1. Verificar se tabela existe tentando fazer uma query
        result = supabase.table(table_name).select("*").limit(1).execute()
        
        print(f"✅ Tabela '{table_name}' EXISTE")
        
        # 2. Contar registros
        count_result = supabase.table(table_name).select("*", count="exact").execute()
        count = count_result.count if hasattr(count_result, 'count') else len(count_result.data)
        print(f"📊 Registros: {count}")
        
        # 3. Mostrar estrutura (primeiros registros)
        if count > 0:
            sample = supabase.table(table_name).select("*").limit(2).execute()
            print(f"\n📋 Exemplo de dados (primeiros 2 registros):")
            for i, record in enumerate(sample.data, 1):
                print(f"\nRegistro {i}:")
                for key, value in record.items():
                    # Truncar valores longos
                    str_value = str(value)
                    if len(str_value) > 100:
                        str_value = str_value[:100] + "..."
                    print(f"  - {key}: {str_value}")
        
        results[table_name] = {
            'exists': True,
            'count': count,
            'sample': sample.data if count > 0 else []
        }
        
    except Exception as e:
        error_msg = str(e)
        if "does not exist" in error_msg or "relation" in error_msg:
            print(f"❌ Tabela '{table_name}' NÃO EXISTE")
            results[table_name] = {'exists': False, 'error': error_msg}
        else:
            print(f"⚠️  Erro ao verificar '{table_name}': {error_msg}")
            results[table_name] = {'exists': 'unknown', 'error': error_msg}

# Verificar estrutura de colunas via SQL direto
print(f"\n\n{'=' * 80}")
print("VERIFICANDO ESTRUTURA DE COLUNAS (SQL)")
print('=' * 80)

for table_name in tables_to_check:
    if results.get(table_name, {}).get('exists') == True:
        print(f"\n--- Estrutura de {table_name} ---")
        try:
            # Query para pegar estrutura de colunas
            query = f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            AND table_schema = 'public'
            ORDER BY ordinal_position;
            """
            
            # Executar via RPC ou função
            # Como Supabase client não tem método direto para SQL arbitrário,
            # vamos usar o que conseguimos dos dados
            print("  (Estrutura inferida dos dados de exemplo)")
            if results[table_name].get('sample'):
                sample = results[table_name]['sample'][0]
                for key in sample.keys():
                    print(f"  - {key}")
                    
        except Exception as e:
            print(f"  ⚠️  Erro: {e}")

# Resumo final
print(f"\n\n{'=' * 80}")
print("RESUMO DA VERIFICAÇÃO")
print('=' * 80)

exists_count = sum(1 for r in results.values() if r.get('exists') == True)
not_exists_count = sum(1 for r in results.values() if r.get('exists') == False)
unknown_count = sum(1 for r in results.values() if r.get('exists') == 'unknown')

print(f"\n✅ Tabelas que EXISTEM: {exists_count}")
for table, data in results.items():
    if data.get('exists') == True:
        print(f"   - {table} ({data.get('count', 0)} registros)")

print(f"\n❌ Tabelas que NÃO EXISTEM: {not_exists_count}")
for table, data in results.items():
    if data.get('exists') == False:
        print(f"   - {table}")

if unknown_count > 0:
    print(f"\n⚠️  Tabelas com status DESCONHECIDO: {unknown_count}")
    for table, data in results.items():
        if data.get('exists') == 'unknown':
            print(f"   - {table}: {data.get('error', 'Erro desconhecido')}")

print(f"\n{'=' * 80}")
print("Verificação concluída!")
print(f"{'=' * 80}\n")
