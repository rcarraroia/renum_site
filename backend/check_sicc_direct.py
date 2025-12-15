#!/usr/bin/env python3
"""
Verificação Direta do Schema SICC
Usando queries diretas nas tabelas do information_schema
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from config.supabase import supabase_admin
    
    print("🔍 VERIFICAÇÃO DIRETA DO SCHEMA SICC")
    print("=" * 50)
    
    # Teste de conexão básico
    try:
        test_result = supabase_admin.table('profiles').select('id').limit(1).execute()
        print("✅ Conexão com Supabase: OK")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        sys.exit(1)
    
    # Lista das tabelas SICC esperadas
    expected_sicc_tables = [
        "agent_dna",
        "agent_memory_chunks", 
        "agent_behavior_patterns",
        "agent_learning_logs",
        "agent_knowledge_snapshots",
        "agent_performance_metrics",
        "agent_learning_settings"
    ]
    
    print(f"\n📊 Verificando {len(expected_sicc_tables)} tabelas SICC...")
    
    found_tables = []
    missing_tables = []
    
    # Verificar cada tabela individualmente
    for table_name in expected_sicc_tables:
        try:
            # Tentar fazer uma query simples na tabela
            result = supabase_admin.table(table_name).select('*').limit(1).execute()
            found_tables.append(table_name)
            
            # Contar registros
            count_result = supabase_admin.table(table_name).select('*', count='exact').execute()
            count = count_result.count or 0
            
            print(f"   ✅ {table_name} - {count} registros")
            
        except Exception as e:
            missing_tables.append(table_name)
            print(f"   ❌ {table_name} - ERRO: {str(e)[:50]}...")
    
    print(f"\n📈 Resultado: {len(found_tables)}/{len(expected_sicc_tables)} tabelas encontradas")
    
    if missing_tables:
        print(f"⚠️  Tabelas faltando: {missing_tables}")
    
    # Verificar estrutura da agent_memory_chunks (mais crítica para property tests)
    if 'agent_memory_chunks' in found_tables:
        print(f"\n🔍 Analisando agent_memory_chunks em detalhes...")
        
        # Verificar se há embeddings
        memory_sample = supabase_admin.table('agent_memory_chunks').select(
            'id, chunk_type, embedding, confidence_score, usage_count'
        ).limit(3).execute()
        
        if memory_sample.data:
            print(f"   📊 Amostra de {len(memory_sample.data)} registros:")
            
            chunk_types_found = set()
            has_embeddings = 0
            
            for i, record in enumerate(memory_sample.data, 1):
                chunk_type = record.get('chunk_type', 'NULL')
                chunk_types_found.add(chunk_type)
                
                embedding = record.get('embedding')
                has_embedding = "✅" if embedding else "❌"
                if embedding:
                    has_embeddings += 1
                
                confidence = record.get('confidence_score', 0)
                usage = record.get('usage_count', 0)
                
                print(f"      {i}. Type: {chunk_type}, Embedding: {has_embedding}, Conf: {confidence}, Usage: {usage}")
            
            print(f"   📝 Chunk types encontrados: {sorted(chunk_types_found)}")
            print(f"   🔧 Registros com embedding: {has_embeddings}/{len(memory_sample.data)}")
            
            # Verificar dimensão do embedding se existir
            if has_embeddings > 0:
                first_with_embedding = next(r for r in memory_sample.data if r.get('embedding'))
                embedding = first_with_embedding['embedding']
                
                if isinstance(embedding, list):
                    dimension = len(embedding)
                    print(f"   📏 Dimensão do embedding: {dimension}")
                    
                    if dimension == 384:
                        print("   ✅ Dimensão correta (GTE-small: 384)")
                    else:
                        print(f"   ⚠️  Dimensão inesperada: {dimension}")
                elif isinstance(embedding, str):
                    print(f"   📄 Embedding como string (pgvector format)")
                    try:
                        import json
                        parsed = json.loads(embedding)
                        dimension = len(parsed)
                        print(f"   📏 Dimensão: {dimension}")
                    except:
                        print("   ❌ Erro ao parsear embedding")
        else:
            print("   ⚠️  Nenhum registro encontrado")
    
    # Verificar agent_behavior_patterns
    if 'agent_behavior_patterns' in found_tables:
        print(f"\n🎯 Analisando agent_behavior_patterns...")
        
        patterns_sample = supabase_admin.table('agent_behavior_patterns').select(
            'id, pattern_type, success_rate, total_applications, is_active'
        ).limit(3).execute()
        
        if patterns_sample.data:
            pattern_types_found = set()
            
            for record in patterns_sample.data:
                pattern_type = record.get('pattern_type', 'NULL')
                pattern_types_found.add(pattern_type)
            
            print(f"   📝 Pattern types encontrados: {sorted(pattern_types_found)}")
        else:
            print("   ⚠️  Nenhum padrão encontrado")
    
    # Verificar IDs reais para testes
    print(f"\n🎯 Verificando IDs reais para testes...")
    
    # IDs do steering
    test_agent_id = "37ae9902-24bf-42b1-9d01-88c201ee0a6c"
    test_client_id = "9e26202e-7090-4051-9bfd-6b397b3947cc"
    test_profile_id = "876be331-9553-4e9a-9f29-63cfa711e056"
    
    # Verificar se existem
    try:
        profile_check = supabase_admin.table('profiles').select('id, role').eq('id', test_profile_id).execute()
        if profile_check.data:
            role = profile_check.data[0]['role']
            print(f"   ✅ Profile teste: {test_profile_id} (role: {role})")
        else:
            print(f"   ❌ Profile teste não encontrado: {test_profile_id}")
    except Exception as e:
        print(f"   ❌ Erro ao verificar profile: {e}")
    
    try:
        client_check = supabase_admin.table('clients').select('id, company_name').eq('id', test_client_id).execute()
        if client_check.data:
            company = client_check.data[0]['company_name']
            print(f"   ✅ Client teste: {test_client_id} ({company})")
        else:
            print(f"   ❌ Client teste não encontrado: {test_client_id}")
    except Exception as e:
        print(f"   ❌ Erro ao verificar client: {e}")
    
    # Verificar se há dados SICC para estes IDs
    sicc_data_count = 0
    for table in found_tables:
        try:
            if table in ['agent_memory_chunks', 'agent_behavior_patterns', 'agent_learning_logs', 
                        'agent_knowledge_snapshots', 'agent_performance_metrics']:
                
                agent_data = supabase_admin.table(table).select('id').eq('agent_id', test_agent_id).execute()
                count = len(agent_data.data) if agent_data.data else 0
                
                if count > 0:
                    sicc_data_count += count
                    print(f"   📊 {table}: {count} registros do agente teste")
        except:
            pass
    
    print(f"\n📊 Total de dados SICC do agente teste: {sicc_data_count} registros")
    
    # Resumo final
    print(f"\n" + "=" * 50)
    print(f"📋 RESUMO DA VERIFICAÇÃO:")
    print(f"   Tabelas SICC: {len(found_tables)}/{len(expected_sicc_tables)}")
    print(f"   Dados de teste: {sicc_data_count} registros")
    
    if len(found_tables) == len(expected_sicc_tables):
        print(f"   Status: ✅ SCHEMA COMPLETO")
        
        if sicc_data_count > 0:
            print(f"   Dados: ✅ DADOS DE TESTE DISPONÍVEIS")
            print(f"\n🎉 BANCO PRONTO PARA PROPERTY TESTS!")
        else:
            print(f"   Dados: ⚠️  POUCOS DADOS DE TESTE")
            print(f"\n⚠️  Recomendado: Criar mais dados de teste antes dos property tests")
    else:
        print(f"   Status: ❌ SCHEMA INCOMPLETO")
        print(f"\n❌ CORRIJA O SCHEMA ANTES DOS PROPERTY TESTS!")
    
except Exception as e:
    print(f"❌ ERRO GERAL: {e}")
    import traceback
    traceback.print_exc()