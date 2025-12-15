
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load env from backend/.env if available
backend_env = os.path.join(os.getcwd(), 'backend', '.env')
if os.path.exists(backend_env):
    load_dotenv(backend_env)

# Try environment vars first, then fallback to hardcoded (if valid, but likely masked)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://vhixvzaxswphwoymdhgg.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_KEY") 

# If key is masked/missing, this will fail.
if not SUPABASE_SERVICE_KEY:
    # Try the one from the file, even if looks masked
    SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def main():
    print(f"Connecting to {SUPABASE_URL}")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # List all
        print("Checking 'sub_agents' table for LEGACY COMPATIBILITY...")
        response = supabase.table('sub_agents').select('id, name, slug').execute()
        
        renus_id = None
        renus_slug = None
        renus_found = False
        
        for agent in response.data:
            slug = agent.get('slug') # Can be None
            name = agent.get('name', 'NO_NAME')
            aid = agent.get('id')
            
            print(f"Found Legacy: {name} (Slug: {slug})")
            
            # Check by name or slug
            is_renus = (slug == 'renus') or (name and 'renus' in name.lower())

            if is_renus:
                renus_found = True
                renus_slug = slug
                renus_id = aid
                # If slug is missing or wrong, we will fix
                if slug != 'renus':
                    print(f"[WARN] Legacy Renus found but has invalid slug: {slug}. Will UPDATE.")
                    renus_slug = None # Trigger update logic

        if renus_found and renus_slug == 'renus':
            print(f"[OK] EXACT MATCH: Legacy Renus with slug 'renus' EXISTS and is valid.")
            # Ensure is_public
            try:
                upd = supabase.table('sub_agents').update({'is_public': True}).eq('id', renus_id).execute()
                print(f"[OK] Legacy Renus Public Status Updated: {upd.data}")
            except Exception as upd_pub_err:
                 print(f"[ERROR] Error updating Legacy Renus Public: {upd_pub_err}")

        elif renus_found and renus_id:
            print(f"[ACTION] Updating Legacy Renus (ID: {renus_id}) with slug 'renus'...")
            try:
                upd = supabase.table('sub_agents').update({'slug': 'renus', 'is_public': True}).eq('id', renus_id).execute()
                print(f"[OK] Legacy Renus Updated: {upd.data}")
            except Exception as upd_err:
                print(f"[ERROR] Error updating Legacy Renus: {upd_err}")

        else:
            print("[WARN] Legacy Renus NOT FOUND. Creating...")
            data = {
                "name": "Renus [Legacy Sync]",
                "slug": "renus",
                "model": "gpt-4o-mini",
                "channel": "web", # Required for sub_agents
                "is_public": True,
                "is_active": True,
                "system_prompt": "You are Renus, the orchestrator."
            }
            try:
                res = supabase.table('sub_agents').insert(data).execute()
                print(f"[OK] Legacy Renus Created: {res.data}")
            except Exception as insert_err:
                print(f"[ERROR] Error creating Legacy Renus: {insert_err}")
                
    except Exception as e:
        print(f"[ERROR] Connection/Auth Error: {e}")

if __name__ == "__main__":
    main()
