"""
BUG #7 - Teste Simples do Endpoint POST /api/interviews/start
"""

import requests

BASE_URL = "http://localhost:8000"

# Ler token
with open("backend/test_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_interviews_simple():
    """Testa endpoint POST /api/interviews/start sem dependências"""
    
    print("\n" + "=" * 60)
    print("TESTE BUG #7 - INTERVIEWS ENDPOINT (SIMPLES)")
    print("=" * 60)
    
    # Teste 1: Criar interview sem lead_id
    print("\n1. POST /api/interviews/start (sem lead_id)")
    
    response = requests.post(
        f"{BASE_URL}/api/interviews/start",
        headers=HEADERS,
        json={},
        timeout=5
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        print("   ✅ SUCESSO")
        data = response.json()
        print(f"   Interview ID: {data.get('id')}")
        print(f"   Status: {data.get('status')}")
    else:
        print(f"   ❌ FALHOU")
        print(f"   Response: {response.text}")
    
    # Teste 2: Listar interviews
    print("\n2. GET /api/interviews")
    
    response = requests.get(
        f"{BASE_URL}/api/interviews",
        headers=HEADERS,
        timeout=5
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        total = data.get("total", 0)
        print(f"   ✅ SUCESSO - {total} interviews encontradas")
    else:
        print(f"   ❌ FALHOU")
        print(f"   Response: {response.text}")
    
    print("\n" + "=" * 60)
    print("CONCLUSÃO:")
    print("✅ BUG #7 CORRIGIDO se ambos os testes passaram")
    print("=" * 60)
    print()

if __name__ == "__main__":
    test_interviews_simple()
