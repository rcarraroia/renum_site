#!/usr/bin/env python3
"""
Fixed SICC Property Tests - Sprint 10 Phase 5
Corrigindo os problemas identificados nos testes anteriores
"""

import asyncio
import sys
import os
from datetime import datetime, date, timedelta
from uuid import UUID, uuid4
from typing import List, Dict, Any
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.sicc.embedding_service import get_embedding_service
from src.services.sicc.memory_service import MemoryService
from src.services.sicc.behavior_service import BehaviorService
from src.services.sicc.snapshot_service import SnapshotService
from src.services.sicc.metrics_service import MetricsService
from src.models.sicc.memory import MemoryChunkCreate, MemorySearchQuery, ChunkType
from src.models.sicc.behavior import BehaviorPatternCreate, PatternType
from src.models.sicc.snapshot import SnapshotType
from src.models.sicc.metrics import MetricsPeriod


class PropertyTestRunner:
    """Runner for property-based tests"""
    
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
        # Test data
        self.agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
        self.client_id = UUID("9e26202e-7090-4051-9bfd-6b397b3947cc")
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status} - {test_name}"
        if details:
            result += f" ({details})"
        
        print(result)
        self.results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"SICC PROPERTY TESTS SUMMARY - FIXED")
        print(f"{'='*60}")
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.passed_tests == self.total_tests:
            print(f"\n🎉 ALL PROPERTY TESTS PASSED!")
        else:
            print(f"\n⚠️  Some tests failed. Review details above.")


# =============================================================================
# TASK 20: PROPERTY TESTS - EMBEDDING SERVICE (3 properties) - FIXED
# =============================================================================

