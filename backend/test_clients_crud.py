"""
Script para testar CRUD de clientes
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Ler token
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_list_clients():
    print("🔍 Testando GET /api/clients...\n")
    
    response = requests.get(f"{BASE_URL}/api/clients", headers=HEADERS)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sucesso! {len(data)} cliente(s) encontrado(s)")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_create_client():
    print("\n🔍 Testando POST /api/clients...\n")
    
    client_data = {
        "company_name": "Empresa Teste Auditoria LTDA",
        "document": "12345678000199",
        "segment": "Tecnologia",
        "website": "https://teste.com",
        "contact": {
            "email": "teste@auditoria.com",
            "phone": "11999999999"
        }
        # Removendo status para usar o default
    }
    
    response = requests.post(
        f"{BASE_URL}/api/clients",
        headers=HEADERS,
        json=client_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ Cliente criado!")
        print(f"   ID: {data.get('id')}")
        print(f"   Nome: {data.get('company_name')}")
        return data.get('id')
    else:
        print(f"❌ Erro: {response.text}")
        return None

def test_get_client(client_id):
    print(f"\n🔍 Testando GET /api/clients/{client_id}...\n")
    
    response = requests.get(
        f"{BASE_URL}/api/clients/{client_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Cliente encontrado!")
        print(f"   Nome: {data.get('company_name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_update_client(client_id):
    print(f"\n🔍 Testando PUT /api/clients/{client_id}...\n")
    
    update_data = {
        "company_name": "Empresa Teste Auditoria LTDA - ATUALIZADA"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/clients/{client_id}",
        headers=HEADERS,
        json=update_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Cliente atualizado!")
        print(f"   Nome: {data.get('company_name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_delete_client(client_id):
    print(f"\n🔍 Testando DELETE /api/clients/{client_id}...\n")
    
    response = requests.delete(
        f"{BASE_URL}/api/clients/{client_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 204]:
        print(f"✅ Cliente deletado!")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TESTE COMPLETO DE CRUD - CLIENTES")
    print("="*60)
    
    # 1. Listar
    test_list_clients()
    
    # 2. Criar
    client_id = test_create_client()
    
    if client_id:
        # 3. Buscar
        test_get_client(client_id)
        
        # 4. Atualizar
        test_update_client(client_id)
        
        # 5. Deletar
        test_delete_client(client_id)
    
    print("\n" + "="*60)
    print("TESTE CONCLUÍDO")
    print("="*60)
