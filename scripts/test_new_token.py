#!/usr/bin/env python3
"""
Testar o novo token JWT gerado
"""
import requests

def test_new_token():
    base_url = "http://localhost:8000"
    
    # Novo token gerado
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjczMjM5LCJpYXQiOjE3NjU1ODY4MzksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.HgEqRYi7ijWwaqj1Vkt-ofRIB5dWY4bRyDNGiKMpDsk"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:8083"
    }
    
    print("🔍 Testando novo token JWT...")
    
    # Teste 1: Dashboard stats
    try:
        response = requests.get(f"{base_url}/api/dashboard/stats", headers=headers, timeout=5)
        print(f"✅ Dashboard stats: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ DADOS REAIS CARREGADOS!")
            print(f"   Total clientes: {data.get('total_clients', 'N/A')}")
            print(f"   Total leads: {data.get('total_leads', 'N/A')}")
            print(f"   Total conversas: {data.get('total_conversations', 'N/A')}")
            print(f"   Entrevistas ativas: {data.get('active_interviews', 'N/A')}")
        else:
            print(f"   ❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Dashboard stats falhou: {e}")
    
    # Teste 2: Projects
    try:
        response = requests.get(f"{base_url}/api/projects", headers=headers, timeout=5)
        print(f"✅ Projects: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total projetos: {len(data.get('items', []))}")
        else:
            print(f"   ❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Projects falhou: {e}")
    
    # Teste 3: Clients
    try:
        response = requests.get(f"{base_url}/api/clients", headers=headers, timeout=5)
        print(f"✅ Clients: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total clientes: {len(data.get('items', []))}")
        else:
            print(f"   ❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Clients falhou: {e}")

if __name__ == "__main__":
    test_new_token()