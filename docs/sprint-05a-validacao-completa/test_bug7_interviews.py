"""Teste BUG #7 - Interviews Endpoint - FASE 7"""
import requests
import time

BASE_URL = "http://localhost:8000"
TS = int(time.time())

# Ler token
with open("backend/test_token.txt", "r") as f:
    TOKEN = f.read().strip()

H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

print("\n" + "="*60)
print("TESTE BUG #7 - INTERVIEWS ENDPOINT")
print("="*60)

results = {"total": 0, "success": 0}

# SETUP: Criar client, lead e project para teste
print("\n📋 SETUP: Criando dados de teste...")

# 1. Criar cliente
results["total"] += 1
client_data = {
    "company_name": f"TEST_Client_Interview_{TS}",
    "cnpj": "99988877000166",
    "segment": "test",
    "plan": "basic",
    "status": "active"
}
r = requests.post(f"{BASE_URL}/api/clients", headers=H, json=client_data, timeout=10)
if r.status_code == 201:
    client_id = r.json()["id"]
    print(f"   ✅ Cliente criado: {client_id}")
    results["success"] += 1
else:
    print(f"   ❌ Erro ao criar cliente: {r.status_code}")
    exit(1)

# 2. Criar lead
results["total"] += 1
lead_data = {
    "client_id": client_id,
    "name": f"TEST_Lead_Interview_{TS}",
    "phone": "+5511966666666",
    "source": "campanha",
    "status": "novo"
}
r = requests.post(f"{BASE_URL}/api/leads", headers=H, json=lead_data, timeout=10)
if r.status_code == 201:
    lead_id = r.json()["id"]
    print(f"   ✅ Lead criado: {lead_id}")
    results["success"] += 1
else:
    print(f"   ❌ Erro ao criar lead: {r.status_code}")
    exit(1)

# 3. Criar project
results["total"] += 1
project_data = {
    "client_id": client_id,
    "name": f"TEST_Project_Interview_{TS}",
    "description": "Projeto para teste de interviews",
    "type": "Workflow",
    "status": "Em Andamento"
}
r = requests.post(f"{BASE_URL}/api/projects", headers=H, json=project_data, timeout=10)
if r.status_code == 201:
    project_id = r.json()["id"]
    print(f"   ✅ Projeto criado: {project_id}")
    results["success"] += 1
else:
    print(f"   ❌ Erro ao criar projeto: {r.status_code}")
    exit(1)

# TESTE PRINCIPAL: POST /api/interviews/start
print("\n" + "-"*60)
print("TESTE PRINCIPAL: POST /api/interviews/start")
print("-"*60)

results["total"] += 1
interview_data = {
    "lead_id": lead_id,
    "project_id": project_id
}

print(f"\n1. POST /api/interviews/start")
print(f"   Dados: lead_id={lead_id}, project_id={project_id}")

r = requests.post(f"{BASE_URL}/api/interviews/start", headers=H, json=interview_data, timeout=10)
print(f"   Status: {r.status_code}")

if r.status_code == 201:
    interview = r.json()
    interview_id = interview["id"]
    print(f"   ✅ Interview criada: {interview_id}")
    print(f"   Status: {interview.get('status')}")
    print(f"   Lead ID: {interview.get('lead_id')}")
    print(f"   Project ID: {interview.get('project_id')}")
    results["success"] += 1
    
    # TESTE 2: GET /api/interviews/{id}
    results["total"] += 1
    print(f"\n2. GET /api/interviews/{interview_id}")
    r = requests.get(f"{BASE_URL}/api/interviews/{interview_id}", headers=H, timeout=10)
    print(f"   Status: {r.status_code}")
    
    if r.status_code == 200:
        print(f"   ✅ Interview encontrada")
        results["success"] += 1
    else:
        print(f"   ❌ Erro ao buscar interview")
        print(f"   Response: {r.text[:100]}")
    
else:
    print(f"   ❌ FALHOU - Status {r.status_code}")
    print(f"   Response: {r.text[:200]}")
    print(f"\n🔴 BUG #7 NÃO CORRIGIDO!")

# CLEANUP
print("\n" + "-"*60)
print("CLEANUP: Removendo dados de teste")
print("-"*60)

requests.delete(f"{BASE_URL}/api/projects/{project_id}", headers=H, timeout=10)
print(f"   ✅ Projeto deletado")

requests.delete(f"{BASE_URL}/api/leads/{lead_id}", headers=H, timeout=10)
print(f"   ✅ Lead deletado")

requests.delete(f"{BASE_URL}/api/clients/{client_id}", headers=H, timeout=10)
print(f"   ✅ Cliente deletado")

# RESULTADO
print("\n" + "="*60)
pct = (results["success"] / results["total"] * 100) if results["total"] > 0 else 0
print(f"RESULTADO: {results['success']}/{results['total']} ({pct:.1f}%)")

if pct == 100:
    print("\n✅ BUG #7 CORRIGIDO COM SUCESSO!")
    print("   Endpoint POST /api/interviews/start funcionando")
elif pct >= 60:
    print("\n⚠️ BUG #7 PARCIALMENTE CORRIGIDO")
    print("   Alguns testes falharam")
else:
    print("\n❌ BUG #7 NÃO CORRIGIDO")
    print("   Endpoint ainda não funciona")

print("="*60)
