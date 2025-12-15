#!/usr/bin/env python3
"""
Testar se o token JWT do frontend funciona com o backend
"""
import requests

def test_auth_token():
    base_url = "http://localhost:8000"
    
    # Token do frontend
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NTE2NzU5LCJpYXQiOjE3NjU0MzAzNTksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Dgavryf5gfGa2fj-FEts2GnzxHBHBO7v7O13mQaI9W0"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Testando token JWT do frontend...")
    
    # Teste 1: Dashboard stats
    try:
        response = requests.get(f"{base_url}/api/dashboard/stats", headers=headers, timeout=5)
        print(f"✅ Dashboard stats com token: {response.status_code}")
        if response.status_code == 200:
            print(f"   Dados: {response.json()}")
        elif response.status_code == 401:
            print("   ❌ Token inválido ou expirado")
        else:
            print(f"   ⚠️  Resposta inesperada: {response.text}")
    except Exception as e:
        print(f"❌ Dashboard stats falhou: {e}")
    
    # Teste 2: Projects
    try:
        response = requests.get(f"{base_url}/api/projects", headers=headers, timeout=5)
        print(f"✅ Projects com token: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total projetos: {len(data.get('items', []))}")
        elif response.status_code == 401:
            print("   ❌ Token inválido ou expirado")
    except Exception as e:
        print(f"❌ Projects falhou: {e}")

if __name__ == "__main__":
    test_auth_token()