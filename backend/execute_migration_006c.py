"""
Execute Migration 006c - Add channel column to messages
"""

import psycopg2
import os
from dotenv import load_dotenv

def execute_migration():
    """Execute migration 006c"""
    
    print("="*60)
    print("EXECUTING MIGRATION 006c")
    print("Adding channel column to messages table")
    print("="*60)
    
    load_dotenv()
    
    # Read migration file
    with open('migrations/006c_add_channel_to_messages.sql', 'r') as f:
        sql = f.read()
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        print("\n📝 Executing SQL...")
        cur.execute(sql)
        conn.commit()
        
        print("✅ Migration executed successfully!")
        
        # Verify column was added
        print("\n🔍 Verifying column...")
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'messages'
            AND column_name = 'channel'
        """)
        
        result = cur.fetchone()
        if result:
            print(f"✅ Column 'channel' verified: {result[0]} ({result[1]})")
        else:
            print("⚠️  Could not verify column")
        
        cur.close()
        conn.close()
        
        print("\n" + "="*60)
        print("MIGRATION 006c COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    execute_migration()
