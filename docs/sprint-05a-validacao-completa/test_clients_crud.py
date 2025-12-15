"""Teste CRUD de Clients - Sprint 05A"""
import requests
import time

BASE_URL = "http://localhost:8000"
TIMESTAMP = int(time.time())

# Ler token
with open("test_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

print("\n" + "="*60)
print("TESTANDO CRUD DE CLIENTS")
print("="*60)

# 1. CREATE
print("\n1. CREATE (POST /api/clients)")
client_data = {
    "company_name": f"TEST_Cliente_{TIMESTAMP}",
    "cnpj": "12345678000199",
    "segment": "test",  # Workaround: campo obrigatório no banco
    "plan": "basic",
    "status": "active"
}
response = requests.post(f"{BASE_URL}/api/clients", headers=HEADERS, json=client_data)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    client_id = response.json()["id"]
    print(f"   ✅ Cliente criado: {client_id}")
    
    # 2. READ
    print("\n2. READ (GET /api/clients/{id})")
    response = requests.get(f"{BASE_URL}/api/clients/{client_id}", headers=HEADERS)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Cliente encontrado")
    else:
        print(f"   ❌ Erro ao buscar cliente")
    
    # 3. UPDATE
    print("\n3. UPDATE (PUT /api/clients/{id})")
    update_data = {
        "company_name": f"TEST_Cliente_Updated_{TIMESTAMP}",
        "cnpj": "12345678000199",
        "segment": "test_updated",
        "plan": "pro",
        "status": "active"
    }
    response = requests.put(f"{BASE_URL}/api/clients/{client_id}", headers=HEADERS, json=update_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Cliente atualizado")
    else:
        print(f"   ❌ Erro ao atualizar: {response.text[:100]}")
    
    # 4. DELETE
    print("\n4. DELETE (DELETE /api/clients/{id})")
    response = requests.delete(f"{BASE_URL}/api/clients/{client_id}", headers=HEADERS)
    print(f"   Status: {response.status_code}")
    if response.status_code == 204:
        print(f"   ✅ Cliente deletado")
    else:
        print(f"   ❌ Erro ao deletar")
else:
    print(f"   ❌ Erro ao criar cliente: {response.text[:100]}")

print("\n" + "="*60)
print("TESTE CONCLUÍDO")
print("="*60)
