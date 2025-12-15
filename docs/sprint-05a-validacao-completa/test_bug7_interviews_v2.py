"""
BUG #7 - Teste do Endpoint POST /api/interviews/start

Versão 2: Usando campos corretos (lead_id, subagent_id)
"""

import requests
import uuid

BASE_URL = "http://localhost:8000"

# Ler token
with open("backend/test_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_interviews_endpoint():
    """Testa endpoint POST /api/interviews/start"""
    
    print("\n" + "=" * 60)
    print("TESTE BUG #7 - INTERVIEWS ENDPOINT (V2)")
    print("=" * 60)
    
    # Setup: Criar lead de teste
    print("\n📋 SETUP: Criando lead de teste...")
    
    # Criar cliente
    client_data = {
        "company_name": f"TEST_Cliente_{uuid.uuid4().hex[:8]}",
        "cnpj": "12345678000199",
        "plan": "basic",
        "status": "active"
    }
    
    client_response = requests.post(
        f"{BASE_URL}/api/clients",
        headers=HEADERS,
        json=client_data,
        timeout=5
    )
    
    if client_response.status_code != 201:
        print(f"   ❌ Erro ao criar cliente: {client_response.status_code}")
        return
    
    client_id = client_response.json()["id"]
    print(f"   ✅ Cliente criado: {client_id}")
    
    # Criar lead
    lead_data = {
        "client_id": client_id,
        "phone": "+5511999999999",
        "name": f"TEST_Lead_{uuid.uuid4().hex[:8]}",
        "status": "active"
    }
    
    lead_response = requests.post(
        f"{BASE_URL}/api/leads",
        headers=HEADERS,
        json=lead_data,
        timeout=5
    )
    
    if lead_response.status_code != 201:
        print(f"   ❌ Erro ao criar lead: {lead_response.status_code}")
        # Cleanup cliente
        requests.delete(f"{BASE_URL}/api/clients/{client_id}", headers=HEADERS)
        return
    
    lead_id = lead_response.json()["id"]
    print(f"   ✅ Lead criado: {lead_id}")
    
    # Teste principal
    print("\n" + "-" * 60)
    print("TESTE PRINCIPAL: POST /api/interviews/start")
    print("-" * 60)
    
    success_count = 0
    total_tests = 2
    
    # 1. POST /api/interviews/start
    print("\n1. POST /api/interviews/start")
    print(f"   Dados: lead_id={lead_id}")
    
    response = requests.post(
        f"{BASE_URL}/api/interviews/start",
        headers=HEADERS,
        json={
            "lead_id": lead_id
        },
        timeout=5
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 201:
        print("   ✅ SUCESSO")
        interview_id = response.json()["id"]
        print(f"   Interview ID: {interview_id}")
        success_count += 1
    else:
        print(f"   ❌ FALHOU - Status {response.status_code}")
        print(f"   Response: {response.text}")
    
    # 2. GET /api/interviews (verificar se aparece)
    print("\n2. GET /api/interviews (verificar se interview foi criada)")
    
    response = requests.get(
        f"{BASE_URL}/api/interviews",
        headers=HEADERS,
        timeout=5
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        interviews = response.json().get("interviews", [])
        found = any(i.get("lead_id") == lead_id for i in interviews)
        
        if found:
            print("   ✅ SUCESSO - Interview encontrada na lista")
            success_count += 1
        else:
            print("   ⚠️ Interview não encontrada na lista")
    else:
        print(f"   ❌ FALHOU - Status {response.status_code}")
    
    # Cleanup
    print("\n" + "-" * 60)
    print("CLEANUP: Removendo dados de teste")
    print("-" * 60)
    
    # Deletar lead
    requests.delete(f"{BASE_URL}/api/leads/{lead_id}", headers=HEADERS)
    print("   ✅ Lead deletado")
    
    # Deletar cliente
    requests.delete(f"{BASE_URL}/api/clients/{client_id}", headers=HEADERS)
    print("   ✅ Cliente deletado")
    
    # Resultado final
    print("\n" + "=" * 60)
    print(f"RESULTADO: {success_count}/{total_tests} ({success_count/total_tests*100:.1f}%)")
    print()
    
    if success_count == total_tests:
        print("✅ BUG #7 CORRIGIDO!")
        print("   Endpoint POST /api/interviews/start funciona")
    elif success_count > 0:
        print("⚠️ BUG #7 PARCIALMENTE CORRIGIDO")
        print("   Alguns testes falharam")
    else:
        print("🔴 BUG #7 NÃO CORRIGIDO!")
    
    print("=" * 60)
    print()

if __name__ == "__main__":
    test_interviews_endpoint()
