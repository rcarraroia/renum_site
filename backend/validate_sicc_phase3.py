"""
Validation Script - SICC Phase 3 (Learning Service)
Sprint 10 - SICC Implementation

Validates LearningService implementation with ISA analysis and approval workflow.
"""

import asyncio
import sys
from uuid import UUID
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, "src")

from src.services.sicc.learning_service import LearningService
from src.services.sicc.memory_service import MemoryService
from src.services.sicc.behavior_service import BehaviorService
from src.config.supabase import supabase_admin
from src.utils.logger import logger


# Test IDs (real from database)
TEST_AGENT_ID = UUID("37ae9902-24bf-42b1-9d01-88c201ee0a6c")
TEST_CLIENT_ID = UUID("9e26202e-7090-4051-9bfd-6b397b3947cc")
TEST_PROFILE_ID = UUID("876be331-9553-4e9a-9f29-63cfa711e056")  # Valid profile for reviewed_by


class Phase3Validator:
    """Validator for Phase 3 - Learning Service"""
    
    def __init__(self):
        self.learning_service = LearningService()
        self.memory_service = MemoryService()
        self.behavior_service = BehaviorService()
        self.supabase = supabase_admin
        self.tests_passed = 0
        self.tests_failed = 0
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if message:
            print(f"    {message}")
        
        if passed:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
    
    async def setup_test_data(self):
        """Setup test data"""
        print("\n📋 Setting up test data...")
        
        try:
            # Clean up any existing test data
            self.supabase.table("agent_learning_logs").delete().eq(
                "agent_id", str(TEST_AGENT_ID)
            ).execute()
            
            print("   ✅ Test environment ready")
            
        except Exception as e:
            print(f"   ⚠️  Setup warning: {e}")
    
    async def cleanup_test_data(self):
        """Clean up test data"""
        print("\n🧹 Cleaning up test data...")
        
        try:
            # Delete learning logs
            self.supabase.table("agent_learning_logs").delete().eq(
                "agent_id", str(TEST_AGENT_ID)
            ).execute()
            
            # Delete test memories created during tests
            self.supabase.table("agent_memory_chunks").delete().eq(
                "agent_id", str(TEST_AGENT_ID)
            ).eq("source", "isa_analysis").execute()
            
            # Delete test patterns
            self.supabase.table("agent_behavior_patterns").delete().eq(
                "agent_id", str(TEST_AGENT_ID)
            ).execute()
            
            print("   ✅ Test data cleaned up")
            
        except Exception as e:
            print(f"   ⚠️  Cleanup warning: {e}")
    
    async def test_1_analyze_conversations(self):
        """Test 1: Analyze conversations and extract learnings"""
        print("\n🧪 Test 1: Analyze conversations")
        
        try:
            result = await self.learning_service.analyze_conversations(
                agent_id=TEST_AGENT_ID,
                time_window_hours=24,
                min_messages=3
            )
            
            # Verify result structure
            assert "conversations_analyzed" in result
            assert "learnings_detected" in result
            assert "high_confidence" in result
            assert "medium_confidence" in result
            assert "low_confidence" in result
            
            # Result should be valid (may be 0 if no conversations)
            assert result["conversations_analyzed"] >= 0
            assert result["learnings_detected"] >= 0
            
            self.log_test(
                "Analyze conversations",
                True,
                f"Analyzed {result['conversations_analyzed']} conversations, "
                f"detected {result['learnings_detected']} learnings"
            )
            
            return result
            
        except Exception as e:
            self.log_test("Analyze conversations", False, str(e))
            raise
    
    async def test_2_create_learning_log(self):
        """Test 2: Create learning log manually"""
        print("\n🧪 Test 2: Create learning log")
        
        try:
            learning = await self.learning_service.create_learning_log(
                agent_id=TEST_AGENT_ID,
                learning_type="memory_added",
                source_data={
                    "content": "Termo: produto premium\nContexto: Conversas sobre produto premium",
                    "chunk_type": "business_term",
                    "metadata": {
                        "term": "produto premium",
                        "frequency": 3
                    }
                },
                analysis={
                    "detected_pattern": "frequent_term",
                    "recommendation": "Add to vocabulary"
                },
                confidence=0.85
            )
            
            # Verify learning log
            assert learning.id is not None
            assert learning.agent_id == TEST_AGENT_ID
            assert learning.learning_type == "memory_added"
            assert learning.confidence == 0.85
            assert learning.status == "pending"
            
            self.log_test(
                "Create learning log",
                True,
                f"Created learning log {learning.id}"
            )
            
            return learning
            
        except Exception as e:
            self.log_test("Create learning log", False, str(e))
            raise
    
    async def test_3_auto_approve_high_confidence(self, learning):
        """Test 3: Auto-approve high confidence learning"""
        print("\n🧪 Test 3: Auto-approve high confidence")
        
        try:
            # Approve learning
            approved = await self.learning_service.approve_learning(
                learning_id=learning.id,
                approved_by=TEST_PROFILE_ID,  # Use profile_id, not agent_id
                auto_approved=True
            )
            
            # Verify approval
            assert approved.status == "approved"
            assert approved.reviewed_by == TEST_PROFILE_ID
            assert approved.reviewed_at is not None
            
            # Wait a bit for consolidation
            await asyncio.sleep(1)
            
            # Verify memory was created
            memories = await self.memory_service.get_agent_memories(
                agent_id=TEST_AGENT_ID,
                limit=10
            )
            
            # Should have at least one memory
            assert len(memories) > 0
            
            self.log_test(
                "Auto-approve high confidence",
                True,
                f"Approved and consolidated into {len(memories)} memories"
            )
            
        except Exception as e:
            self.log_test("Auto-approve high confidence", False, str(e))
            raise
    
    async def test_4_reject_low_confidence(self):
        """Test 4: Reject low confidence learning"""
        print("\n🧪 Test 4: Reject low confidence")
        
        try:
            # Create low confidence learning
            learning = await self.learning_service.create_learning_log(
                agent_id=TEST_AGENT_ID,
                learning_type="memory_added",
                source_data={
                    "content": "Termo: test_low",
                    "chunk_type": "business_term",
                    "metadata": {"term": "test_low", "frequency": 1}
                },
                analysis={"detected_pattern": "rare_term"},
                confidence=0.3
            )
            
            # Reject learning
            rejected = await self.learning_service.reject_learning(
                learning_id=learning.id,
                rejected_by=TEST_PROFILE_ID,
                reason="Confidence below threshold"
            )
            
            # Verify rejection
            assert rejected.status == "rejected"
            assert rejected.reviewed_by == TEST_PROFILE_ID
            
            self.log_test(
                "Reject low confidence",
                True,
                f"Rejected learning {learning.id}"
            )
            
        except Exception as e:
            self.log_test("Reject low confidence", False, str(e))
            raise
    
    async def test_5_get_pending_learnings(self):
        """Test 5: Get pending learnings"""
        print("\n🧪 Test 5: Get pending learnings")
        
        try:
            # Create a pending learning
            await self.learning_service.create_learning_log(
                agent_id=TEST_AGENT_ID,
                learning_type="memory_added",
                source_data={
                    "content": "Como funciona?",
                    "chunk_type": "faq",
                    "metadata": {}
                },
                analysis={"detected_pattern": "frequent_question"},
                confidence=0.6  # Medium confidence
            )
            
            # Get pending learnings
            pending = await self.learning_service.get_pending_learnings(
                agent_id=TEST_AGENT_ID,
                limit=10
            )
            
            # Should have at least one pending
            assert len(pending) >= 1
            
            # All should be pending status
            for learning in pending:
                assert learning.status == "pending"
            
            self.log_test(
                "Get pending learnings",
                True,
                f"Found {len(pending)} pending learnings"
            )
            
        except Exception as e:
            self.log_test("Get pending learnings", False, str(e))
            raise
    
    async def test_6_get_learning_stats(self):
        """Test 6: Get learning statistics"""
        print("\n🧪 Test 6: Get learning statistics")
        
        try:
            stats = await self.learning_service.get_learning_stats(
                agent_id=TEST_AGENT_ID
            )
            
            # Verify stats structure
            assert "total_learnings" in stats
            assert "pending" in stats
            assert "approved" in stats
            assert "rejected" in stats
            assert "applied" in stats
            assert "avg_confidence" in stats
            
            # Should have some learnings from previous tests
            assert stats["total_learnings"] > 0
            
            self.log_test(
                "Get learning statistics",
                True,
                f"Total: {stats['total_learnings']}, "
                f"Pending: {stats['pending']}, "
                f"Approved: {stats['approved']}, "
                f"Rejected: {stats['rejected']}"
            )
            
        except Exception as e:
            self.log_test("Get learning statistics", False, str(e))
            raise
    
    async def test_7_batch_approve(self):
        """Test 7: Batch approve learnings"""
        print("\n🧪 Test 7: Batch approve learnings")
        
        try:
            # Create multiple pending learnings
            learning_ids = []
            
            for i in range(3):
                learning = await self.learning_service.create_learning_log(
                    agent_id=TEST_AGENT_ID,
                    learning_type="memory_added",
                    source_data={
                        "content": f"Termo: batch_term_{i}",
                        "chunk_type": "business_term",
                        "metadata": {"term": f"batch_term_{i}"}
                    },
                    analysis={"detected_pattern": "batch_test"},
                    confidence=0.7
                )
                learning_ids.append(learning.id)
            
            # Batch approve
            result = await self.learning_service.batch_approve_learnings(
                learning_ids=learning_ids,
                approved_by=TEST_PROFILE_ID
            )
            
            # Verify result
            assert result["total"] == 3
            assert result["approved"] == 3
            assert result["failed"] == 0
            
            self.log_test(
                "Batch approve learnings",
                True,
                f"Approved {result['approved']}/{result['total']} learnings"
            )
            
        except Exception as e:
            self.log_test("Batch approve learnings", False, str(e))
            raise
    
    async def test_8_batch_reject(self):
        """Test 8: Batch reject learnings"""
        print("\n🧪 Test 8: Batch reject learnings")
        
        try:
            # Create multiple pending learnings
            learning_ids = []
            
            for i in range(2):
                learning = await self.learning_service.create_learning_log(
                    agent_id=TEST_AGENT_ID,
                    learning_type="memory_added",
                    source_data={
                        "content": f"Termo: reject_term_{i}",
                        "chunk_type": "business_term",
                        "metadata": {"term": f"reject_term_{i}"}
                    },
                    analysis={"detected_pattern": "batch_reject_test"},
                    confidence=0.4
                )
                learning_ids.append(learning.id)
            
            # Batch reject
            result = await self.learning_service.batch_reject_learnings(
                learning_ids=learning_ids,
                rejected_by=TEST_PROFILE_ID,
                reason="Batch rejection test"
            )
            
            # Verify result
            assert result["total"] == 2
            assert result["rejected"] == 2
            assert result["failed"] == 0
            
            self.log_test(
                "Batch reject learnings",
                True,
                f"Rejected {result['rejected']}/{result['total']} learnings"
            )
            
        except Exception as e:
            self.log_test("Batch reject learnings", False, str(e))
            raise
    
    async def run_all_tests(self):
        """Run all validation tests"""
        print("=" * 70)
        print("🚀 SICC PHASE 3 VALIDATION - LEARNING SERVICE")
        print("=" * 70)
        
        try:
            # Setup
            await self.setup_test_data()
            
            # Run tests
            await self.test_1_analyze_conversations()
            learning = await self.test_2_create_learning_log()
            await self.test_3_auto_approve_high_confidence(learning)
            await self.test_4_reject_low_confidence()
            await self.test_5_get_pending_learnings()
            await self.test_6_get_learning_stats()
            await self.test_7_batch_approve()
            await self.test_8_batch_reject()
            
        finally:
            # Cleanup
            await self.cleanup_test_data()
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        print(f"📈 Success Rate: {self.tests_passed}/{self.tests_passed + self.tests_failed} ({100 * self.tests_passed / (self.tests_passed + self.tests_failed):.1f}%)")
        print("=" * 70)
        
        if self.tests_failed == 0:
            print("\n🎉 ALL TESTS PASSED! Phase 3 is complete.")
            return True
        else:
            print(f"\n⚠️  {self.tests_failed} test(s) failed. Please review.")
            return False


async def main():
    """Main validation function"""
    validator = Phase3Validator()
    success = await validator.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
