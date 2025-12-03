"""
Script para testar endpoints de sub-agents
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

def test_list_subagents():
    print("🔍 Testando GET /api/sub-agents...\n")
    
    response = requests.get(f"{BASE_URL}/api/sub-agents", headers=HEADERS)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sucesso!")
        print(f"   Total: {len(data)}")
        if data:
            print(f"\n   Primeiro sub-agent:")
            print(f"   ID: {data[0].get('id')}")
            print(f"   Nome: {data[0].get('name')}")
            print(f"   Slug: {data[0].get('slug')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_create_subagent():
    print("\n🔍 Testando POST /api/sub-agents...\n")
    
    subagent_data = {
        "name": "Agente Teste Auditoria",
        "slug": "agente-teste-auditoria",
        "description": "Sub-agente criado durante auditoria",
        "channel": "web",
        "ai_model": "gpt-4",
        "system_prompt": "Você é um assistente de teste",
        "is_active": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/sub-agents",
        headers=HEADERS,
        json=subagent_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"✅ Sub-agent criado!")
        print(f"   ID: {data.get('id')}")
        print(f"   Nome: {data.get('name')}")
        return data.get('id')
    else:
        print(f"❌ Erro: {response.text}")
        return None

def test_get_subagent(subagent_id):
    print(f"\n🔍 Testando GET /api/sub-agents/{subagent_id}...\n")
    
    response = requests.get(
        f"{BASE_URL}/api/sub-agents/{subagent_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sub-agent encontrado!")
        print(f"   Nome: {data.get('name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_update_subagent(subagent_id):
    print(f"\n🔍 Testando PUT /api/sub-agents/{subagent_id}...\n")
    
    update_data = {
        "name": "Agente Teste Auditoria - ATUALIZADO"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/sub-agents/{subagent_id}",
        headers=HEADERS,
        json=update_data
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sub-agent atualizado!")
        print(f"   Nome: {data.get('name')}")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

def test_delete_subagent(subagent_id):
    print(f"\n🔍 Testando DELETE /api/sub-agents/{subagent_id}...\n")
    
    response = requests.delete(
        f"{BASE_URL}/api/sub-agents/{subagent_id}",
        headers=HEADERS
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code in [200, 204]:
        print(f"✅ Sub-agent deletado!")
        return True
    else:
        print(f"❌ Erro: {response.text}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TESTE COMPLETO - SUB-AGENTS")
    print("="*60)
    
    results = {
        "list": False,
        "create": False,
        "get": False,
        "update": False,
        "delete": False
    }
    
    results["list"] = test_list_subagents()
    
    subagent_id = test_create_subagent()
    if subagent_id:
        results["create"] = True
        results["get"] = test_get_subagent(subagent_id)
        results["update"] = test_update_subagent(subagent_id)
        results["delete"] = test_delete_subagent(subagent_id)
    
    print("\n" + "="*60)
    print("RESUMO - SUB-AGENTS")
    print("="*60)
    for operation, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {operation.upper()}")
    print("="*60)
