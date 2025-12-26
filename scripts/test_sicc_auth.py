"""
Script para testar autenticação SICC com token de usuário admin
"""
import requests

# Token do admin (obtido via login)
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6InJVaFpFT2VXWnpjRmpNc3YiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3ZoaXh2emF4c3dwaHdveW1kaGdnLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI4NzZiZTMzMS05NTUzLTRlOWEtOWYyOS02M2NmYTcxMWUwNTYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY2MzczNDA1LCJpYXQiOjE3NjYzNjk4MDUsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcnN0X25hbWUiOiJBZG1pbiIsImxhc3RfbmFtZSI6IlJlbnVtIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NjYzNjk4MDV9XSwic2Vzc2lvbl9pZCI6ImQxYmM3NDg4LTg4M2EtNDFiZS04ZTgwLWZiYWM3ODBjMzU2ZiIsImlzX2Fub255bW91cyI6ZmFsc2V9.s5ldkuNNWzaK0jgc32y-nPa04Tbd_KseGSxwI6yXDns"

BASE_URL = "http://localhost:8000"
AGENT_ID = "00000000-0000-0000-0000-000000000001"

headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

endpoints = [
    # Endpoints com dependencies.get_current_user
    ("Settings (dependencies)", f"/api/sicc/settings/{AGENT_ID}"),
    ("Commands (dependencies)", "/api/sicc/commands"),
    ("Status (dependencies)", "/api/sicc/status"),
    
    # Endpoints com auth_middleware.get_current_user
    ("Memories (auth_middleware)", f"/api/sicc/memories/?agent_id={AGENT_ID}"),
    ("Memory Stats (auth_middleware)", f"/api/sicc/memories/agent/{AGENT_ID}/stats"),
    ("Learnings (auth_middleware)", f"/api/sicc/learnings/?agent_id={AGENT_ID}"),
    ("Learning Stats (auth_middleware)", f"/api/sicc/learnings/agent/{AGENT_ID}/stats"),
    ("Patterns (auth_middleware)", f"/api/sicc/patterns/?agent_id={AGENT_ID}"),
    ("Pattern Stats (auth_middleware)", f"/api/sicc/patterns/agent/{AGENT_ID}/stats"),
    ("Dashboard Stats (auth_middleware)", f"/api/sicc/stats/agent/{AGENT_ID}/dashboard"),
    ("Agent Metrics (auth_middleware)", f"/api/sicc/stats/agent/{AGENT_ID}/metrics"),
    
    # Endpoint de auth para comparação
    ("Auth Me (auth_middleware)", "/auth/me"),
]

print("=" * 60)
print("TESTE DE AUTENTICAÇÃO SICC COM TOKEN ADMIN")
print("=" * 60)
print()

for name, endpoint in endpoints:
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=headers, timeout=10)
        status = response.status_code
        
        if status == 200:
            print(f"✅ {name}: {status} OK")
        elif status == 401:
            print(f"❌ {name}: {status} UNAUTHORIZED")
        elif status == 403:
            print(f"❌ {name}: {status} FORBIDDEN")
        else:
            print(f"⚠️ {name}: {status}")
            
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")

print()
print("=" * 60)
