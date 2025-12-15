"""
Script para ver detalhes do GET /api/clients
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Ler token
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_get_clients():
    print("🔍 Testando GET /api/clients com detalhes...\n")
    
    response = requests.get(f"{BASE_URL}/api/clients", headers=HEADERS)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResposta completa:")
        print(json.dumps(data, indent=2))
    else:
        print(f"❌ Erro: {response.text}")

if __name__ == "__main__":
    test_get_clients()
