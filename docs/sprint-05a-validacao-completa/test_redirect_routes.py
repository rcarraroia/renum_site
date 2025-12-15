"""
Teste de rotas que podem estar retornando 307 redirect
"""
import requests

BASE_URL = "http://localhost:8000"

# Token do admin
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("="*70)
print("TESTE ROTAS REDIRECT 307")
print("="*70)

routes = [
    "/api/sub-agents",
    "/api/sub-agents/",
    "/api/renus-config",
    "/api/renus-config/"
]

for route in routes:
    print(f"\nTestando: {route}")
    try:
        response = requests.get(f"{BASE_URL}{route}", headers=HEADERS, allow_redirects=False, timeout=5)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 307:
            print(f"  ❌ REDIRECT 307")
            print(f"  Location: {response.headers.get('Location', 'N/A')}")
        elif response.status_code == 200:
            print(f"  ✅ OK")
        else:
            print(f"  ⚠️ Outro status: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)[:50]}")

print("\n" + "="*70)
