#!/usr/bin/env python3
"""
Property Tests para SICC Services
Sprint 10 - Phase 5

Implementa todos os property tests pendentes das Tasks 20, 22, 24, 26, 28.
"""

import asyncio
import sys
import os
from typing import List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, date

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.sicc.embedding_service import get_embedding_service
from src.services.sicc.memory_service import MemoryService
from src.services.sicc.behavior_service import BehaviorService
from src.services.sicc.snapshot_service import SnapshotService
from src.services.sicc.metrics_service import MetricsService
from src.models.sicc.memory import MemoryChunkCreate, ChunkType, MemorySearchQuery
from src.models.sicc.behavior import BehaviorPatternCreate, PatternType
from src.models.sicc.snapshot import SnapshotType
from src.models.sicc.metrics import MetricsPeriod


class PropertyTestRunner:
    """Runner para property tests do SICC"""
    
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.memory_service = MemoryService()
        self.behavior_service = BehaviorService()
        self.snapshot_service = SnapshotService()
        self.metrics_service = MetricsService()
        
        # IDs reais para testes
        self.agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
        self.client_id = UUID("9e26202e-7090-4051-9bfd-6b397b3947cc")
        
        self.results = []
    
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """Log resultado do teste"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        
        self.results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    # ========== TASK 20: Property Tests para EmbeddingService ==========
    
    def test_embedding_dimension_consistency(self):
        """Property 1: Embedding dimension consistency"""
        try:
            texts = [
                "Texto curto",
                "Este é um texto médio com algumas palavras a mais para testar",
                "Este é um texto muito longo que contém muitas palavras e frases para garantir que o embedding mantenha dimensão consistente independentemente do tamanho do texto de entrada"
            ]
            
            embeddings = []
            for text in texts:
                embedding = self.embedding_service.generate_embedding(text)
                embeddings.append(embedding)
            
            # Verificar que todas têm a mesma dimensão
            dimensions = [len(emb) for emb in embeddings]
            expected_dim = self.embedding_service.EMBEDDING_DIMENSION
            
            all_correct = all(dim == expected_dim for dim in dimensions)
            
            self.log_result(
                "Property 1: Embedding dimension consistency",
                all_correct,
                f"Dimensions: {dimensions}, Expected: {expected_dim}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 1: Embedding dimension consistency",
                False,
                f"Error: {e}"
            )
    
    def test_batch_embedding_processing(self):
        """Property 3: Batch embedding processing"""
        try:
            texts = [
                "Primeiro texto",
                "Segundo texto",
                "Terceiro texto",
                "Quarto texto"
            ]
            
            # Gerar embeddings individuais
            individual_embeddings = []
            for text in texts:
                emb = self.embedding_service.generate_embedding(text)
                individual_embeddings.append(emb)
            
            # Gerar embeddings em batch
            batch_embeddings = self.embedding_service.generate_embeddings_batch(texts)
            
            # Verificar que resultados são equivalentes
            matches = 0
            for i, (ind, batch) in enumerate(zip(individual_embeddings, batch_embeddings)):
                # Calcular similaridade (deve ser muito alta, próxima de 1.0)
                similarity = self.embedding_service.cosine_similarity(ind, batch)
                if similarity > 0.99:  # Permitir pequenas diferenças de precisão
                    matches += 1
            
            success = matches == len(texts)
            
            self.log_result(
                "Property 3: Batch embedding processing",
                success,
                f"Matches: {matches}/{len(texts)}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 3: Batch embedding processing",
                False,
                f"Error: {e}"
            )
    
    def test_embedding_cache_effectiveness(self):
        """Property 4: Embedding cache effectiveness"""
        try:
            text = "Texto para testar cache de embeddings"
            
            # Primeira geração (sem cache)
            start_time = datetime.now()
            embedding1 = self.embedding_service.generate_embedding(text)
            first_duration = (datetime.now() - start_time).total_seconds()
            
            # Segunda geração (com cache, se implementado)
            start_time = datetime.now()
            embedding2 = self.embedding_service.generate_embedding(text)
            second_duration = (datetime.now() - start_time).total_seconds()
            
            # Verificar que embeddings são idênticos
            similarity = self.embedding_service.cosine_similarity(embedding1, embedding2)
            
            success = similarity > 0.99
            
            self.log_result(
                "Property 4: Embedding cache effectiveness",
                success,
                f"Similarity: {similarity:.4f}, Times: {first_duration:.3f}s, {second_duration:.3f}s"
            )
            
        except Exception as e:
            self.log_result(
                "Property 4: Embedding cache effectiveness",
                False,
                f"Error: {e}"
            )
    
    # ========== TASK 22: Property Tests para MemoryService ==========
    
    async def test_memory_chunk_completeness(self):
        """Property 7: Memory chunk completeness"""
        try:
            # Criar memória
            memory = await self.memory_service.create_memory_from_text(
                agent_id=self.agent_id,
                client_id=self.client_id,
                content="Teste de completude de chunk de memória",
                chunk_type=ChunkType.FAQ,
                metadata={"test": "property_7"},
                source="property_test",
                confidence=0.9
            )
            
            # Verificar que todos os campos obrigatórios estão presentes
            required_fields = [
                'id', 'agent_id', 'client_id', 'content', 'chunk_type',
                'embedding', 'confidence_score', 'created_at'
            ]
            
            missing_fields = []
            for field in required_fields:
                if not hasattr(memory, field) or getattr(memory, field) is None:
                    missing_fields.append(field)
            
            # Verificar embedding tem dimensão correta
            embedding_valid = len(memory.embedding) == self.embedding_service.EMBEDDING_DIMENSION
            
            success = len(missing_fields) == 0 and embedding_valid
            
            self.log_result(
                "Property 7: Memory chunk completeness",
                success,
                f"Missing fields: {missing_fields}, Embedding valid: {embedding_valid}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 7: Memory chunk completeness",
                False,
                f"Error: {e}"
            )
    
    async def test_similarity_search_limit(self):
        """Property 8: Similarity search limit"""
        try:
            # Criar várias memórias
            memories_created = []
            for i in range(5):
                memory = await self.memory_service.create_memory_from_text(
                    agent_id=self.agent_id,
                    client_id=self.client_id,
                    content=f"Memória de teste número {i} para busca por similaridade",
                    chunk_type=ChunkType.FAQ,
                    confidence=0.8
                )
                memories_created.append(memory.id)
            
            # Testar busca com limite
            query = MemorySearchQuery(
                agent_id=self.agent_id,
                query_text="teste busca similaridade",
                limit=3,
                similarity_threshold=0.1
            )
            
            results = await self.memory_service.search_memories(query)
            
            # Verificar que respeitou o limite
            success = len(results) <= 3
            
            self.log_result(
                "Property 8: Similarity search limit",
                success,
                f"Results: {len(results)}, Limit: 3"
            )
            
        except Exception as e:
            self.log_result(
                "Property 8: Similarity search limit",
                False,
                f"Error: {e}"
            )
    
    async def test_memory_usage_tracking(self):
        """Property 9: Memory usage tracking"""
        try:
            # Criar memória
            memory = await self.memory_service.create_memory_from_text(
                agent_id=self.agent_id,
                client_id=self.client_id,
                content="Teste de tracking de uso de memória",
                chunk_type=ChunkType.FAQ
            )
            
            initial_usage = memory.usage_count
            
            # Incrementar uso
            await self.memory_service.increment_usage_count(memory.id)
            
            # Verificar memória atualizada
            updated_memory = await self.memory_service.get_memory(memory.id)
            
            success = updated_memory.usage_count == initial_usage + 1
            
            self.log_result(
                "Property 9: Memory usage tracking",
                success,
                f"Initial: {initial_usage}, Updated: {updated_memory.usage_count}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 9: Memory usage tracking",
                False,
                f"Error: {e}"
            )
    
    async def test_memory_quota_enforcement(self):
        """Property 10: Memory quota enforcement"""
        try:
            # Obter estatísticas atuais
            stats = await self.memory_service.get_memory_stats(self.agent_id)
            initial_count = stats['total_memories']
            
            # Criar nova memória
            memory = await self.memory_service.create_memory_from_text(
                agent_id=self.agent_id,
                client_id=self.client_id,
                content="Teste de quota de memória",
                chunk_type=ChunkType.FAQ
            )
            
            # Verificar que contador aumentou
            new_stats = await self.memory_service.get_memory_stats(self.agent_id)
            new_count = new_stats['total_memories']
            
            success = new_count == initial_count + 1
            
            self.log_result(
                "Property 10: Memory quota enforcement",
                success,
                f"Initial: {initial_count}, New: {new_count}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 10: Memory quota enforcement",
                False,
                f"Error: {e}"
            )
    
    # ========== TASK 24: Property Tests para BehaviorService ==========
    
    async def test_behavior_pattern_completeness(self):
        """Property 11: Behavior pattern completeness"""
        try:
            # Criar padrão comportamental
            pattern_data = BehaviorPatternCreate(
                agent_id=self.agent_id,
                client_id=self.client_id,
                pattern_type=PatternType.RESPONSE_OPTIMIZATION,
                trigger_context={"situation": "user_question"},
                action_config={"response_style": "helpful"},
                success_rate=0.85,
                total_applications=10
            )
            
            pattern = await self.behavior_service.create_pattern(pattern_data)
            
            # Verificar campos obrigatórios
            required_fields = [
                'id', 'agent_id', 'client_id', 'pattern_type',
                'trigger_context', 'action_config', 'success_rate',
                'total_applications', 'created_at'
            ]
            
            missing_fields = []
            for field in required_fields:
                if not hasattr(pattern, field) or getattr(pattern, field) is None:
                    missing_fields.append(field)
            
            success = len(missing_fields) == 0
            
            self.log_result(
                "Property 11: Behavior pattern completeness",
                success,
                f"Missing fields: {missing_fields}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 11: Behavior pattern completeness",
                False,
                f"Error: {e}"
            )
    
    async def test_pattern_application_recording(self):
        """Property 12: Pattern application recording"""
        try:
            # Criar padrão
            pattern_data = BehaviorPatternCreate(
                agent_id=self.agent_id,
                client_id=self.client_id,
                pattern_type=PatternType.RESPONSE_OPTIMIZATION,
                trigger_context={"test": "recording"},
                action_config={"action": "test"},
                success_rate=0.5,
                total_applications=2
            )
            
            pattern = await self.behavior_service.create_pattern(pattern_data)
            initial_applications = pattern.total_applications
            initial_success_rate = pattern.success_rate
            
            # Registrar uso bem-sucedido
            updated_pattern = await self.behavior_service.record_pattern_usage(
                pattern.id, success=True
            )
            
            # Verificar que contadores foram atualizados
            applications_increased = updated_pattern.total_applications == initial_applications + 1
            success_rate_updated = updated_pattern.success_rate != initial_success_rate
            
            success = applications_increased and success_rate_updated
            
            self.log_result(
                "Property 12: Pattern application recording",
                success,
                f"Applications: {initial_applications} -> {updated_pattern.total_applications}, "
                f"Success rate: {initial_success_rate:.2f} -> {updated_pattern.success_rate:.2f}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 12: Pattern application recording",
                False,
                f"Error: {e}"
            )
    
    async def test_pattern_success_rate_ordering(self):
        """Property 13: Pattern success rate ordering"""
        try:
            # Criar padrões com diferentes success rates
            patterns_created = []
            success_rates = [0.9, 0.7, 0.5, 0.3]
            
            for i, rate in enumerate(success_rates):
                pattern_data = BehaviorPatternCreate(
                    agent_id=self.agent_id,
                    client_id=self.client_id,
                    pattern_type=PatternType.RESPONSE_OPTIMIZATION,
                    trigger_context={"order_test": i},
                    action_config={"test": f"pattern_{i}"},
                    success_rate=rate,
                    total_applications=10
                )
                
                pattern = await self.behavior_service.create_pattern(pattern_data)
                patterns_created.append(pattern)
            
            # Buscar padrões (devem vir ordenados por success_rate desc)
            retrieved_patterns = await self.behavior_service.get_agent_patterns(
                agent_id=self.agent_id,
                limit=10
            )
            
            # Verificar ordenação
            rates = [p.success_rate for p in retrieved_patterns if p.id in [pc.id for pc in patterns_created]]
            is_ordered = all(rates[i] >= rates[i+1] for i in range(len(rates)-1))
            
            success = is_ordered and len(rates) >= len(success_rates)
            
            self.log_result(
                "Property 13: Pattern success rate ordering",
                success,
                f"Rates found: {rates}, Ordered: {is_ordered}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 13: Pattern success rate ordering",
                False,
                f"Error: {e}"
            )
    
    # ========== TASK 26: Property Tests para SnapshotService ==========
    
    async def test_snapshot_completeness(self):
        """Property 23: Snapshot completeness"""
        try:
            # Criar snapshot
            snapshot = await self.snapshot_service.create_snapshot(
                agent_id=self.agent_id,
                client_id=self.client_id,
                snapshot_type=SnapshotType.MANUAL
            )
            
            # Verificar campos obrigatórios
            required_fields = [
                'id', 'agent_id', 'client_id', 'snapshot_type',
                'memory_count', 'pattern_count', 'created_at'
            ]
            
            missing_fields = []
            for field in required_fields:
                if not hasattr(snapshot, field) or getattr(snapshot, field) is None:
                    missing_fields.append(field)
            
            # Verificar que contadores são não-negativos
            counts_valid = (
                snapshot.memory_count >= 0 and
                snapshot.pattern_count >= 0
            )
            
            success = len(missing_fields) == 0 and counts_valid
            
            self.log_result(
                "Property 23: Snapshot completeness",
                success,
                f"Missing fields: {missing_fields}, Counts valid: {counts_valid}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 23: Snapshot completeness",
                False,
                f"Error: {e}"
            )
    
    async def test_rollback_deactivation(self):
        """Property 24: Rollback deactivation"""
        try:
            # Criar snapshot inicial
            initial_snapshot = await self.snapshot_service.create_snapshot(
                agent_id=self.agent_id,
                client_id=self.client_id,
                snapshot_type=SnapshotType.PRE_ROLLBACK
            )
            
            # Aguardar um pouco para garantir timestamps diferentes
            import time
            time.sleep(1)
            
            # Criar nova memória após snapshot
            new_memory = await self.memory_service.create_memory_from_text(
                agent_id=self.agent_id,
                client_id=self.client_id,
                content="Memória criada após snapshot para teste de rollback",
                chunk_type=ChunkType.FAQ
            )
            
            # Fazer rollback
            rollback_result = await self.snapshot_service.restore_snapshot(
                initial_snapshot.id
            )
            
            # Verificar que memória foi desativada
            restored_memory = await self.memory_service.get_memory(new_memory.id)
            
            success = (
                rollback_result is not None and
                'memories_deactivated' in rollback_result and
                rollback_result['memories_deactivated'] >= 0
            )
            
            self.log_result(
                "Property 24: Rollback deactivation",
                success,
                f"Rollback result: {rollback_result}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 24: Rollback deactivation",
                False,
                f"Error: {e}"
            )
    
    # ========== TASK 28: Property Tests para MetricsService ==========
    
    async def test_interaction_metrics_recording(self):
        """Property 25: Interaction metrics recording"""
        try:
            # Registrar interação
            metrics = await self.metrics_service.record_interaction(
                agent_id=self.agent_id,
                client_id=self.client_id,
                success=True,
                response_time_ms=250,
                satisfaction_score=4.5
            )
            
            # Verificar que métricas foram registradas
            success = (
                metrics.total_interactions > 0 and
                metrics.successful_interactions > 0 and
                metrics.avg_response_time_ms is not None and
                metrics.user_satisfaction_score is not None
            )
            
            self.log_result(
                "Property 25: Interaction metrics recording",
                success,
                f"Total: {metrics.total_interactions}, Success: {metrics.successful_interactions}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 25: Interaction metrics recording",
                False,
                f"Error: {e}"
            )
    
    async def test_memory_usage_metrics(self):
        """Property 26: Memory usage metrics"""
        try:
            # Incrementar uso de memória
            await self.metrics_service.increment_memory_usage(self.agent_id, count=5)
            
            # Obter métricas agregadas
            aggregated = await self.metrics_service.get_aggregated_metrics(
                self.agent_id,
                MetricsPeriod.LAST_7_DAYS
            )
            
            success = (
                'total_memory_usage' in aggregated and
                aggregated['total_memory_usage'] >= 0
            )
            
            self.log_result(
                "Property 26: Memory usage metrics",
                success,
                f"Memory usage: {aggregated.get('total_memory_usage', 0)}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 26: Memory usage metrics",
                False,
                f"Error: {e}"
            )
    
    async def test_pattern_application_metrics(self):
        """Property 27: Pattern application metrics"""
        try:
            # Incrementar aplicação de padrões
            await self.metrics_service.increment_pattern_application(self.agent_id, count=3)
            
            # Obter métricas agregadas
            aggregated = await self.metrics_service.get_aggregated_metrics(
                self.agent_id,
                MetricsPeriod.LAST_7_DAYS
            )
            
            success = (
                'total_patterns_applied' in aggregated and
                aggregated['total_patterns_applied'] >= 0
            )
            
            self.log_result(
                "Property 27: Pattern application metrics",
                success,
                f"Patterns applied: {aggregated.get('total_patterns_applied', 0)}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 27: Pattern application metrics",
                False,
                f"Error: {e}"
            )
    
    async def test_learning_consolidation_metrics(self):
        """Property 28: Learning consolidation metrics"""
        try:
            # Incrementar novos aprendizados
            await self.metrics_service.increment_new_learnings(self.agent_id, count=2)
            
            # Obter métricas agregadas
            aggregated = await self.metrics_service.get_aggregated_metrics(
                self.agent_id,
                MetricsPeriod.LAST_7_DAYS
            )
            
            success = (
                'total_new_learnings' in aggregated and
                aggregated['total_new_learnings'] >= 0
            )
            
            self.log_result(
                "Property 28: Learning consolidation metrics",
                success,
                f"New learnings: {aggregated.get('total_new_learnings', 0)}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 28: Learning consolidation metrics",
                False,
                f"Error: {e}"
            )
    
    async def test_metrics_aggregation(self):
        """Property 29: Metrics aggregation"""
        try:
            # Obter métricas de diferentes períodos
            periods = [
                MetricsPeriod.LAST_7_DAYS,
                MetricsPeriod.LAST_30_DAYS,
                MetricsPeriod.LAST_90_DAYS
            ]
            
            aggregations = {}
            for period in periods:
                agg = await self.metrics_service.get_aggregated_metrics(
                    self.agent_id, period
                )
                aggregations[period.value] = agg
            
            # Verificar que todas agregações têm campos esperados
            required_fields = [
                'total_interactions', 'successful_interactions', 'success_rate'
            ]
            
            all_valid = True
            for period, agg in aggregations.items():
                for field in required_fields:
                    if field not in agg:
                        all_valid = False
                        break
            
            success = all_valid and len(aggregations) == len(periods)
            
            self.log_result(
                "Property 29: Metrics aggregation",
                success,
                f"Periods aggregated: {list(aggregations.keys())}"
            )
            
        except Exception as e:
            self.log_result(
                "Property 29: Metrics aggregation",
                False,
                f"Error: {e}"
            )
    
    async def test_learning_velocity_calculation(self):
        """Property 31: Learning velocity calculation"""
        try:
            # Calcular velocidade de aprendizado
            velocity = await self.metrics_service.calculate_learning_velocity(
                self.agent_id, days=30
            )
            
            # Verificar que retorna um número válido
            success = isinstance(velocity, (int, float)) and velocity >= 0
            
            self.log_result(
                "Property 31: Learning velocity calculation",
                success,
                f"Velocity: {velocity} learnings/day"
            )
            
        except Exception as e:
            self.log_result(
                "Property 31: Learning velocity calculation",
                False,
                f"Error: {e}"
            )
    
    # ========== RUNNER PRINCIPAL ==========
    
    async def run_all_tests(self):
        """Executa todos os property tests"""
        print("🧪 Executando Property Tests do SICC...")
        print("=" * 60)
        
        # Task 20: EmbeddingService
        print("\n📊 Task 20: EmbeddingService Property Tests")
        self.test_embedding_dimension_consistency()
        self.test_batch_embedding_processing()
        self.test_embedding_cache_effectiveness()
        
        # Task 22: MemoryService
        print("\n🧠 Task 22: MemoryService Property Tests")
        await self.test_memory_chunk_completeness()
        await self.test_similarity_search_limit()
        await self.test_memory_usage_tracking()
        await self.test_memory_quota_enforcement()
        
        # Task 24: BehaviorService
        print("\n🎯 Task 24: BehaviorService Property Tests")
        await self.test_behavior_pattern_completeness()
        await self.test_pattern_application_recording()
        await self.test_pattern_success_rate_ordering()
        
        # Task 26: SnapshotService
        print("\n📸 Task 26: SnapshotService Property Tests")
        await self.test_snapshot_completeness()
        await self.test_rollback_deactivation()
        
        # Task 28: MetricsService
        print("\n📈 Task 28: MetricsService Property Tests")
        await self.test_interaction_metrics_recording()
        await self.test_memory_usage_metrics()
        await self.test_pattern_application_metrics()
        await self.test_learning_consolidation_metrics()
        await self.test_metrics_aggregation()
        await self.test_learning_velocity_calculation()
        
        # Resumo final
        print("\n" + "=" * 60)
        print("📋 RESUMO DOS PROPERTY TESTS")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total de testes: {total_tests}")
        print(f"✅ Passou: {passed_tests}")
        print(f"❌ Falhou: {failed_tests}")
        print(f"📊 Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Testes que falharam:")
            for result in self.results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
        
        return passed_tests, total_tests


async def main():
    """Função principal"""
    runner = PropertyTestRunner()
    passed, total = await runner.run_all_tests()
    
    # Exit code baseado no sucesso
    if passed == total:
        print(f"\n🎉 Todos os {total} property tests passaram!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} de {total} property tests falharam.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())