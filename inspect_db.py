from supabase import create_client
import os

# Dados capturados do settings.py e .env.example
URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SERVICE_KEY = "your_service_key_here" # Vou tentar ler do .env via Python

def get_config():
    conf = {}
    try:
        with open("backend/.env", "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    conf[k] = v
    except:
        pass
    return conf

def find_client():
    conf = get_config()
    url = conf.get("SUPABASE_URL")
    key = conf.get("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        print("Could not find Supabase config in .env")
        return
    
    supabase = create_client(url, key)
    
    print("Listing clients from DB...")
    res = supabase.table("clients").select("id, company_name").limit(5).execute()
    if res.data:
        for c in res.data:
            print(f"CLIENT: {c['company_name']} ID: {c['id']}")
    else:
        print("No clients in database table 'clients'")

    print("\nTesting Pydantic serialization for agents...")
    import sys
    sys.path.append("backend")
    from src.models.agent import AgentListItem
    
    res = supabase.table("agents").select("*").execute()
    if res.data:
        print(f"Found {len(res.data)} agents.")
        for a in res.data:
            try:
                # Tratar datas (se necessário, Pydantic costuma aceitar string ISO)
                item = AgentListItem(**a)
                print(f"SUCCESS: Agent {a['name']} serialized.")
            except Exception as e:
                print(f"FAILURE: Agent {a['name']} failed serialization: {e}")
                import json
                print(f"Data: {json.dumps(a, indent=2, default=str)}")
    else:
        print("No agents in database")

if __name__ == "__main__":
    find_client()
