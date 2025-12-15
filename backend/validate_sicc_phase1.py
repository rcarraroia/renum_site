"""
SICC Phase 1 Validation Script
Sprint 10 - SICC Implementation

Validates EmbeddingService, MemoryService, and BehaviorService functionality.
"""

import asyncio
import sys
from uuid import uuid4, UUID
from datetime import datetime

# Add src to path
sys.path.insert(0, 'src')

from src.services.sicc.embedding_service import get_embedding_service
from src.services.sicc.memory_service import MemoryService
from src.services.sicc.behavior_service import BehaviorService
from src.models.sicc.memory import ChunkType, MemorySearchQuery
from src.models.sicc.behavior import PatternType, BehaviorPatternCreate


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_test(name: str, passed: bool, details: str = ""):
    """Print test result"""
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if details:
        print(f"     {details}")


def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


async def test_embedding_service():
    """Test EmbeddingService functionality"""
    print_section("TESTING EMBEDDING SERVICE")
    
    try:
        service = get_embedding_service()
        
        # Test 1: Model loaded
        model_info = service.get_model_info()
        print_test(
            "Model Loading",
            model_info["model_loaded"],
            f"Model: {model_info['model_name']}, Dim: {model_info['embedding_dimension']}"
        )
        
        # Test 2: Generate single embedding
        text = "This is a test sentence for embedding generation."
        embedding = service.generate_embedding(text)
        print_test(
            "Single Embedding Generation",
            len(embedding) == 384,
            f"Generated {len(embedding)} dimensions"
        )
        
        # Test 3: Generate batch embeddings
        texts = [
            "First test sentence",
            "Second test sentence",
            "Third test sentence"
        ]
        embeddings = service.generate_embeddings_batch(texts)
        print_test(
            "Batch Embedding Generation",
            len(embeddings) == 3 and all(len(e) == 384 for e in embeddings),
            f"Generated {len(embeddings)} embeddings"
        )
        
        # Test 4: Cosine similarity
        similarity = service.cosine_similarity(embeddings[0], embeddings[1])
        print_test(
            "Cosine Similarity",
            0.0 <= similarity <= 1.0,
            f"Similarity: {similarity:.4f}"
        )
        
        # Test 5: Token counting
        token_count = service.count_tokens(text)
        print_test(
            "Token Counting",
            token_count > 0,
            f"Tokens: {token_count}"
        )
        
        # Test 6: Text truncation
        long_text = "word " * 1000
        truncated = service.truncate_text(long_text, max_tokens=100)
        truncated_tokens = service.count_tokens(truncated)
        print_test(
            "Text Truncation",
            truncated_tokens <= 100,
            f"Truncated to {truncated_tokens} tokens"
        )
        
        return True
        
    except Exception as e:
        print_test("EmbeddingService", False, f"Error: {e}")
        return False


