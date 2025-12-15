"""
Insert test data via raw SQL to bypass PostgREST cache
Sprint 10 - SICC Implementation
"""

import sys
sys.path.insert(0, 'src')

from src.config.supabase import supabase_admin
from uuid import uuid4
import json

print("="*60)
print("INSERTING VIA RAW SQL (BYPASS POSTGREST CACHE)")
print("="*60)

test_agent_id = str(uuid4())
test_embedding = [0.0] * 384

# Try to execute raw SQL via Supabase
print("\nAttempting raw SQL insert...")

sql_query = f"""
INSERT INTO agent_memory_chunks (
    agent_id,
    content,
    memory_type,
    embedding,
    metadata,
    source,
    confidence,
    importance,
    version
) VALUES (
    '{test_agent_id}',
    'Schema cache test - safe to delete',
    'business_term',
    ARRAY{test_embedding}::vector(384),
    '{{"test": true}}'::jsonb,
    'sql_direct_insert',
    1.0,
    0.1,
    1
) RETURNING id;
"""

print(f"SQL Query prepared for agent_id: {test_agent_id}")
print("\nNote: Supabase may not allow direct SQL execution via client.")
print("Alternative: Use Supabase Dashboard → SQL Editor")
print("\nSQL to execute:")
print("-" * 60)
print(sql_query)
print("-" * 60)

print("\n✅ SOLUTION: Execute this SQL in Supabase Dashboard")
print("\nSteps:")
print("1. Go to: https://supabase.com/dashboard/project/vhixvzaxswphwoymdhgg/sql")
print("2. Paste the SQL above")
print("3. Click 'Run'")
print("4. Then run: python validate_sicc_phase1.py")
print("\nThis will force PostgREST to reload the schema cache.")
print("="*60)
