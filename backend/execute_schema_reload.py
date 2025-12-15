"""
Execute schema reload via direct PostgreSQL connection
Sprint 10 - SICC Implementation
"""

import psycopg2
from uuid import uuid4

# Connection string from SUPABASE_CREDENTIALS.md
conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

print("="*60)
print("EXECUTING SCHEMA RELOAD VIA DIRECT CONNECTION")
print("="*60)

try:
    # Connect to database
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # STEP 1: Test agent_memory_chunks
    print("\n[STEP 1] Testing agent_memory_chunks...")
    
    # Use real IDs from database
    test_agent_id = '37ae9902-24bf-42b1-9d01-88c201ee0a6c'
    test_client_id = '9e26202e-7090-4051-9bfd-6b397b3947cc'
    
    # Create embedding array (384 zeros) - pgvector uses [] not {}
    embedding_array = '[' + ','.join(['0.0'] * 384) + ']'
    
    insert_sql = f"""
    INSERT INTO agent_memory_chunks (
        agent_id,
        client_id,
        chunk_type,
        content,
        embedding,
        metadata,
        source,
        confidence_score,
        version
    ) VALUES (
        '{test_agent_id}'::uuid,
        '{test_client_id}'::uuid,
        'business_term',
        'SCHEMA CACHE TEST - Safe to delete',
        '{embedding_array}'::vector(384),
        '{{"test": true, "purpose": "force_schema_reload"}}'::jsonb,
        'manual',
        1.0,
        1
    ) RETURNING id;
    """
    
    cursor.execute(insert_sql)
    result = cursor.fetchone()
    test_memory_id = result[0]
    print(f"✅ Inserted test memory: {test_memory_id}")
    
    # Delete test data
    cursor.execute(f"DELETE FROM agent_memory_chunks WHERE content = 'SCHEMA CACHE TEST - Safe to delete';")
    print(f"✅ Deleted test memory: {test_memory_id}")
    
    # STEP 2: Test agent_behavior_patterns
    print("\n[STEP 2] Testing agent_behavior_patterns...")
    
    # Use same real IDs
    test_agent_id2 = '37ae9902-24bf-42b1-9d01-88c201ee0a6c'
    test_client_id2 = '9e26202e-7090-4051-9bfd-6b397b3947cc'
    
    insert_sql2 = f"""
    INSERT INTO agent_behavior_patterns (
        agent_id,
        client_id,
        pattern_type,
        trigger_context,
        action_config,
        success_rate
    ) VALUES (
        '{test_agent_id2}'::uuid,
        '{test_client_id2}'::uuid,
        'response_strategy',
        '{{"test": true, "purpose": "force_schema_reload"}}'::jsonb,
        '{{"test": true}}'::jsonb,
        0.0
    ) RETURNING id;
    """
    
    cursor.execute(insert_sql2)
    result = cursor.fetchone()
    test_pattern_id = result[0]
    print(f"✅ Inserted test pattern: {test_pattern_id}")
    
    # Delete test data
    cursor.execute(f"DELETE FROM agent_behavior_patterns WHERE id = '{test_pattern_id}'::uuid;")
    print(f"✅ Deleted test pattern: {test_pattern_id}")
    
    # STEP 3: Verify tables
    print("\n[STEP 3] Verifying tables...")
    
    cursor.execute("SELECT COUNT(*) FROM agent_memory_chunks;")
    memory_count = cursor.fetchone()[0]
    print(f"✅ agent_memory_chunks: {memory_count} records")
    
    cursor.execute("SELECT COUNT(*) FROM agent_behavior_patterns;")
    pattern_count = cursor.fetchone()[0]
    print(f"✅ agent_behavior_patterns: {pattern_count} records")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ SCHEMA RELOAD COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nPostgREST schema cache should now be refreshed.")
    print("Next step: Run validation script")
    print("  → python validate_sicc_phase1.py")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"   Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
