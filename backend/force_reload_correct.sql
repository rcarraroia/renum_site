-- ============================================================
-- FORCE POSTGREST SCHEMA CACHE RELOAD - CORRECT SCHEMA
-- Sprint 10 - SICC Implementation
-- Using REAL column names from database
-- ============================================================

-- STEP 1: Test agent_memory_chunks (with correct column names)
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
    gen_random_uuid(),
    gen_random_uuid(),
    'business_term',
    'SCHEMA CACHE TEST - Safe to delete',
    ARRAY(SELECT 0.0 FROM generate_series(1, 384))::vector(384),
    '{"test": true, "purpose": "force_schema_reload"}'::jsonb,
    'sql_force_reload',
    1.0,
    1
);

-- Delete test data
DELETE FROM agent_memory_chunks 
WHERE source = 'sql_force_reload';

-- STEP 2: Test agent_behavior_patterns (with correct column names)
INSERT INTO agent_behavior_patterns (
    agent_id,
    client_id,
    pattern_type,
    trigger_context,
    action_config,
    success_rate,
    version
) VALUES (
    gen_random_uuid(),
    gen_random_uuid(),
    'dialogue_strategy',
    '{"test": true, "purpose": "force_schema_reload"}'::jsonb,
    '{"test": true}'::jsonb,
    0.0,
    1
);

-- Delete test data  
DELETE FROM agent_behavior_patterns 
WHERE trigger_context @> '{"purpose": "force_schema_reload"}'::jsonb;

-- STEP 3: Verify tables
SELECT 
    'agent_memory_chunks' as table_name,
    COUNT(*) as record_count
FROM agent_memory_chunks

UNION ALL

SELECT 
    'agent_behavior_patterns' as table_name,
    COUNT(*) as record_count
FROM agent_behavior_patterns;

-- ============================================================
-- ✅ SUCCESS - Schema cache should now be reloaded!
-- ============================================================
