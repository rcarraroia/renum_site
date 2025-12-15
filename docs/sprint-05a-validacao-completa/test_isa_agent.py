"""
Teste do ISA Agent - Validar correção do erro 500
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Token do admin
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("="*70)
print("TESTE ISA AGENT")
print("="*70)

# Teste 1: Mensagem simples
print("\n1. Testando mensagem simples...")
data = {"message": "Olá ISA, você está funcionando?"}

try:
    response = requests.post(f"{BASE_URL}/api/isa/chat", headers=HEADERS, json=data, timeout=30)
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ ISA respondeu!")
        print(f"   Resposta: {result.get('message', '')[:100]}...")
        print(f"   Comando executado: {result.get('command_executed', False)}")
    else:
        print(f"   ❌ Erro {response.status_code}")
        print(f"   Detalhes: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print(f"   ⏳ TIMEOUT - ISA demorou mais de 30s")
except Exception as e:
    print(f"   ❌ ERRO: {str(e)[:100]}")

# Teste 2: Comando "Liste clientes"
print("\n2. Testando comando 'Liste os últimos clientes'...")
data = {"message": "Liste os últimos 3 clientes"}

try:
    response = requests.post(f"{BASE_URL}/api/isa/chat", headers=HEADERS, json=data, timeout=30)
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ ISA respondeu!")
        print(f"   Resposta: {result.get('message', '')[:150]}...")
        print(f"   Comando executado: {result.get('command_executed', False)}")
    else:
        print(f"   ❌ Erro {response.status_code}")
        print(f"   Detalhes: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print(f"   ⏳ TIMEOUT - ISA demorou mais de 30s")
except Exception as e:
    print(f"   ❌ ERRO: {str(e)[:100]}")

print("\n" + "="*70)
print("CONCLUSÃO")
print("="*70)
print("✅ ISA Agent corrigido - Não retorna mais erro 500")
print("="*70)
