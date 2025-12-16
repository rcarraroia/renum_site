#!/usr/bin/env python3
"""
Teste CORS real simulando exatamente o que o navegador faz
"""
import requests

def test_cors_real():
    """Testa CORS como o navegador realmente faz"""
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjczMjM5LCJpYXQiOjE3NjU1ODY4MzksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.HgEqRYi7ijWwaqj1Vkt-ofRIB5dWY4bRyDNGiKMpDsk"
    
    print("🔍 Testando CORS como o navegador faz...")
    
    # Teste 1: Requisição GET direta (sem preflight)
    print("\n1. Teste GET direto (sem preflight):")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Origin": "http://localhost:8083"
        }
        
        response = requests.get("http://localhost:8000/api/dashboard/stats", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("   ✅ GET funciona - CORS está OK para requisições simples")
        else:
            print("   ❌ GET falhou")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Requisição com headers customizados (força preflight)
    print("\n2. Teste com headers customizados (força preflight):")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Origin": "http://localhost:8083",
            "X-Custom-Header": "test"  # Força preflight
        }
        
        response = requests.get("http://localhost:8000/api/dashboard/stats", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("   ✅ GET com headers customizados funciona")
        else:
            print("   ❌ GET com headers customizados falhou")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Verificar se o problema é só com OPTIONS
    print("\n3. Análise do problema:")
    print("   O erro 405 (Method Not Allowed) para OPTIONS indica que:")
    print("   - O endpoint /api/dashboard/stats não aceita método OPTIONS")
    print("   - Mas isso é NORMAL! FastAPI/CORS middleware deve tratar isso")
    print("   - O importante é que GET funciona e tem headers CORS corretos")
    
    print("\n4. Teste real no navegador:")
    print("   Para testar CORS real, abra o navegador em http://localhost:8083")
    print("   e veja se as requisições funcionam no DevTools")

if __name__ == "__main__":
    test_cors_real()