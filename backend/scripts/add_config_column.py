import os
import psycopg2
from dotenv import load_dotenv

# Load env vars
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    # Try constructing it if possible or look for other names
    DB_URL = os.getenv("SUPABASE_DB_URL")

if not DB_URL:
    print("❌ Error: DATABASE_URL not found in .env. Cannot verify/migrate DB.")
    # Fallback: try to construct if we have password. Usually Supabase URL is:
    # postgres://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
    # But we don't have password visible in settings.py, only keys.
    # Exiting.
    exit(1)

try:
    print(f"🔌 Connecting to DB...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # 1. Check if column exists
    print("🔍 Checking 'config' column in 'agents' table...")
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='agents' AND column_name='config';
    """)
    result = cur.fetchone()

    if result:
        print("✅ Column 'config' already exists.")
    else:
        print("🛠️ Column 'config' missing. Adding it now...")
        cur.execute("ALTER TABLE agents ADD COLUMN config JSONB DEFAULT '{}'::jsonb;")
        print("✅ Column 'config' added successfully.")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"❌ Database error: {e}")
    exit(1)
