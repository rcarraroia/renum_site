#!/usr/bin/env python3
"""
Check database constraints and enum values
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.supabase import supabase_admin

def check_memory_constraints():
    """Check memory table constraints"""
    print("🔍 Checking agent_memory_chunks constraints...")
    
    # Get table info
    result = supabase_admin.table("agent_memory_chunks").select("*").limit(1).execute()
    print(f"Table exists: {len(result.data) >= 0}")
    
    # Try to insert with different source values to see what's valid
    test_sources = [
        "conversation",
        "manual", 
        "api",
        "property_test",
        "test"
    ]
    
    for source in test_sources:
        try:
            # Try a minimal insert to test constraint
            test_data = {
                "agent_id": "37ae9902-24bf-42b1-9d01-88c201ee0a6c",
                "client_id": "9e26202e-7090-4051-9bfd-6b397b3947cc",
                "content": f"Test content for {source}",
                "chunk_type": "faq",
                "embedding": [0.1] * 384,
                "source": source,
                "confidence_score": 0.8
            }
            
            result = supabase_admin.table("agent_memory_chunks").insert(test_data).execute()
            print(f"✅ Source '{source}' is VALID")
            
            # Clean up
            if result.data:
                supabase_admin.table("agent_memory_chunks").delete().eq("id", result.data[0]["id"]).execute()
                
        except Exception as e:
            print(f"❌ Source '{source}' is INVALID: {str(e)}")

def check_pattern_types():
    """Check behavior pattern types"""
    print("\n🔍 Checking behavior pattern types...")
    
    test_types = [
        "response_optimization",
        "conversation_flow", 
        "error_handling",
        "user_engagement",
        "RESPONSE_OPTIMIZATION",
        "CONVERSATION_FLOW"
    ]
    
    for pattern_type in test_types:
        try:
            test_data = {
                "agent_id": "37ae9902-24bf-42b1-9d01-88c201ee0a6c",
                "client_id": "9e26202e-7090-4051-9bfd-6b397b3947cc",
                "pattern_type": pattern_type,
                "trigger_context": {"test": True},
                "action_config": {"test": True},
                "success_rate": 0.5,
                "total_applications": 1
            }
            
            result = supabase_admin.table("agent_behavior_patterns").insert(test_data).execute()
            print(f"✅ Pattern type '{pattern_type}' is VALID")
            
            # Clean up
            if result.data:
                supabase_admin.table("agent_behavior_patterns").delete().eq("id", result.data[0]["id"]).execute()
                
        except Exception as e:
            print(f"❌ Pattern type '{pattern_type}' is INVALID: {str(e)}")

def check_metrics_table():
    """Check metrics table structure"""
    print("\n🔍 Checking metrics table...")
    
    try:
        # Get today's metrics if any
        from datetime import date
        today = date.today()
        
        result = supabase_admin.table("agent_performance_metrics").select("*").eq(
            "agent_id", "37ae9902-24bf-42b1-9d01-88c201ee0a6c"
        ).eq("metric_date", today.isoformat()).execute()
        
        print(f"Today's metrics found: {len(result.data)}")
        if result.data:
            print(f"Sample data: {result.data[0]}")
            
    except Exception as e:
        print(f"❌ Error checking metrics: {e}")

if __name__ == "__main__":
    check_memory_constraints()
    check_pattern_types()
    check_metrics_table()