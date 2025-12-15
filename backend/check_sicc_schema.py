#!/usr/bin/env python3
"""
Verificação Rápida do Schema SICC
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from config.supabase import supabase_admin
    
    print("🔍 VERIFICAÇÃO RÁPIDA DO SCHEMA SICC")
    print("=" * 50)
    
    # Teste de conexão
    result = supabase_admin.rpc('exec_sql', {
        'query': 'SELECT NOW() as current_time;'
    }).execute()
    
    print(f"✅ Conexão OK: {result.data[0]['current_time']}")
    
    # Listar tabelas SICC
    tables_result = supabase_admin.rpc('exec_sql', {
        'query': """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'agent_%'
        ORDER BY table_name;
        """
    }).execute()
    
    print(f"\n📊 Tabelas SICC encontradas ({len(tables_result.data)}):")
    sicc_tables = []
    for table in tables_result.data:
        table_name = table['table_name']
        sicc_tables.append(table_name)
        print(f"   ✅ {table_name}")
    
    # Verificar estrutura da agent_memory_chunks (mais importante para property tests)
    if 'agent_memory_chunks' in sicc_tables:
        print(f"\n🔍 Estrutura da agent_memory_chunks:")
        
        columns_result = supabase_admin.rpc('exec_sql', {
            'query': """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'agent_memory_chunks'
            ORDER BY ordinal_position;
            """
        }).execute()
        
        for col in columns_result.data:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            print(f"   - {col['column_name']}: {col['data_type']} {nullable}")
        
        # Verificar se há dados
        count_result = supabase_admin.table('agent_memory_chunks').select('*', count='exact').execute()
        print(f"\n📊 Registros existentes: {count_result.count or 0}")
        
        # Verificar chunk_type values
        if count_result.count and count_result.count > 0:
            types_result = supabase_admin.rpc('exec_sql', {
                'query': """
                SELECT DISTINCT chunk_type 
                FROM agent_memory_chunks 
                WHERE chunk_type IS NOT NULL
                ORDER BY chunk_type;
                """
            }).execute()
            
            if types_result.data:
                chunk_types = [row['chunk_type'] for row in types_result.data]
                print(f"📝 Chunk types em uso: {chunk_types}")
    
    # Verificar pgvector
    vector_result = supabase_admin.rpc('exec_sql', {
        'query': "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
    }).execute()
    
    if vector_result.data:
        version = vector_result.data[0]['extversion']
        print(f"\n🔧 pgvector: ✅ v{version}")
    else:
        print(f"\n🔧 pgvector: ❌ NÃO INSTALADO")
    
    print(f"\n✅ VERIFICAÇÃO CONCLUÍDA!")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()