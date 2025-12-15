
import json
import os
import glob
from datetime import datetime
from supabase import create_client

# Conexão
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    exit(1)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_table(table_name):
    print(f"Backing up {table_name}...")
    try:
        response = supabase.table(table_name).select("*").execute()
        filename = f"backup_{table_name}_{timestamp}.json"
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(response.data, f, indent=2, default=str)
        print(f"✓ Saved {len(response.data)} records to {filename}")
        return len(response.data)
    except Exception as e:
        print(f"❌ Error backing up {table_name}: {e}")
        return 0

# Backup renus_config
backup_table("renus_config")

# Backup sub_agents
backup_table("sub_agents")

# Backup isa_commands
backup_table("isa_commands")

print("\n✅ BACKUP COMPLETO")
print(f"Timestamp: {timestamp}")
