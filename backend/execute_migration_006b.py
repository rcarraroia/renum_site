"""
Execute Migration 006b - Add config column to sub_agents
"""

from src.config.supabase import supabase_admin
from src.utils.logger import logger

def execute_migration():
    """Execute migration 006b"""
    
    print("="*60)
    print("EXECUTING MIGRATION 006b")
    print("Adding config JSONB column to sub_agents")
    print("="*60)
    
    # Read migration file
    with open('migrations/006b_add_config_column.sql', 'r') as f:
        sql = f.read()
    
    try:
        # Execute migration
        print("\n📝 Executing SQL...")
        result = supabase_admin.rpc('exec_sql', {'sql': sql}).execute()
        
        print("✅ Migration executed successfully!")
        
        # Verify column was added
        print("\n🔍 Verifying column...")
        verify_result = supabase_admin.table('sub_agents').select('config').limit(1).execute()
        
        if verify_result.data is not None:
            print("✅ Column 'config' verified!")
        else:
            print("⚠️  Could not verify column (table might be empty)")
        
        print("\n" + "="*60)
        print("MIGRATION 006b COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        print("\nTrying alternative approach...")
        
        # Alternative: Execute via psycopg2 if available
        try:
            import psycopg2
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            cur = conn.cursor()
            
            cur.execute(sql)
            conn.commit()
            
            cur.close()
            conn.close()
            
            print("✅ Migration executed via psycopg2!")
            
        except Exception as e2:
            print(f"❌ Alternative approach also failed: {str(e2)}")
            print("\nPlease execute the migration manually in Supabase SQL Editor:")
            print("migrations/006b_add_config_column.sql")
            raise

if __name__ == "__main__":
    execute_migration()
