"""
Debug do login - testar diretamente
"""
import httpx
import json

BASE_URL = "http://localhost:8000"

# Teste 1: Login direto via API
print("🔍 Testando login via API FastAPI...")
print()

login_data = {
    "email": "kiro.auditoria@renum.com",
    "password": "kiro123"
}

try:
    response = httpx.post(
        f"{BASE_URL}/auth/login",
        json=login_data,
        timeout=10.0
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("✅ LOGIN SUCESSO!")
        print(f"Token: {data.get('access_token', 'N/A')[:50]}...")
        print(f"User: {data.get('user', {})}")
    else:
        print("❌ LOGIN FALHOU")
        print(f"Erro: {response.text}")
        
except Exception as e:
    print(f"❌ ERRO: {str(e)}")
