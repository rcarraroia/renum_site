"""
Script para testar endpoints de dashboard
"""
import requests
import json

BASE_URL = "http://localhost:8000"

with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_dashboard_stats():
    print("🔍 Testando GET /api/dashboard/stats...\n")
    
    response = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=HEADERS)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sucesso!")
        print(f"\nEstatísticas:")
        print(json.dumps(data, indent=2))
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TESTE - DASHBOARD")
    print("="*60)
    
    success = test_dashboard_stats()
    
    print("\n" + "="*60)
    print("RESUMO - DASHBOARD")
    print("="*60)
    status = "✅" if success else "❌"
    print(f"{status} STATS")
    print("="*60)
