"""
Script para testar endpoints de interviews
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

def test_list_interviews():
    print("🔍 Testando GET /api/interviews...\n")
    
    response = requests.get(f"{BASE_URL}/api/interviews", headers=HEADERS)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sucesso!")
        print(f"   Total: {data.get('total', len(data))}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TESTE - INTERVIEWS")
    print("="*60)
    
    success = test_list_interviews()
    
    print("\n" + "="*60)
    print("RESUMO - INTERVIEWS")
    print("="*60)
    status = "✅" if success else "❌"
    print(f"{status} LIST")
    print("="*60)
