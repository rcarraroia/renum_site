#!/usr/bin/env python3
"""
Verificação do Schema SICC no Banco Real
Sprint 10 - Phase 5

Verifica o estado real das tabelas SICC no Supabase antes de implementar property tests.
Seguindo as regras de validação: NUNCA ASSUMA. SEMPRE VERIFIQUE.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config.supabase import supabase_admin
from utils.logger import logger


def verify_sicc_tables():
    """Verifica se todas as tabelas SICC existem e sua estrutura"""
    
    print("🔍 VERIFICAÇÃO DO SCHEMA SICC NO BANCO REAL")
    print("=" * 60)
    
    # Lista das tabelas SICC esperadas
    expected_tables = [
        "agent_dna",
        "agent_memory_chunks", 
        "agent_behavior_patterns",
        "agent_learning_logs",
        "agent_knowledge_snapshots",
        "agent_performance_metrics",
        "agent_learning_settings"
    ]
    
    try:
        # 1. Listar todas as tabelas públicas
        print("\n1️⃣ VERIFICANDO TABELAS EXISTENTES...")
        
        result = supabase_admin.rpc("exec_sql", {
            "query": """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
            """
        }).execute()
        
        existing_tables = [row["table_name"] for row in result.data]
        print(f"   📊 Total de tabelas no banco: {len(existing_tables)}")
        
        # Verificar quais tabelas SICC existem
        sicc_tables_found = []
        sicc_tables_missing = []
        
        for table in expected_tables:
            if table in existing_tables:
                sicc_tables_found.append(table)
                print(f"   ✅ {table}")
            else:
                sicc_tables_missing.append(table)
                print(f"   ❌ {table} - NÃO ENCONTRADA")
        
        print(f"\n   📈 SICC Tables: {len(sicc_tables_found)}/{len(expected_tables)} encontradas")
        
        if sicc_tables_missing:
            print(f"   ⚠️  TABELAS FALTANDO: {sicc_tables_missing}")
            return False
        
        # 2. Verificar estrutura de cada tabela SICC
        print("\n2️⃣ VERIFICANDO ESTRUTURA DAS TABELAS SICC...")
        
        for table in sicc_tables_found:
            print(f"\n   🔍 Analisando {table}:")
            
            # Verificar colunas
            columns_result = supabase_admin.rpc("exec_sql", {
                "query": f"""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = '{table}'
                ORDER BY ordinal_position;
                """
            }).execute()
            
            columns = columns_result.data
            print(f"      📋 Colunas ({len(columns)}):")
            for col in columns:
                nullable = "NULL" if col["is_nullable"] == "YES" else "NOT NULL"
                default = f" DEFAULT {col['column_default']}" if col["column_default"] else ""
                print(f"         - {col['column_name']}: {col['data_type']} {nullable}{default}")
            
            # Verificar RLS
            rls_result = supabase_admin.rpc("exec_sql", {
                "query": f"""
                SELECT tablename, rowsecurity 
                FROM pg_tables 
                WHERE tablename = '{table}';
                """
            }).execute()
            
            if rls_result.data:
                rls_enabled = rls_result.data[0]["rowsecurity"]
                rls_status = "✅ HABILITADO" if rls_enabled else "❌ DESABILITADO"
                print(f"      🔒 RLS: {rls_status}")
            
            # Verificar índices
            indexes_result = supabase_admin.rpc("exec_sql", {
                "query": f"""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = '{table}';
                """
            }).execute()
            
            indexes = indexes_result.data
            print(f"      📊 Índices ({len(indexes)}):")
            for idx in indexes:
                print(f"         - {idx['indexname']}")
        
        # 3. Verificar constraints específicas
        print("\n3️⃣ VERIFICANDO CONSTRAINTS ESPECÍFICAS...")
        
        # Verificar enums (se existirem)
        enums_result = supabase_admin.rpc("exec_sql", {
            "query": """
            SELECT typname, enumlabel 
            FROM pg_enum e 
            JOIN pg_type t ON e.enumtypid = t.oid 
            WHERE typname LIKE '%chunk_type%' OR typname LIKE '%pattern_type%' 
            ORDER BY typname, enumsortorder;
            """
        }).execute()
        
        if enums_result.data:
            print("      📝 Enums encontrados:")
            current_enum = None
            for enum_data in enums_result.data:
                if enum_data["typname"] != current_enum:
                    current_enum = enum_data["typname"]
                    print(f"         {current_enum}:")
                print(f"           - {enum_data['enumlabel']}")
        else:
            print("      ⚠️  Nenhum enum específico encontrado")
        
        # 4. Verificar dados de teste existentes
        print("\n4️⃣ VERIFICANDO DADOS EXISTENTES...")
        
        # IDs reais para testes (do steering)
        test_agent_id = "37ae9902-24bf-42b1-9d01-88c201ee0a6c"
        test_client_id = "9e26202e-7090-4051-9bfd-6b397b3947cc"
        
        for table in sicc_tables_found:
            try:
                count_result = supabase_admin.table(table).select("*", count="exact").execute()
                count = count_result.count or 0
                print(f"      📊 {table}: {count} registros")
                
                # Verificar se há dados do agente de teste
                if "agent_id" in [col["column_name"] for col in columns]:
                    agent_data = supabase_admin.table(table).select("*").eq(
                        "agent_id", test_agent_id
                    ).execute()
                    agent_count = len(agent_data.data) if agent_data.data else 0
                    if agent_count > 0:
                        print(f"         🎯 Dados do agente teste: {agent_count} registros")
                
            except Exception as e:
                print(f"      ❌ Erro ao contar {table}: {e}")
        
        print("\n✅ VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO NA VERIFICAÇÃO: {e}")
        return False


def verify_property_test_requirements():
    """Verifica requisitos específicos para property tests"""
    
    print("\n🧪 VERIFICAÇÃO DE REQUISITOS PARA PROPERTY TESTS")
    print("=" * 60)
    
    try:
        # Verificar se pgvector está instalado
        print("\n1️⃣ VERIFICANDO PGVECTOR...")
        
        vector_result = supabase_admin.rpc("exec_sql", {
            "query": "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
        }).execute()
        
        if vector_result.data:
            version = vector_result.data[0]["extversion"]
            print(f"   ✅ pgvector instalado: versão {version}")
        else:
            print("   ❌ pgvector NÃO instalado")
            return False
        
        # Verificar se há embeddings válidos
        print("\n2️⃣ VERIFICANDO EMBEDDINGS EXISTENTES...")
        
        memory_result = supabase_admin.table("agent_memory_chunks").select(
            "id, embedding"
        ).limit(5).execute()
        
        if memory_result.data:
            print(f"   📊 Encontradas {len(memory_result.data)} memórias com embeddings")
            
            # Verificar dimensão dos embeddings
            first_embedding = memory_result.data[0]["embedding"]
            if first_embedding:
                if isinstance(first_embedding, str):
                    # Parse pgvector format
                    import json
                    try:
                        embedding_list = json.loads(first_embedding)
                        dimension = len(embedding_list)
                        print(f"   📏 Dimensão dos embeddings: {dimension}")
                        
                        if dimension == 384:
                            print("   ✅ Dimensão correta (384)")
                        else:
                            print(f"   ⚠️  Dimensão inesperada: {dimension} (esperado: 384)")
                    except:
                        print("   ❌ Erro ao parsear embedding")
                elif isinstance(first_embedding, list):
                    dimension = len(first_embedding)
                    print(f"   📏 Dimensão dos embeddings: {dimension}")
        else:
            print("   ⚠️  Nenhuma memória com embedding encontrada")
        
        # Verificar constraints de enum
        print("\n3️⃣ VERIFICANDO VALORES DE ENUM...")
        
        # Chunk types
        chunk_types_result = supabase_admin.rpc("exec_sql", {
            "query": """
            SELECT DISTINCT chunk_type 
            FROM agent_memory_chunks 
            WHERE chunk_type IS NOT NULL;
            """
        }).execute()
        
        if chunk_types_result.data:
            chunk_types = [row["chunk_type"] for row in chunk_types_result.data]
            print(f"   📝 Chunk types em uso: {chunk_types}")
        
        # Pattern types  
        pattern_types_result = supabase_admin.rpc("exec_sql", {
            "query": """
            SELECT DISTINCT pattern_type 
            FROM agent_behavior_patterns 
            WHERE pattern_type IS NOT NULL;
            """
        }).execute()
        
        if pattern_types_result.data:
            pattern_types = [row["pattern_type"] for row in pattern_types_result.data]
            print(f"   🎯 Pattern types em uso: {pattern_types}")
        
        print("\n✅ REQUISITOS VERIFICADOS!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO NA VERIFICAÇÃO DE REQUISITOS: {e}")
        return False


def main():
    """Função principal"""
    
    print("🔍 VERIFICAÇÃO COMPLETA DO SCHEMA SICC")
    print("Seguindo regras de validação: NUNCA ASSUMA. SEMPRE VERIFIQUE.")
    print("=" * 80)
    
    # Verificar se conseguimos conectar
    try:
        test_result = supabase_admin.rpc("exec_sql", {
            "query": "SELECT NOW() as current_time;"
        }).execute()
        
        current_time = test_result.data[0]["current_time"]
        print(f"🔗 Conexão com Supabase: ✅ SUCESSO")
        print(f"⏰ Timestamp do banco: {current_time}")
        
    except Exception as e:
        print(f"❌ ERRO DE CONEXÃO: {e}")
        return False
    
    # Executar verificações
    schema_ok = verify_sicc_tables()
    requirements_ok = verify_property_test_requirements()
    
    print("\n" + "=" * 80)
    print("📋 RESUMO DA VERIFICAÇÃO:")
    print(f"   Schema SICC: {'✅ OK' if schema_ok else '❌ PROBLEMAS'}")
    print(f"   Requisitos Property Tests: {'✅ OK' if requirements_ok else '❌ PROBLEMAS'}")
    
    if schema_ok and requirements_ok:
        print("\n🎉 BANCO PRONTO PARA PROPERTY TESTS!")
        print("   Pode prosseguir com a implementação das Tasks 20, 22, 24, 26, 28")
        return True
    else:
        print("\n⚠️  PROBLEMAS ENCONTRADOS!")
        print("   Corrija os problemas antes de implementar property tests")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)