async def test_memory_service():
    """Test MemoryService functionality"""
    print_section("TESTING MEMORY SERVICE")
    
    try:
        service = MemoryService()
        # Use real IDs from database
        test_agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
        test_client_id = UUID("9e26202e-7090-4051-9bfd-6b397b3947cc")
        
        # Test 1: Create memory from text
        memory = await service.create_memory_from_text(
            agent_id=test_agent_id,
            client_id=test_client_id,
            content="Test memory content about product features",
            chunk_type=ChunkType.PRODUCT,
            metadata={"test": True},
            source="manual",
            confidence=0.9
        )
        print_test(
            "Create Memory from Text",
            memory.id is not None,
            f"Created memory {memory.id}"
        )
        
        memory_id = memory.id
        
        # Test 2: Get memory
        retrieved = await service.get_memory(memory_id)
        print_test(
            "Get Memory",
            retrieved is not None and retrieved.id == memory_id,
            f"Retrieved memory {retrieved.id if retrieved else 'None'}"
        )
        
        # Test 3: Search memories
        search_query = MemorySearchQuery(
            query_text="product features",
            agent_id=test_agent_id,
            limit=5,
            similarity_threshold=0.5
        )
        results = await service.search_memories(search_query)
        print_test(
            "Search Memories",
            len(results) > 0,
            f"Found {len(results)} results"
        )
        
        if results:
            print_test(
                "Search Result Similarity",
                results[0].similarity_score >= 0.5,
                f"Top result similarity: {results[0].similarity_score:.4f}"
            )
        
        # Test 4: Increment usage count
        await service.increment_usage_count(memory_id)
        updated = await service.get_memory(memory_id)
        print_test(
            "Increment Usage Count",
            updated.usage_count == 1,
            f"Usage count: {updated.usage_count}"
        )
        
        # Test 5: Get agent memories
        memories = await service.get_agent_memories(test_agent_id, limit=10)
        print_test(
            "Get Agent Memories",
            len(memories) > 0,
            f"Found {len(memories)} memories"
        )
        
        # Test 6: Get memory stats
        stats = await service.get_memory_stats(test_agent_id)
        print_test(
            "Get Memory Stats",
            stats["total_memories"] > 0,
            f"Total: {stats['total_memories']}, Avg confidence: {stats['avg_confidence']:.2f}"
        )
        
        # Test 7: Delete memory
        deleted = await service.delete_memory(memory_id)
        print_test(
            "Delete Memory",
            deleted,
            f"Deleted memory {memory_id}"
        )
        
        return True
        
    except Exception as e:
        print_test("MemoryService", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_behavior_service():
    """Test BehaviorService functionality"""
    print_section("TESTING BEHAVIOR SERVICE")
    
    try:
        service = BehaviorService()
        # Use real IDs from database
        test_agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
        test_client_id = UUID("9e26202e-7090-4051-9bfd-6b397b3947cc")
        
        # Test 1: Create pattern
        pattern_data = BehaviorPatternCreate(
            agent_id=test_agent_id,
            client_id=test_client_id,
            pattern_type=PatternType.RESPONSE_STRATEGY,
            trigger_context={"user_sentiment": "positive"},
            action_config={"response_style": "enthusiastic"}
        )
        pattern = await service.create_pattern(pattern_data)
        print_test(
            "Create Pattern",
            pattern.id is not None,
            f"Created pattern {pattern.id}"
        )
        
        pattern_id = pattern.id
        
        # Test 2: Get pattern
        retrieved = await service.get_pattern(pattern_id)
        print_test(
            "Get Pattern",
            retrieved is not None and retrieved.id == pattern_id,
            f"Retrieved pattern {retrieved.id if retrieved else 'None'}"
        )
        
        # Test 3: Record pattern usage (success)
        updated = await service.record_pattern_usage(pattern_id, success=True)
        print_test(
            "Record Pattern Usage (Success)",
            updated.total_applications == 1 and updated.success_rate == 1.0,
            f"Uses: {updated.total_applications}, Success rate: {updated.success_rate:.2f}"
        )
        
        # Test 4: Record pattern usage (failure)
        updated = await service.record_pattern_usage(pattern_id, success=False)
        print_test(
            "Record Pattern Usage (Failure)",
            updated.total_applications == 2 and updated.success_rate == 0.5,
            f"Uses: {updated.total_applications}, Success rate: {updated.success_rate:.2f}"
        )
        
        # Test 5: Get agent patterns
        patterns = await service.get_agent_patterns(test_agent_id)
        print_test(
            "Get Agent Patterns",
            len(patterns) > 0,
            f"Found {len(patterns)} patterns"
        )
        
        # Test 6: Get pattern stats
        stats = await service.get_pattern_stats(pattern_id)
        print_test(
            "Get Pattern Stats",
            stats.total_uses == 2,
            f"Total: {stats.total_uses}, Success: {stats.successful_applications}, Failed: {stats.failed_uses}"
        )
        
        # Test 7: Find matching patterns
        context = {"user_sentiment": "positive"}
        matching = await service.find_matching_patterns(test_agent_id, context)
        print_test(
            "Find Matching Patterns",
            len(matching) > 0,
            f"Found {len(matching)} matching patterns"
        )
        
        # Test 8: Delete pattern
        deleted = await service.delete_pattern(pattern_id)
        print_test(
            "Delete Pattern",
            deleted,
            f"Deleted pattern {pattern_id}"
        )
        
        return True
        
    except Exception as e:
        print_test("BehaviorService", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all validation tests"""
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}SICC PHASE 1 VALIDATION{Colors.END}")
    print(f"{Colors.YELLOW}Sprint 10 - Sistema de Inteligência Corporativa Contínua{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")
    
    results = []
    
    # Test EmbeddingService
    results.append(await test_embedding_service())
    
    # Test MemoryService
    results.append(await test_memory_service())
    
    # Test BehaviorService
    results.append(await test_behavior_service())
    
    # Summary
    print_section("VALIDATION SUMMARY")
    
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"Total Services: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    if failed > 0:
        print(f"{Colors.RED}Failed: {failed}{Colors.END}")
    
    if all(results):
        print(f"\n{Colors.GREEN}✅ ALL TESTS PASSED - PHASE 1 VALIDATED{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}❌ SOME TESTS FAILED - PHASE 1 NOT VALIDATED{Colors.END}\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
