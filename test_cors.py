#!/usr/bin/env python3
"""
Testar se CORS está funcionando para porta 8083
"""
import requests

def test_cors():
    base_url = "http://localhost:8000"
    
    # Token do frontend
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NTE2NzU5LCJpYXQiOjE3NjU0MzAzNTksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Dgavryf5gfGa2fj-FEts2GnzxHBHBO7v7O13mQaI9W0"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:8083"  # Simular requisição do frontend na porta 8083
    }
    
    print("🔍 Testando CORS para porta 8083...")
    
    # Teste OPTIONS (preflight)
    try:
        response = requests.options(f"{base_url}/api/dashboard/stats", headers=headers, timeout=5)
        print(f"✅ OPTIONS request: {response.status_code}")
        print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
        print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
    except Exception as e:
        print(f"❌ OPTIONS request falhou: {e}")
    
    # Teste GET real
    try:
        response = requests.get(f"{base_url}/api/dashboard/stats", headers=headers, timeout=5)
        print(f"✅ GET request: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dados carregados com sucesso!")
            data = response.json()
            print(f"   Total clientes: {data.get('total_clients', 'N/A')}")
        else:
            print(f"   ⚠️  Resposta: {response.text}")
    except Exception as e:
        print(f"❌ GET request falhou: {e}")

if __name__ == "__main__":
    test_cors()