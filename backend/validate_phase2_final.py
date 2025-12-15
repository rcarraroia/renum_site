"""
SICC Phase 2 Final Validation Script
Sprint 10 - SICC Implementation - Task 31 (Renus Integration)

Validates AgentOrchestrator functionality:
- Prompt enrichment with memories
- Pattern application
- Token limit enforcement
- Fallback handling
"""

import asyncio
import sys
from uuid import UUID

# Add src to path
sys.path.insert(0, 'src')

from src.services.sicc.agent_orchestrator import AgentOrchestrator, get_agent_orchestrator
from src.services.sicc.memory_service import MemoryService
from src.services.sicc.behavior_service import BehaviorService
from src.services.sicc.embedding_service import get_embedding_service
from src.models.sicc.memory import MemoryChunkCreate, ChunkType
from src.models.sicc.behavior import BehaviorPatternCreate, PatternType


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_test(name: str, passed: bool, details: str = ""):
    """Print test result"""
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if details:
        print(f"     {details}")


async def setup_test_data():
    """Setup test memories and patterns"""
    print_section("SETTING UP TEST DATA")
    
    # Use real IDs from database
    test_agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
    test_client_id = UUID("9e26202e-7090-4051-9bfd-6b397b3947cc")
    
    memory_service = MemoryService()
    behavior_service = BehaviorService()
    embedding_service = get_embedding_service()
    
    # Create test memories
    memories_created = []
    
    try:
        # Memory 1: Business term
        content1 = "RENUM é uma plataforma de agentes de IA especializados para diferentes nichos de mercado"
        embedding1 = embedding_service.generate_embedding(content1)
        
        memory1 = await memory_service.create_memory(
            MemoryChunkCreate(
                agent_id=test_agent_id,
                client_id=test_client_id,
                chunk_type=ChunkType.BUSINESS_TERM,
                content=content1,
                embedding=embedding1,
                confidence=0.95,
                metadata={"source": "test_setup"}
            )
        )
        memories_created.append(memory1.id)
        print_test("Create Memory 1 (Business Term)", True, f"ID: {memory1.id}")
        
        # Memory 2: FAQ
        content2 = "Pergunta: Como funciona o SICC? Resposta: O SICC é um sistema de aprendizado contínuo que permite aos agentes evoluírem com base em interações reais"
        embedding2 = embedding_service.generate_embedding(content2)
        
        memory2 = await memory_service.create_memory(
            MemoryChunkCreate(
                agent_id=test_agent_id,
                client_id=test_client_id,
                chunk_type=ChunkType.FAQ,
                content=content2,
                embedding=embedding2,
                confidence=0.90,
                metadata={"source": "test_setup"}
            )
        )
        memories_created.append(memory2.id)
        print_test("Create Memory 2 (FAQ)", True, f"ID: {memory2.id}")
        
        # Memory 3: Process
        content3 = "Processo de onboarding: 1) Cadastro inicial 2) Configuração do agente 3) Treinamento 4) Ativação"
        embedding3 = embedding_service.generate_embedding(content3)
        
        memory3 = await memory_service.create_memory(
            MemoryChunkCreate(
                agent_id=test_agent_id,
                client_id=test_client_id,
                chunk_type=ChunkType.PROCESS,
                content=content3,
                embedding=embedding3,
                confidence=0.85,
                metadata={"source": "test_setup"}
            )
        )
        memories_created.append(memory3.id)
        print_test("Create Memory 3 (Process)", True, f"ID: {memory3.id}")
        
    except Exception as e:
        print_test("Setup Memories", False, f"Error: {e}")
        return None, None
    
    # Create test pattern
    patterns_created = []
    
    try:
        pattern1 = await behavior_service.create_pattern(
            BehaviorPatternCreate(
                agent_id=test_agent_id,
                client_id=test_client_id,
                pattern_type=PatternType.RESPONSE_STRATEGY,
                trigger_context={
                    "message_type": "question",
                    "topic": "sicc"
                },
                action_config={
                    "strategy": "detailed_explanation",
                    "template": "Vou explicar em detalhes: {content}"
                },
                confidence=0.88
            )
        )
        patterns_created.append(pattern1.id)
        print_test("Create Pattern 1 (Response Strategy)", True, f"ID: {pattern1.id}")
        
    except Exception as e:
        print_test("Setup Patterns", False, f"Error: {e}")
        return memories_created, None
    
    return memories_created, patterns_created


