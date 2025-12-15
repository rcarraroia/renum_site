
import os
import sys
import psycopg2

# Credentials from supabase-credentials.md
DB_HOST = "db.vhixvzaxswphwoymdhgg.supabase.co"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "BD5yEMQ9iDMOkeGW"
DB_PORT = "5432"

MIGRATION_FILE = r'backend\migrations\007_create_integrations_table.sql'

def run_migration():
    try:
        # Establish connection
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print(f"Connected to database {DB_NAME} at {DB_HOST}")
        
        # Read SQL file
        with open(MIGRATION_FILE, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        print(f"Executing migration: {MIGRATION_FILE}...")
        
        # Execute SQL
        cursor.execute(sql_content)
        
        print("Migration applied successfully! ✅")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error executing migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
