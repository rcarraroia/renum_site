"""
Script para testar CRUD de leads
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

def test_list_leads():
    print("🔍 Testando GET /api/leads...\n")
    
    response = requests.get(f"{BASE_URL}/api/leads", headers=HEADERS)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sucesso!")
        print(f"   Total: {data.get('total', 0)}")
        print(f"   Items: {len(data.get('items', []))}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_create_lead():
    print("\n🔍 Testando POST /api/leads...\n")
    
    lead_data = {
        "name": "João Silva Teste",
        "phone": "+5511999999999",
        "email": "joao.teste@email.com",
        "source": "home"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/leads",
        headers=HEADERS,
        json=lead_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ Lead criado!")
        print(f"   ID: {data.get('id')}")
        print(f"   Nome: {data.get('name')}")
        return data.get('id')
    else:
        print(f"❌ Erro: {response.text}")
        return None

def test_get_lead(lead_id):
    print(f"\n🔍 Testando GET /api/leads/{lead_id}...\n")
    
    response = requests.get(
        f"{BASE_URL}/api/leads/{lead_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Lead encontrado!")
        print(f"   Nome: {data.get('name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_update_lead(lead_id):
    print(f"\n🔍 Testando PUT /api/leads/{lead_id}...\n")
    
    update_data = {
        "name": "João Silva Teste - ATUALIZADO"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/leads/{lead_id}",
        headers=HEADERS,
        json=update_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Lead atualizado!")
        print(f"   Nome: {data.get('name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_delete_lead(lead_id):
    print(f"\n🔍 Testando DELETE /api/leads/{lead_id}...\n")
    
    response = requests.delete(
        f"{BASE_URL}/api/leads/{lead_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 204]:
        print(f"✅ Lead deletado!")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TESTE COMPLETO DE CRUD - LEADS")
    print("="*60)
    
    results = {
        "list": False,
        "create": False,
        "get": False,
        "update": False,
        "delete": False
    }
    
    # 1. Listar
    results["list"] = test_list_leads()
    
    # 2. Criar
    lead_id = test_create_lead()
    if lead_id:
        results["create"] = True
        
        # 3. Buscar
        results["get"] = test_get_lead(lead_id)
        
        # 4. Atualizar
        results["update"] = test_update_lead(lead_id)
        
        # 5. Deletar
        results["delete"] = test_delete_lead(lead_id)
    
    print("\n" + "="*60)
    print("RESUMO - LEADS")
    print("="*60)
    for operation, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {operation.upper()}")
    print("="*60)