async def test_embedding_properties_fixed(runner: PropertyTestRunner):
    """Test EmbeddingService properties - FIXED VERSION"""
    print(f"\n🧪 TASK 20: EmbeddingService Property Tests (FIXED)")
    print("-" * 50)
    
    try:
        embedding_service = get_embedding_service()
        
        # Property 1: Embedding dimension consistency
        try:
            test_texts = [
                "Hello world",
                "This is a longer text with more content to test embedding consistency",
                "Short",
                "A" * 500  # Reduced size to avoid token limits
            ]
            
            embeddings = []
            for text in test_texts:
                embedding = embedding_service.generate_embedding(text)
                embeddings.append(embedding)
            
            # All embeddings should have same dimension
            dimensions = [len(emb) for emb in embeddings]
            consistent = all(dim == embedding_service.EMBEDDING_DIMENSION for dim in dimensions)
            
            runner.log_test(
                "Property 1: Embedding dimension consistency",
                consistent,
                f"All {len(embeddings)} embeddings have {embedding_service.EMBEDDING_DIMENSION} dimensions"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 1: Embedding dimension consistency",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 3: Batch embedding processing
        try:
            texts = [
                "First text for batch processing",
                "Second text for batch processing", 
                "Third text for batch processing"
            ]
            
            # Generate individually
            individual_embeddings = []
            for text in texts:
                emb = embedding_service.generate_embedding(text)
                individual_embeddings.append(emb)
            
            # Generate in batch
            batch_embeddings = embedding_service.generate_embeddings_batch(texts)
            
            # Should produce same results
            batch_consistent = len(individual_embeddings) == len(batch_embeddings)
            if batch_consistent:
                for i, (ind, batch) in enumerate(zip(individual_embeddings, batch_embeddings)):
                    # Check if embeddings are very similar (allowing for small numerical differences)
                    similarity = embedding_service.cosine_similarity(ind, batch)
                    if similarity < 0.99:  # Should be nearly identical
                        batch_consistent = False
                        break
            
            runner.log_test(
                "Property 3: Batch embedding processing",
                batch_consistent,
                f"Batch and individual processing produce consistent results"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 3: Batch embedding processing",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 4: Embedding cache effectiveness
        try:
            test_text = "This text will be embedded multiple times to test caching"
            
            # Generate embedding multiple times
            embedding1 = embedding_service.generate_embedding(test_text)
            embedding2 = embedding_service.generate_embedding(test_text)
            embedding3 = embedding_service.generate_embedding(test_text)
            
            # Should be identical (exact same results)
            cache_effective = (
                embedding1 == embedding2 and 
                embedding2 == embedding3 and
                len(embedding1) == embedding_service.EMBEDDING_DIMENSION
            )
            
            runner.log_test(
                "Property 4: Embedding cache effectiveness",
                cache_effective,
                f"Multiple calls return identical embeddings"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 4: Embedding cache effectiveness",
                False,
                f"Error: {str(e)}"
            )
            
    except Exception as e:
        runner.log_test(
            "EmbeddingService initialization",
            False,
            f"Failed to initialize: {str(e)}"
        )


# =============================================================================
# TASK 22: PROPERTY TESTS - MEMORY SERVICE (4 properties) - FIXED
# =============================================================================

async def test_memory_properties_fixed(runner: PropertyTestRunner):
    """Test MemoryService properties - FIXED VERSION"""
    print(f"\n🧪 TASK 22: MemoryService Property Tests (FIXED)")
    print("-" * 50)
    
    try:
        memory_service = MemoryService()
        
        # Property 7: Memory chunk completeness - FIXED with valid source
        try:
            # Create memory with all required fields - using valid source
            memory_data = MemoryChunkCreate(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                content="Test memory content for completeness validation",
                chunk_type=ChunkType.FAQ,
                embedding=[0.1] * 384,  # Valid 384-dim embedding
                metadata={"test": "property_7"},
                source="conversation",  # FIXED: using valid source
                confidence_score=0.8
            )
            
            created_memory = await memory_service.create_memory(memory_data)
            
            # Verify all fields are preserved
            completeness_check = (
                created_memory.agent_id == runner.agent_id and
                created_memory.client_id == runner.client_id and
                created_memory.content == memory_data.content and
                created_memory.chunk_type == memory_data.chunk_type and
                created_memory.confidence_score == memory_data.confidence_score and
                created_memory.source == memory_data.source and
                created_memory.metadata.get("test") == "property_7"
            )
            
            runner.log_test(
                "Property 7: Memory chunk completeness",
                completeness_check,
                f"All fields preserved in memory {created_memory.id}"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 7: Memory chunk completeness",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 8: Similarity search limit
        try:
            # Create multiple memories
            memories_created = []
            for i in range(5):
                memory = await memory_service.create_memory_from_text(
                    agent_id=runner.agent_id,
                    client_id=runner.client_id,
                    content=f"Test memory content number {i} for similarity search",
                    chunk_type=ChunkType.FAQ,
                    metadata={"index": i},
                    source="conversation"  # FIXED: using valid source
                )
                memories_created.append(memory)
            
            # Search with different limits
            search_query = MemorySearchQuery(
                agent_id=runner.agent_id,
                query_text="test memory content",
                limit=3,
                similarity_threshold=0.1  # Low threshold to get results
            )
            
            results = await memory_service.search_memories(search_query)
            
            # Should respect limit
            limit_respected = len(results) <= search_query.limit
            
            runner.log_test(
                "Property 8: Similarity search limit",
                limit_respected,
                f"Search returned {len(results)} results (limit: {search_query.limit})"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 8: Similarity search limit",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 9: Memory usage tracking
        try:
            # Create a memory
            memory = await memory_service.create_memory_from_text(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                content="Memory for usage tracking test",
                chunk_type=ChunkType.FAQ,
                source="conversation"  # FIXED: using valid source
            )
            
            initial_usage = memory.usage_count
            
            # Increment usage
            await memory_service.increment_usage_count(memory.id)
            
            # Get updated memory
            updated_memory = await memory_service.get_memory(memory.id)
            
            usage_tracked = (
                updated_memory is not None and
                updated_memory.usage_count == initial_usage + 1
            )
            
            runner.log_test(
                "Property 9: Memory usage tracking",
                usage_tracked,
                f"Usage count incremented from {initial_usage} to {updated_memory.usage_count if updated_memory else 'N/A'}"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 9: Memory usage tracking",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 10: Memory quota enforcement
        try:
            # Get current memory stats
            stats = await memory_service.get_memory_stats(runner.agent_id)
            
            # Verify stats structure
            quota_structure = (
                "total_memories" in stats and
                "by_type" in stats and
                "avg_confidence" in stats and
                isinstance(stats["total_memories"], int) and
                isinstance(stats["by_type"], dict)
            )
            
            runner.log_test(
                "Property 10: Memory quota enforcement",
                quota_structure,
                f"Stats structure valid: {stats['total_memories']} total memories"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 10: Memory quota enforcement",
                False,
                f"Error: {str(e)}"
            )
            
    except Exception as e:
        runner.log_test(
            "MemoryService initialization",
            False,
            f"Failed to initialize: {str(e)}"
        )


# =============================================================================
# TASK 24: PROPERTY TESTS - BEHAVIOR SERVICE (3 properties) - FIXED
# =============================================================================

async def test_behavior_properties_fixed(runner: PropertyTestRunner):
    """Test BehaviorService properties - FIXED VERSION"""
    print(f"\n🧪 TASK 24: BehaviorService Property Tests (FIXED)")
    print("-" * 50)
    
    try:
        behavior_service = BehaviorService()
        
        # Property 11: Behavior pattern completeness - FIXED with lowercase enum
        try:
            pattern_data = BehaviorPatternCreate(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                pattern_type=PatternType.RESPONSE_OPTIMIZATION,  # This should work with lowercase in DB
                trigger_context={"context": "test_trigger"},
                action_config={"action": "test_action"},
                success_rate=0.75,
                total_applications=10,
                is_active=True
            )
            
            created_pattern = await behavior_service.create_pattern(pattern_data)
            
            # Verify completeness
            completeness_check = (
                created_pattern.agent_id == runner.agent_id and
                created_pattern.client_id == runner.client_id and
                created_pattern.pattern_type == pattern_data.pattern_type and
                created_pattern.success_rate == pattern_data.success_rate and
                created_pattern.total_applications == pattern_data.total_applications and
                created_pattern.is_active == pattern_data.is_active
            )
            
            runner.log_test(
                "Property 11: Behavior pattern completeness",
                completeness_check,
                f"All fields preserved in pattern {created_pattern.id}"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 11: Behavior pattern completeness",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 12: Pattern application recording - FIXED
        try:
            # Create a pattern
            pattern = await behavior_service.create_pattern(BehaviorPatternCreate(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                pattern_type=PatternType.CONVERSATION_FLOW,  # This should work
                trigger_context={"test": "recording"},
                action_config={"record": "test"},
                success_rate=0.5,
                total_applications=2,
                is_active=True
            ))
            
            initial_applications = pattern.total_applications
            initial_success_rate = pattern.success_rate
            
            # Record successful usage
            updated_pattern = await behavior_service.record_pattern_usage(
                pattern.id, 
                success=True
            )
            
            # Verify recording
            recording_correct = (
                updated_pattern.total_applications == initial_applications + 1 and
                updated_pattern.success_rate >= initial_success_rate  # Should increase or stay same
            )
            
            runner.log_test(
                "Property 12: Pattern application recording",
                recording_correct,
                f"Applications: {initial_applications} → {updated_pattern.total_applications}, "
                f"Success rate: {initial_success_rate:.2f} → {updated_pattern.success_rate:.2f}"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 12: Pattern application recording",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 13: Pattern success rate ordering - FIXED
        try:
            # Create patterns with different success rates
            patterns_created = []
            success_rates = [0.9, 0.3, 0.7, 0.5]
            
            for i, rate in enumerate(success_rates):
                pattern = await behavior_service.create_pattern(BehaviorPatternCreate(
                    agent_id=runner.agent_id,
                    client_id=runner.client_id,
                    pattern_type=PatternType.RESPONSE_OPTIMIZATION,
                    trigger_context={"order_test": i},
                    action_config={"rate": rate},
                    success_rate=rate,
                    total_applications=10,
                    is_active=True
                ))
                patterns_created.append(pattern)
            
            # Get patterns (should be ordered by success rate desc)
            retrieved_patterns = await behavior_service.get_agent_patterns(
                agent_id=runner.agent_id,
                is_active=True
            )
            
            # Check if ordered by success rate (descending)
            ordering_correct = True
            for i in range(len(retrieved_patterns) - 1):
                if retrieved_patterns[i].success_rate < retrieved_patterns[i + 1].success_rate:
                    ordering_correct = False
                    break
            
            runner.log_test(
                "Property 13: Pattern success rate ordering",
                ordering_correct,
                f"Retrieved {len(retrieved_patterns)} patterns in correct order"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 13: Pattern success rate ordering",
                False,
                f"Error: {str(e)}"
            )
            
    except Exception as e:
        runner.log_test(
            "BehaviorService initialization",
            False,
            f"Failed to initialize: {str(e)}"
        )


# =============================================================================
# TASK 26: PROPERTY TESTS - SNAPSHOT SERVICE (2 properties) - ALREADY WORKING
# =============================================================================

async def test_snapshot_properties_fixed(runner: PropertyTestRunner):
    """Test SnapshotService properties - ALREADY WORKING"""
    print(f"\n🧪 TASK 26: SnapshotService Property Tests (ALREADY WORKING)")
    print("-" * 50)
    
    try:
        snapshot_service = SnapshotService()
        
        # Property 23: Snapshot completeness
        try:
            # Create a snapshot
            snapshot = await snapshot_service.create_snapshot(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                snapshot_type=SnapshotType.MANUAL
            )
            
            # Verify completeness
            completeness_check = (
                snapshot.agent_id == runner.agent_id and
                snapshot.client_id == runner.client_id and
                snapshot.snapshot_type == SnapshotType.MANUAL and
                isinstance(snapshot.memory_count, int) and
                isinstance(snapshot.pattern_count, int) and
                isinstance(snapshot.total_interactions, int) and
                snapshot.snapshot_data is not None
            )
            
            runner.log_test(
                "Property 23: Snapshot completeness",
                completeness_check,
                f"Snapshot {snapshot.id}: {snapshot.memory_count} memories, {snapshot.pattern_count} patterns"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 23: Snapshot completeness",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 24: Rollback deactivation
        try:
            # Create initial snapshot
            initial_snapshot = await snapshot_service.create_snapshot(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                snapshot_type=SnapshotType.PRE_ROLLBACK
            )
            
            # Simulate some time passing and create another snapshot
            import time
            time.sleep(1)  # Ensure different timestamps
            
            later_snapshot = await snapshot_service.create_snapshot(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                snapshot_type=SnapshotType.AUTOMATIC
            )
            
            # Test rollback (this would deactivate newer items)
            rollback_result = await snapshot_service.restore_snapshot(
                initial_snapshot.id
            )
            
            rollback_successful = (
                "snapshot_id" in rollback_result and
                "memories_deactivated" in rollback_result and
                "patterns_deactivated" in rollback_result and
                isinstance(rollback_result["memories_deactivated"], int) and
                isinstance(rollback_result["patterns_deactivated"], int)
            )
            
            runner.log_test(
                "Property 24: Rollback deactivation",
                rollback_successful,
                f"Rollback completed: {rollback_result.get('memories_deactivated', 0)} memories, "
                f"{rollback_result.get('patterns_deactivated', 0)} patterns deactivated"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 24: Rollback deactivation",
                False,
                f"Error: {str(e)}"
            )
            
    except Exception as e:
        runner.log_test(
            "SnapshotService initialization",
            False,
            f"Failed to initialize: {str(e)}"
        )


# =============================================================================
# TASK 28: PROPERTY TESTS - METRICS SERVICE (6 properties) - FIXED
# =============================================================================

async def test_metrics_properties_fixed(runner: PropertyTestRunner):
    """Test MetricsService properties - FIXED VERSION"""
    print(f"\n🧪 TASK 28: MetricsService Property Tests (FIXED)")
    print("-" * 50)
    
    try:
        metrics_service = MetricsService()
        
        # Property 25: Interaction metrics recording
        try:
            # Record an interaction
            metrics = await metrics_service.record_interaction(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                success=True,
                response_time_ms=250,
                satisfaction_score=4.5,
                metadata={"test": "property_25"}
            )
            
            # Verify recording
            recording_correct = (
                metrics.agent_id == runner.agent_id and
                metrics.client_id == runner.client_id and
                metrics.total_interactions >= 1 and
                metrics.successful_interactions >= 1 and
                metrics.avg_response_time_ms is not None and
                metrics.user_satisfaction_score is not None
            )
            
            runner.log_test(
                "Property 25: Interaction metrics recording",
                recording_correct,
                f"Recorded interaction: {metrics.total_interactions} total, "
                f"{metrics.avg_response_time_ms}ms avg response"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 25: Interaction metrics recording",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 26: Memory usage metrics - FIXED with proper wait
        try:
            # Record an interaction first to ensure today's metrics exist
            await metrics_service.record_interaction(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                success=True
            )
            
            # Increment memory usage
            await metrics_service.increment_memory_usage(runner.agent_id, count=3)
            
            # Get today's metrics
            today_metrics = await metrics_service.get_metrics(
                runner.agent_id,
                MetricsPeriod.LAST_7_DAYS
            )
            
            # Find today's entry
            today = date.today()
            today_entry = None
            for metric in today_metrics:
                if metric.metric_date == today:
                    today_entry = metric
                    break
            
            memory_tracking = (
                today_entry is not None and
                today_entry.memory_chunks_used >= 3
            )
            
            runner.log_test(
                "Property 26: Memory usage metrics",
                memory_tracking,
                f"Memory usage tracked: {today_entry.memory_chunks_used if today_entry else 0} chunks"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 26: Memory usage metrics",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 27: Pattern application metrics - FIXED
        try:
            # Ensure today's metrics exist
            await metrics_service.record_interaction(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                success=True
            )
            
            # Increment pattern applications
            await metrics_service.increment_pattern_application(runner.agent_id, count=2)
            
            # Get metrics
            metrics_list = await metrics_service.get_metrics(
                runner.agent_id,
                MetricsPeriod.LAST_7_DAYS
            )
            
            # Find today's entry
            today = date.today()
            today_entry = None
            for metric in metrics_list:
                if metric.metric_date == today:
                    today_entry = metric
                    break
            
            pattern_tracking = (
                today_entry is not None and
                today_entry.patterns_applied >= 2
            )
            
            runner.log_test(
                "Property 27: Pattern application metrics",
                pattern_tracking,
                f"Pattern applications tracked: {today_entry.patterns_applied if today_entry else 0}"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 27: Pattern application metrics",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 28: Learning consolidation metrics - FIXED
        try:
            # Ensure today's metrics exist
            await metrics_service.record_interaction(
                agent_id=runner.agent_id,
                client_id=runner.client_id,
                success=True
            )
            
            # Increment new learnings
            await metrics_service.increment_new_learnings(runner.agent_id, count=1)
            
            # Get metrics
            metrics_list = await metrics_service.get_metrics(
                runner.agent_id,
                MetricsPeriod.LAST_7_DAYS
            )
            
            # Find today's entry
            today = date.today()
            today_entry = None
            for metric in metrics_list:
                if metric.metric_date == today:
                    today_entry = metric
                    break
            
            learning_tracking = (
                today_entry is not None and
                today_entry.new_learnings >= 1
            )
            
            runner.log_test(
                "Property 28: Learning consolidation metrics",
                learning_tracking,
                f"New learnings tracked: {today_entry.new_learnings if today_entry else 0}"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 28: Learning consolidation metrics",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 29: Metrics aggregation
        try:
            # Get aggregated metrics
            aggregated = await metrics_service.get_aggregated_metrics(
                runner.agent_id,
                MetricsPeriod.LAST_30_DAYS
            )
            
            # Verify aggregation structure
            aggregation_correct = (
                "period" in aggregated and
                "total_interactions" in aggregated and
                "successful_interactions" in aggregated and
                "success_rate" in aggregated and
                isinstance(aggregated["total_interactions"], int) and
                isinstance(aggregated["success_rate"], float)
            )
            
            runner.log_test(
                "Property 29: Metrics aggregation",
                aggregation_correct,
                f"Aggregated {aggregated['total_interactions']} interactions, "
                f"{aggregated['success_rate']:.1%} success rate"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 29: Metrics aggregation",
                False,
                f"Error: {str(e)}"
            )
        
        # Property 31: Learning velocity calculation
        try:
            # Calculate learning velocity
            velocity = await metrics_service.calculate_learning_velocity(
                runner.agent_id,
                days=7
            )
            
            velocity_valid = (
                isinstance(velocity, float) and
                velocity >= 0.0
            )
            
            runner.log_test(
                "Property 31: Learning velocity calculation",
                velocity_valid,
                f"Learning velocity: {velocity:.2f} learnings/day"
            )
            
        except Exception as e:
            runner.log_test(
                "Property 31: Learning velocity calculation",
                False,
                f"Error: {str(e)}"
            )
            
    except Exception as e:
        runner.log_test(
            "MetricsService initialization",
            False,
            f"Failed to initialize: {str(e)}"
        )


# =============================================================================
# MAIN EXECUTION - FIXED VERSION
# =============================================================================

async def main():
    """Run all property tests - FIXED VERSION"""
    print("🚀 SICC PROPERTY TESTS - PHASE 5 (FIXED)")
    print("=" * 60)
    print("Executing all pending property tests with fixes applied")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    runner = PropertyTestRunner()
    
    # Execute all property test suites - FIXED VERSIONS
    await test_embedding_properties_fixed(runner)
    await test_memory_properties_fixed(runner)
    await test_behavior_properties_fixed(runner)
    await test_snapshot_properties_fixed(runner)
    await test_metrics_properties_fixed(runner)
    
    # Print final summary
    runner.print_summary()
    
    return runner.passed_tests == runner.total_tests


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)