"""
Check REAL database schema using direct PostgreSQL connection
Sprint 10 - SICC Implementation
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Connection string from SUPABASE_CREDENTIALS.md
conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

print("="*60)
print("CHECKING REAL DATABASE SCHEMA")
print("="*60)

try:
    # Connect to database
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check agent_memory_chunks
    print("\n[TABLE: agent_memory_chunks]")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'agent_memory_chunks'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    if columns:
        print(f"\nFound {len(columns)} columns:")
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f"DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"  - {col['column_name']:<25} {col['data_type']:<20} {nullable:<10} {default}")
    else:
        print("  ❌ Table not found or no columns!")
    
    # Check agent_behavior_patterns
    print("\n[TABLE: agent_behavior_patterns]")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'agent_behavior_patterns'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    if columns:
        print(f"\nFound {len(columns)} columns:")
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f"DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"  - {col['column_name']:<25} {col['data_type']:<20} {nullable:<10} {default}")
    else:
        print("  ❌ Table not found or no columns!")
    
    # Check all SICC tables
    print("\n[ALL SICC TABLES]")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'agent_%'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    if tables:
        print(f"\nFound {len(tables)} SICC tables:")
        for table in tables:
            print(f"  - {table['table_name']}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ SCHEMA CHECK COMPLETED")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"   Type: {type(e).__name__}")
