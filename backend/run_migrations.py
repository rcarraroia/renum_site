"""
Execute Sprint 07A migrations on Supabase
"""

import psycopg2
from pathlib import Path

# Connection string
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def run_migration(cursor, migration_file: Path):
    """Execute a single migration file"""
    print(f"\n📄 Executing: {migration_file.name}")
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    try:
        cursor.execute(sql)
        print(f"✅ {migration_file.name} executed successfully")
        return True
    except Exception as e:
        print(f"❌ Error in {migration_file.name}: {e}")
        return False

def main():
    print("=" * 60)
    print("SPRINT 07A - EXECUTING MIGRATIONS")
    print("=" * 60)
    
    # Connect to database
    print("\n🔌 Connecting to Supabase...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False  # Use transactions
        cursor = conn.cursor()
        print("✅ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return 1
    
    # Migration files in order
    migrations_dir = Path(__file__).parent / "migrations"
    migration_files = [
        migrations_dir / "006_create_update_function.sql",
        migrations_dir / "007_create_integrations_table.sql",
        migrations_dir / "008_create_triggers_table.sql",
        migrations_dir / "009_create_trigger_executions_table.sql",
    ]
    
    # Execute migrations
    success_count = 0
    for migration_file in migration_files:
        if not migration_file.exists():
            print(f"❌ Migration file not found: {migration_file}")
            continue
        
        if run_migration(cursor, migration_file):
            success_count += 1
        else:
            print("\n⚠️  Migration failed. Rolling back...")
            conn.rollback()
            cursor.close()
            conn.close()
            return 1
    
    # Commit all migrations
    print("\n💾 Committing changes...")
    try:
        conn.commit()
        print("✅ All migrations committed successfully")
    except Exception as e:
        print(f"❌ Commit failed: {e}")
        conn.rollback()
        cursor.close()
        conn.close()
        return 1
    
    # Verify tables created
    print("\n🔍 Verifying tables...")
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('integrations', 'triggers', 'trigger_executions')
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    print(f"Found {len(tables)} tables:")
    for table in tables:
        print(f"  ✅ {table[0]}")
    
    # Verify RLS enabled
    print("\n🔒 Verifying RLS...")
    cursor.execute("""
        SELECT tablename, rowsecurity 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename IN ('integrations', 'triggers', 'trigger_executions')
        ORDER BY tablename;
    """)
    
    rls_status = cursor.fetchall()
    for table, enabled in rls_status:
        status = "✅ Enabled" if enabled else "❌ Disabled"
        print(f"  {table}: {status}")
    
    # Close connection
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print(f"✅ MIGRATIONS COMPLETED: {success_count}/{len(migration_files)}")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
