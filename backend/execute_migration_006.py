#!/usr/bin/env python3
"""
Execute Migration 006: Add Wizard Fields to sub_agents
Sprint 06 - Wizard de Criação de Agentes
"""

import psycopg2
from pathlib import Path

def execute_migration():
    """Execute migration 006"""
    print("=" * 60)
    print("EXECUTING MIGRATION 006")
    print("Add Wizard Fields to sub_agents")
    print("=" * 60)
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(
            host='db.vhixvzaxswphwoymdhgg.supabase.co',
            port=5432,
            database='postgres',
            user='postgres',
            password='BD5yEMQ9iDMOkeGW'
        )
        
        conn.autocommit = False
        cur = conn.cursor()
        
        # Read migration file
        migration_file = Path(__file__).parent / 'migrations' / '006_add_wizard_fields_to_sub_agents.sql'
        
        print(f"\n📄 Reading migration file: {migration_file}")
        
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Split by verification queries (we'll run those separately)
        parts = sql.split('-- VERIFICATION QUERIES')
        migration_sql = parts[0]
        verification_sql = parts[1] if len(parts) > 1 else ''
        
        print("\n🔄 Executing migration...")
        
        # Execute migration
        cur.execute(migration_sql)
        
        print("✅ Migration executed successfully")
        
        # Commit transaction
        conn.commit()
        print("✅ Transaction committed")
        
        # Run verification queries
        if verification_sql:
            print("\n🔍 Running verification queries...")
            
            # Extract individual queries
            queries = [q.strip() for q in verification_sql.split(';') if q.strip() and not q.strip().startswith('--')]
            
            for i, query in enumerate(queries, 1):
                if query:
                    print(f"\n--- Query {i} ---")
                    cur.execute(query)
                    results = cur.fetchall()
                    
                    if results:
                        for row in results:
                            print(f"  {row}")
                    else:
                        print("  (no results)")
        
        cur.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION 006 COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        if 'conn' in locals():
            conn.rollback()
            print("⚠️ Transaction rolled back")
        return False

if __name__ == "__main__":
    success = execute_migration()
    exit(0 if success else 1)
