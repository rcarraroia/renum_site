"""Teste CRUD de Leads - Sprint 05A"""
import requests
import time

BASE_URL = "http://localhost:8000"
TIMESTAMP = int(time.time())

with open("test_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

print("\n" + "="*60)
print("TESTANDO CRUD DE LEADS")
print("="*60)

# Criar cliente temporário
print("\n0. Criando cliente temporário...")
client_data = {
    "company_name": f"TEST_Cliente_For_Leads_{TIMESTAMP}",
    "cnpj": "98765432000188",
    "segment": "test",
    "plan": "basic",
    "status": "active"
}
response = requests.post(f"{BASE_URL}/api/clients", headers=HEADERS, json=client_data)
if response.status_code != 201:
    print(f"   ❌ Erro ao criar cliente: {response.text[:100]}")
    exit(1)

client_id = response.json()["id"]
print(f"   ✅ Cliente criado: {client_id}")

# 1. CREATE
print("\n1. CREATE (POST /api/leads)")
lead_data = {
    "client_id": client_id,
    "name": f"TEST_Lead_{TIMESTAMP}",
    "phone": "+5511999999999",
    "email": f"test_lead_{TIMESTAMP}@example.com",
    "source": "pesquisa",  # Valores válidos: pesquisa, home, campanha, indicacao
    "status": "novo"  # Valores válidos: novo, qualificado, em_negociacao, perdido
}
response = requests.post(f"{BASE_URL}/api/leads", headers=HEADERS, json=lead_data)
print(f"   Status: {response.status_code}")
if response.status_code != 201:
    print(f"   Erro completo: {response.text}")
if response.status_code == 201:
    lead_id = response.json()["id"]
    print(f"   ✅ Lead criado: {lead_id}")
    
    # 2. READ
    print("\n2. READ (GET /api/leads/{id})")
    response = requests.get(f"{BASE_URL}/api/leads/{lead_id}", headers=HEADERS)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Lead encontrado")
    else:
        print(f"   ❌ Erro ao buscar lead")
    
    # 3. UPDATE
    print("\n3. UPDATE (PUT /api/leads/{id})")
    update_data = {
        "client_id": client_id,
        "name": f"TEST_Lead_Updated_{TIMESTAMP}",
        "phone": "+5511988888888",
        "email": f"test_lead_updated_{TIMESTAMP}@example.com",
        "source": "indicacao",
        "status": "qualificado"
    }
    response = requests.put(f"{BASE_URL}/api/leads/{lead_id}", headers=HEADERS, json=update_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Lead atualizado")
    else:
        print(f"   ❌ Erro ao atualizar: {response.text[:100]}")
    
    # 4. DELETE
    print("\n4. DELETE (DELETE /api/leads/{id})")
    response = requests.delete(f"{BASE_URL}/api/leads/{lead_id}", headers=HEADERS)
    print(f"   Status: {response.status_code}")
    if response.status_code == 204:
        print(f"   ✅ Lead deletado")
    else:
        print(f"   ❌ Erro ao deletar")
else:
    print(f"   ❌ Erro ao criar lead: {response.text[:100]}")

# Cleanup: deletar cliente
print("\n5. Cleanup: deletando cliente temporário...")
response = requests.delete(f"{BASE_URL}/api/clients/{client_id}", headers=HEADERS)
if response.status_code == 204:
    print(f"   ✅ Cliente deletado")

print("\n" + "="*60)
print("TESTE CONCLUÍDO")
print("="*60)
