"""
Force Supabase PostgREST Schema Reload
Sprint 10 - SICC Implementation

Attempts to force PostgREST to reload schema cache using multiple methods.
"""

import sys
import time
sys.path.insert(0, 'src')

from src.config.supabase import supabase_admin
from uuid import uuid4

print("="*60)
print("FORCING SUPABASE SCHEMA RELOAD")
print("="*60)

# METHOD 1: Try NOTIFY (official PostgREST method)
print("\n[METHOD 1] Attempting NOTIFY pgrst...")
try:
    result = supabase_admin.rpc('notify_schema_reload').execute()
    print("✅ NOTIFY sent successfully")
    print("   Waiting 5 seconds for reload...")
    time.sleep(5)
except Exception as e:
    print(f"⚠️  NOTIFY failed (expected if function doesn't exist): {e}")

# METHOD 2: Insert test data to force detection
print("\n[METHOD 2] Inserting test data to force schema detection...")
try:
    test_agent_id = str(uuid4())
    
    # Create minimal test embedding (384 dimensions of zeros)
    test_embedding = [0.0] * 384
    
    # Try to insert test memory
    test_data = {
        "agent_id": test_agent_id,
        "content": "Schema cache test - safe to delete",
        "memory_type": "business_term",
        "embedding": test_embedding,
        "metadata": {"test": True},
        "source": "schema_reload_script",
        "confidence": 1.0,
        "importance": 0.1,
        "version": 1
    }
    
    print(f"   Inserting test record with agent_id: {test_agent_id}")
    result = supabase_admin.table("agent_memory_chunks").insert(test_data).execute()
    
    if result.data:
        print("✅ Test data inserted successfully")
        test_id = result.data[0]['id']
        
        # Delete test data
        print(f"   Cleaning up test record {test_id}...")
        supabase_admin.table("agent_memory_chunks").delete().eq("id", test_id).execute()
        print("✅ Test data cleaned up")
        print("✅ Schema cache should now be refreshed!")
    else:
        print("⚠️  Insert returned no data")
        
except Exception as e:
    print(f"❌ Insert method failed: {e}")
    print(f"   Error type: {type(e).__name__}")

# METHOD 3: Try behavior patterns table
print("\n[METHOD 3] Testing behavior patterns table...")
try:
    test_agent_id = str(uuid4())
    
    test_pattern = {
        "agent_id": test_agent_id,
        "pattern_type": "dialogue_strategy",
        "pattern_name": "Schema cache test",
        "description": "Test pattern - safe to delete",
        "trigger_conditions": {"test": True},
        "actions": {"test": True},
        "confidence": 1.0,
        "version": 1
    }
    
    print(f"   Inserting test pattern with agent_id: {test_agent_id}")
    result = supabase_admin.table("agent_behavior_patterns").insert(test_pattern).execute()
    
    if result.data:
        print("✅ Test pattern inserted successfully")
        test_id = result.data[0]['id']
        
        # Delete test data
        print(f"   Cleaning up test pattern {test_id}...")
        supabase_admin.table("agent_behavior_patterns").delete().eq("id", test_id).execute()
        print("✅ Test pattern cleaned up")
        print("✅ Schema cache refreshed for behavior patterns!")
    else:
        print("⚠️  Insert returned no data")
        
except Exception as e:
    print(f"❌ Pattern insert failed: {e}")
    print(f"   Error type: {type(e).__name__}")

# VERIFICATION
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

print("\nAttempting to query tables...")

# Test memory chunks
try:
    result = supabase_admin.table("agent_memory_chunks").select("*").limit(1).execute()
    print("✅ agent_memory_chunks: Accessible")
except Exception as e:
    print(f"❌ agent_memory_chunks: {e}")

# Test behavior patterns
try:
    result = supabase_admin.table("agent_behavior_patterns").select("*").limit(1).execute()
    print("✅ agent_behavior_patterns: Accessible")
except Exception as e:
    print(f"❌ agent_behavior_patterns: {e}")

print("\n" + "="*60)
print("RECOMMENDATION")
print("="*60)
print("\nIf tables are now accessible:")
print("  → Run: python validate_sicc_phase1.py")
print("\nIf still failing:")
print("  → Wait 5-10 minutes for automatic reload")
print("  → Or restart PostgREST via Supabase Dashboard")
print("="*60)
