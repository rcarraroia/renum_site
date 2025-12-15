
import json
from datetime import datetime
from supabase import create_client

# Conexão
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Backing up EXISTING 'agents' table (for safety before DROP)...")
    response = supabase.table("agents").select("*").execute()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_agents_conflict_{timestamp}.json"
    
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(response.data, f, indent=2, default=str)
        
    print(f"✓ Saved {len(response.data)} records to {filename}")
    
    if len(response.data) > 0:
        print("⚠️ AVISO: A tabela agents NÃO ESTAVA VAZIA.")
        print("Dados preservados no arquivo acima.")
    else:
        print("ℹ️ A tabela agents estava vazia (seguro para drop).")

except Exception as e:
    print(f"❌ Erro ao acessar tabela agents (talvez ela nem exista?): {e}")

