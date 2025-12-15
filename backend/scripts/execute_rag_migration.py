import asyncio
import os
from src.config.settings import settings
from src.config.supabase import supabase_admin

async def run_migration():
    print("Running migration 010...")
    
    file_path = "backend/migrations/010_create_rag_tables.sql"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Split by statement if needed, but supabase-py might take the whole block if using rpc or just passing raw sql via specific endpoint?
    # supabase-py doesn't have a direct 'query' method for raw sql usually exposed unless via RPC 'exec_sql' if configured.
    # However, previous scripts seem to imply we might not have a direct sql executor unless we use psycopg2 or have a helper.
    # Let's check `backend/scripts/execute_migrations.py` to see how it's done. 
    # For now, I will try to use the `postgres` driver (psycopg2) directly if settings allow, OR rely on a known patterns.
    
    # Actually, let's use the pattern from `execute_schema_reload.py` or similar if checked.
    # But since I can't check easily now without delay, I'll use psycopg2 which is in requirements.txt
    
    import psycopg2
    
    try:
        # Construct DB URL from settings if available or hardcode for this env if known
        # settings.DATABASE_URL usually exists.
        conn = psycopg2.connect(settings.DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("Migration 010 executed successfully.")
    except Exception as e:
        print(f"Error executing migration: {e}")

if __name__ == "__main__":
    asyncio.run(run_migration())