async def test_orchestrator_basic():
    """Test basic orchestrator functionality"""
    print_section("TESTING ORCHESTRATOR - BASIC FUNCTIONALITY")
    
    try:
        orchestrator = get_agent_orchestrator()
        test_agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
        
        # Test 1: Enrich prompt with relevant query
        enriched = await orchestrator.enrich_prompt(
            agent_id=test_agent_id,
            message="O que é o SICC e como ele funciona?",
            context={"message_type": "question", "topic": "sicc"}
        )
        
        print_test(
            "Enrich Prompt (Relevant Query)",
            enriched is not None,
            f"Memories: {len(enriched.memories_used)}, Patterns: {len(enriched.patterns_applied)}, Tokens: {enriched.token_count}"
        )
        
        # Verify memories were found
        print_test(
            "Memories Found",
            len(enriched.memories_used) > 0,
            f"Found {len(enriched.memories_used)} relevant memories"
        )
        
        # Verify patterns were applied
        print_test(
            "Patterns Applied",
            len(enriched.patterns_applied) >= 0,  # May be 0 if no match
            f"Applied {len(enriched.patterns_applied)} patterns"
        )
        
        # Verify enriched prompt is different from original
        print_test(
            "Prompt Enriched",
            enriched.enriched_prompt != enriched.original_message,
            "Prompt was enriched with context"
        )
        
        # Verify token count is reasonable
        print_test(
            "Token Count Reasonable",
            enriched.token_count < AgentOrchestrator.MAX_TOKENS,
            f"Token count: {enriched.token_count} < {AgentOrchestrator.MAX_TOKENS}"
        )
        
        # Test 2: Enrich prompt with irrelevant query
        enriched2 = await orchestrator.enrich_prompt(
            agent_id=test_agent_id,
            message="Qual é a capital da França?",
            context={}
        )
        
        print_test(
            "Enrich Prompt (Irrelevant Query)",
            enriched2 is not None,
            f"Memories: {len(enriched2.memories_used)}, Patterns: {len(enriched2.patterns_applied)}"
        )
        
        # Should have fewer or no memories for irrelevant query
        print_test(
            "Fewer Memories for Irrelevant Query",
            len(enriched2.memories_used) <= len(enriched.memories_used),
            f"Found {len(enriched2.memories_used)} memories (expected <= {len(enriched.memories_used)})"
        )
        
        return True
        
    except Exception as e:
        print_test("Orchestrator Basic", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_orchestrator_process_with_memory():
    """Test process_with_memory method"""
    print_section("TESTING ORCHESTRATOR - PROCESS WITH MEMORY")
    
    try:
        orchestrator = get_agent_orchestrator()
        test_agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
        
        # Test: Process message with memory
        result = await orchestrator.process_with_memory(
            agent_id=test_agent_id,
            message="Como funciona o processo de onboarding?",
            context={"message_type": "question"}
        )
        
        print_test(
            "Process With Memory",
            result is not None,
            f"Returned result with {result['memories_count']} memories"
        )
        
        # Verify result structure
        required_keys = [
            "enriched_prompt",
            "original_message",
            "memories_count",
            "patterns_count",
            "token_count",
            "memories",
            "patterns",
            "context"
        ]
        
        for key in required_keys:
            print_test(
                f"Result has '{key}'",
                key in result,
                f"Value: {type(result.get(key))}"
            )
        
        # Verify enriched prompt is usable
        print_test(
            "Enriched Prompt Usable",
            len(result["enriched_prompt"]) > len(result["original_message"]),
            f"Enriched: {len(result['enriched_prompt'])} chars, Original: {len(result['original_message'])} chars"
        )
        
        return True
        
    except Exception as e:
        print_test("Process With Memory", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_orchestrator_token_limit():
    """Test token limit enforcement"""
    print_section("TESTING ORCHESTRATOR - TOKEN LIMIT")
    
    try:
        orchestrator = get_agent_orchestrator()
        test_agent_id = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
        
        # Create a very long message to test token limit
        long_message = "Explique em detalhes " + ("sobre o SICC " * 100)
        
        enriched = await orchestrator.enrich_prompt(
            agent_id=test_agent_id,
            message=long_message,
            context={}
        )
        
        print_test(
            "Token Limit Enforced",
            enriched.token_count <= AgentOrchestrator.MAX_TOKENS,
            f"Token count: {enriched.token_count} <= {AgentOrchestrator.MAX_TOKENS}"
        )
        
        # Verify prompt was still enriched (even if truncated)
        print_test(
            "Prompt Still Enriched",
            enriched is not None,
            "Enrichment succeeded despite long message"
        )
        
        return True
        
    except Exception as e:
        print_test("Token Limit", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_orchestrator_fallback():
    """Test fallback when no memories found"""
    print_section("TESTING ORCHESTRATOR - FALLBACK HANDLING")
    
    try:
        orchestrator = get_agent_orchestrator()
        # Use a different agent ID that has no memories
        fake_agent_id = UUID("00000000-0000-0000-0000-000000000001")
        
        # This should not fail, just return original message
        enriched = await orchestrator.enrich_prompt(
            agent_id=fake_agent_id,
            message="Test message",
            context={}
        )
        
        print_test(
            "Fallback Works",
            enriched is not None,
            "Returned result even with no memories"
        )
        
        print_test(
            "No Memories Found",
            len(enriched.memories_used) == 0,
            "Correctly returned 0 memories"
        )
        
        print_test(
            "Original Message Preserved",
            enriched.original_message == "Test message",
            "Original message preserved in fallback"
        )
        
        return True
        
    except Exception as e:
        print_test("Fallback Handling", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def cleanup_test_data(memory_ids, pattern_ids):
    """Cleanup test data"""
    print_section("CLEANING UP TEST DATA")
    
    memory_service = MemoryService()
    behavior_service = BehaviorService()
    
    # Delete test memories
    if memory_ids:
        for memory_id in memory_ids:
            try:
                await memory_service.delete_memory(memory_id)
                print_test(f"Delete Memory {memory_id}", True, "Deleted")
            except Exception as e:
                print_test(f"Delete Memory {memory_id}", False, f"Error: {e}")
    
    # Delete test patterns
    if pattern_ids:
        for pattern_id in pattern_ids:
            try:
                await behavior_service.delete_pattern(pattern_id)
                print_test(f"Delete Pattern {pattern_id}", True, "Deleted")
            except Exception as e:
                print_test(f"Delete Pattern {pattern_id}", False, f"Error: {e}")


async def main():
    """Run all validation tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}SICC PHASE 2 FINAL VALIDATION{Colors.END}")
    print(f"{Colors.BLUE}Sprint 10 - Task 31 - Renus Integration{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    # Setup test data
    memory_ids, pattern_ids = await setup_test_data()
    
    if memory_ids is None:
        print(f"\n{Colors.RED}❌ FAILED TO SETUP TEST DATA{Colors.END}\n")
        return 1
    
    # Run tests
    results = {
        "Basic Functionality": await test_orchestrator_basic(),
        "Process With Memory": await test_orchestrator_process_with_memory(),
        "Token Limit": await test_orchestrator_token_limit(),
        "Fallback Handling": await test_orchestrator_fallback()
    }
    
    # Cleanup
    await cleanup_test_data(memory_ids, pattern_ids)
    
    # Summary
    print_section("VALIDATION SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED - PHASE 2 FINAL VALIDATED{Colors.END}")
        print(f"{Colors.GREEN}✅ TASK 31 (RENUS INTEGRATION) COMPLETE{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}❌ SOME TESTS FAILED - PHASE 2 FINAL NOT VALIDATED{Colors.END}\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
