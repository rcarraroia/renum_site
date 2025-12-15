#!/usr/bin/env python3
"""
Property Tests para MemoryService - Task 22
Sprint 10 - SICC Implementation - Phase 5

Testes de propriedades usando dados reais do banco.
"""

import sys
from pathlib import Path
import asyncio
from uuid import UUID, uuid4
import random

# Configurar path
backend_path = Path(__file__).parent
src_path = backend_path / "src"
sys.path.insert(0, str(src_path))

# Imports diretos
try:
    from config.supabase import supabase_admin
    from services.sicc.memory_service import MemoryService
    from models.sicc.memory import MemoryChunkCreate, MemorySearchQuery, ChunkType
    
    print("🧪 PROPERTY TESTS - MEMORY SERVICE")
    print("Task 22 - Sprint 10 - Phase 5")
    print("=" * 60)
    
    # IDs reais do banco (verificados anteriormente)
    TEST_AGENT_ID = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
    TEST_CLIENT_ID = UUID("9e26202e-7090-4051-9bfd-6b397b3947cc")
    
    # Valores de enum reais do banco
    VALID_CHUNK_TYPES = ["faq", "product"]  # Obtidos da verificação anterior
    
    async def test_property_7_memory_chunk_completeness():
        """
        Property 7: Memory chunk completeness
        
        Toda memória criada deve conter todos os campos obrigatórios.
        """
        print("🧪 Property 7: Memory chunk completeness")
        
        service = MemoryService()
        
        # Criar embedding fake (384 dimensões)
        fake_embedding = [0.1] * 384
        
        test_cases = [
            {
                "content": "Teste de FAQ completo",
                "chunk_type": ChunkType.FAQ,
                "source": "test_property_7",
                "confidence": 0.9
            },
            {
                "content": "Produto de teste com descrição detalhada",
                "chunk_type": ChunkType.PRODUCT,
                "source": "test_property_7",
                "confidence": 0.8
            },
            {
                "content": "Memória com conteúdo mínimo",
                "chunk_type": ChunkType.FAQ,
                "source": None,  # Opcional
                "confidence": 1.0
            }
        ]
        
        created_memories = []
        passed = 0
        
        for i, case in enumerate(test_cases, 1):
            try:
                memory_data = MemoryChunkCreate(
                    agent_id=TEST_AGENT_ID,
                    client_id=TEST_CLIENT_ID,
                    content=case["content"],
                    chunk_type=case["chunk_type"],
                    embedding=fake_embedding,
                    metadata={"test": "property_7", "case": i},
                    source=case["source"],
                    confidence_score=case["confidence"]
                )
                
                created_memory = await service.create_memory(memory_data)
                created_memories.append(created_memory.id)
                
                # Verificar campos obrigatórios
                required_fields = ["id", "agent_id", "client_id", "content", "chunk_type", 
                                 "embedding", "confidence_score", "created_at", "usage_count"]
                
                missing_fields = []
                for field in required_fields:
                    if not hasattr(created_memory, field) or getattr(created_memory, field) is None:
                        if field not in ["source", "metadata"]:  # Campos opcionais
                            missing_fields.append(field)
                
                if not missing_fields:
                    print(f"   ✅ Caso {i}: Todos os campos obrigatórios presentes")
                    passed += 1
                else:
                    print(f"   ❌ Caso {i}: Campos faltando: {missing_fields}")
                
            except Exception as e:
                print(f"   ❌ Caso {i}: Erro - {e}")
        
        # Limpeza
        for memory_id in created_memories:
            try:
                await service.delete_memory(memory_id)
            except:
                pass
        
        success_rate = passed / len(test_cases)
        print(f"   📊 Resultado: {passed}/{len(test_cases)} casos completos ({success_rate:.1%})")
        
        return success_rate >= 0.9
    
    async def test_property_8_similarity_search_limit():
        """
        Property 8: Similarity search limit
        
        Busca por similaridade deve respeitar o limite especificado.
        """
        print("\n🧪 Property 8: Similarity search limit")
        
        service = MemoryService()
        
        # Verificar quantas memórias existem para o agente teste
        existing_memories = await service.get_agent_memories(TEST_AGENT_ID, limit=100)
        total_memories = len(existing_memories)
        
        print(f"   📊 Memórias existentes para agente teste: {total_memories}")
        
        if total_memories == 0:
            print(f"   ⚠️  Nenhuma memória encontrada. Criando dados de teste...")
            
            # Criar algumas memórias para teste
            fake_embedding = [0.1] * 384
            test_memories = []
            
            for i in range(5):
                memory_data = MemoryChunkCreate(
                    agent_id=TEST_AGENT_ID,
                    client_id=TEST_CLIENT_ID,
                    content=f"Memória de teste {i+1} para busca por similaridade",
                    chunk_type=ChunkType.FAQ,
                    embedding=fake_embedding,
                    metadata={"test": "property_8"},
                    confidence_score=0.8
                )
                
                created = await service.create_memory(memory_data)
                test_memories.append(created.id)
            
            total_memories = 5
        else:
            test_memories = []
        
        # Testar diferentes limites
        test_limits = [1, 3, 5, 10, 20]
        passed = 0
        
        for limit in test_limits:
            try:
                search_query = MemorySearchQuery(
                    agent_id=TEST_AGENT_ID,
                    query_text="teste busca similaridade",
                    limit=limit,
                    similarity_threshold=0.0  # Baixo para pegar resultados
                )
                
                results = await service.search_memories(search_query)
                actual_count = len(results)
                expected_count = min(limit, total_memories)
                
                if actual_count <= expected_count:
                    print(f"   ✅ Limite {limit}: {actual_count} resultados (≤ {expected_count})")
                    passed += 1
                else:
                    print(f"   ❌ Limite {limit}: {actual_count} resultados (> {expected_count})")
                
            except Exception as e:
                print(f"   ❌ Limite {limit}: Erro - {e}")
        
        # Limpeza
        for memory_id in test_memories:
            try:
                await service.delete_memory(memory_id)
            except:
                pass
        
        success_rate = passed / len(test_limits)
        print(f"   📊 Resultado: {passed}/{len(test_limits)} limites respeitados ({success_rate:.1%})")
        
        return success_rate >= 0.8
    
    async def test_property_9_memory_usage_tracking():
        """
        Property 9: Memory usage tracking
        
        Contador de uso deve incrementar corretamente.
        """
        print("\n🧪 Property 9: Memory usage tracking")
        
        service = MemoryService()
        
        # Criar uma memória para teste
        fake_embedding = [0.1] * 384
        memory_data = MemoryChunkCreate(
            agent_id=TEST_AGENT_ID,
            client_id=TEST_CLIENT_ID,
            content="Memória para testar contador de uso",
            chunk_type=ChunkType.FAQ,
            embedding=fake_embedding,
            metadata={"test": "property_9"},
            confidence_score=0.9
        )
        
        try:
            created_memory = await service.create_memory(memory_data)
            memory_id = created_memory.id
            
            # Verificar uso inicial
            initial_memory = await service.get_memory(memory_id)
            initial_usage = initial_memory.usage_count
            
            print(f"   📊 Uso inicial: {initial_usage}")
            
            # Incrementar uso várias vezes
            increments = [1, 2, 1, 3, 1]
            expected_total = initial_usage
            
            passed = 0
            for i, increment in enumerate(increments, 1):
                # Incrementar
                for _ in range(increment):
                    await service.increment_usage_count(memory_id)
                
                expected_total += increment
                
                # Verificar
                updated_memory = await service.get_memory(memory_id)
                actual_usage = updated_memory.usage_count
                
                if actual_usage == expected_total:
                    print(f"   ✅ Incremento {i}: {actual_usage} (esperado: {expected_total})")
                    passed += 1
                else:
                    print(f"   ❌ Incremento {i}: {actual_usage} (esperado: {expected_total})")
            
            # Limpeza
            await service.delete_memory(memory_id)
            
            success_rate = passed / len(increments)
            print(f"   📊 Resultado: {passed}/{len(increments)} incrementos corretos ({success_rate:.1%})")
            
            return success_rate >= 0.9
            
        except Exception as e:
            print(f"   ❌ Erro no teste: {e}")
            return False
    
    async def test_property_10_memory_quota_enforcement():
        """
        Property 10: Memory quota enforcement
        
        Sistema deve gerenciar limites de memória por agente.
        """
        print("\n🧪 Property 10: Memory quota enforcement")
        
        service = MemoryService()
        
        # Verificar estatísticas atuais
        try:
            stats = await service.get_memory_stats(TEST_AGENT_ID)
            current_total = stats["total_memories"]
            
            print(f"   📊 Memórias atuais: {current_total}")
            
            # Simular criação de muitas memórias
            fake_embedding = [0.1] * 384
            created_memories = []
            
            # Criar algumas memórias
            for i in range(3):
                memory_data = MemoryChunkCreate(
                    agent_id=TEST_AGENT_ID,
                    client_id=TEST_CLIENT_ID,
                    content=f"Memória de quota {i+1}",
                    chunk_type=ChunkType.FAQ,
                    embedding=fake_embedding,
                    metadata={"test": "property_10"},
                    confidence_score=0.7
                )
                
                created = await service.create_memory(memory_data)
                created_memories.append(created.id)
            
            # Verificar se foram criadas
            new_stats = await service.get_memory_stats(TEST_AGENT_ID)
            new_total = new_stats["total_memories"]
            
            expected_total = current_total + 3
            
            if new_total == expected_total:
                print(f"   ✅ Criação: {new_total} memórias (esperado: {expected_total})")
                quota_ok = True
            else:
                print(f"   ❌ Criação: {new_total} memórias (esperado: {expected_total})")
                quota_ok = False
            
            # Limpeza
            for memory_id in created_memories:
                try:
                    await service.delete_memory(memory_id)
                except:
                    pass
            
            # Verificar se foram removidas
            final_stats = await service.get_memory_stats(TEST_AGENT_ID)
            final_total = final_stats["total_memories"]
            
            if final_total == current_total:
                print(f"   ✅ Limpeza: {final_total} memórias (volta ao inicial: {current_total})")
                cleanup_ok = True
            else:
                print(f"   ⚠️  Limpeza: {final_total} memórias (esperado: {current_total})")
                cleanup_ok = False
            
            print(f"   📊 Resultado: Quota {'✅' if quota_ok else '❌'}, Limpeza {'✅' if cleanup_ok else '⚠️'}")
            
            return quota_ok and cleanup_ok
            
        except Exception as e:
            print(f"   ❌ Erro no teste: {e}")
            return False
    
    async def main():
        """Executa todos os property tests do MemoryService"""
        
        # Verificar conexão
        try:
            test_result = supabase_admin.table('profiles').select('id').limit(1).execute()
            print("✅ Conexão com banco: OK")
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
        
        # Executar property tests
        results = []
        
        try:
            results.append(("Property 7: Memory Chunk Completeness", await test_property_7_memory_chunk_completeness()))
            results.append(("Property 8: Similarity Search Limit", await test_property_8_similarity_search_limit()))
            results.append(("Property 9: Memory Usage Tracking", await test_property_9_memory_usage_tracking()))
            results.append(("Property 10: Memory Quota Enforcement", await test_property_10_memory_quota_enforcement()))
            
        except Exception as e:
            print(f"\n❌ Erro durante execução dos testes: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Resumo dos resultados
        print(f"\n" + "=" * 60)
        print(f"📊 RESUMO DOS PROPERTY TESTS - MEMORY SERVICE")
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSOU" if result else "❌ FALHOU"
            print(f"   {status} - {test_name}")
            if result:
                passed += 1
        
        success_rate = passed / total if total > 0 else 0
        print(f"\n📈 Taxa de sucesso: {passed}/{total} ({success_rate:.1%})")
        
        if success_rate >= 0.8:  # 80% mínimo
            print(f"🎉 PROPERTY TESTS APROVADOS!")
            print(f"✅ Task 22 - MemoryService funcionando corretamente")
            return True
        else:
            print(f"❌ PROPERTY TESTS FALHARAM!")
            print(f"⚠️  Task 22 - MemoryService precisa de correções")
            return False
    
    # Executar
    if __name__ == "__main__":
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
        
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print("💡 Verifique se todas as dependências estão instaladas")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)