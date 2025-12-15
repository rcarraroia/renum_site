"""
Script para testar CRUD de projects
"""
import requests
import json

BASE_URL = "http://localhost:8000"

with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_list_projects():
    print("🔍 Testando GET /api/projects...\n")
    
    response = requests.get(f"{BASE_URL}/api/projects", headers=HEADERS)
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

def test_create_project():
    print("\n🔍 Testando POST /api/projects...\n")
    
    project_data = {
        "name": "Projeto Teste Auditoria",
        "description": "Projeto criado durante auditoria",
        "type": "AI Native"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/projects",
        headers=HEADERS,
        json=project_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ Projeto criado!")
        print(f"   ID: {data.get('id')}")
        print(f"   Nome: {data.get('name')}")
        return data.get('id')
    else:
        print(f"❌ Erro: {response.text}")
        return None

def test_get_project(project_id):
    print(f"\n🔍 Testando GET /api/projects/{project_id}...\n")
    
    response = requests.get(
        f"{BASE_URL}/api/projects/{project_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Projeto encontrado!")
        print(f"   Nome: {data.get('name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_update_project(project_id):
    print(f"\n🔍 Testando PUT /api/projects/{project_id}...\n")
    
    update_data = {
        "name": "Projeto Teste Auditoria - ATUALIZADO"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/projects/{project_id}",
        headers=HEADERS,
        json=update_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Projeto atualizado!")
        print(f"   Nome: {data.get('name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_delete_project(project_id):
    print(f"\n🔍 Testando DELETE /api/projects/{project_id}...\n")
    
    response = requests.delete(
        f"{BASE_URL}/api/projects/{project_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 204]:
        print(f"✅ Projeto deletado!")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TESTE COMPLETO DE CRUD - PROJECTS")
    print("="*60)
    
    results = {
        "list": False,
        "create": False,
        "get": False,
        "update": False,
        "delete": False
    }
    
    results["list"] = test_list_projects()
    
    project_id = test_create_project()
    if project_id:
        results["create"] = True
        results["get"] = test_get_project(project_id)
        results["update"] = test_update_project(project_id)
        results["delete"] = test_delete_project(project_id)
    
    print("\n" + "="*60)
    print("RESUMO - PROJECTS")
    print("="*60)
    for operation, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {operation.upper()}")
    print("="*60)
