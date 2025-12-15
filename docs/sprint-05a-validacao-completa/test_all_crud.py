"""Teste CRUD consolidado - Sprint 05A"""
import requests
import time

BASE_URL = "http://localhost:8000"
TIMESTAMP = int(time.time())

with open("test_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

results = {"total": 0, "success": 0, "failed": 0}

def test(name, method, url, data=None, expected=200):
    """Testa endpoint e registra resultado"""
    results["total"] += 1
    try:
        if method == "GET":
            r = requests.get(url, headers=HEADERS, timeout=5)
        elif method == "POST":
            r = requests.post(url, headers=HEADERS, json=data, timeout=5)
        elif method == "PUT":
            r = requests.put(url, headers=HEADERS, json=data, timeout=5)
        elif method == "DELETE":
            r = requests.delete(url, headers=HEADERS, timeout=5)
        
        if r.status_code == expected:
            results["success"] += 1
            print(f"✅ {name}")
            return r.json() if r.text else None
        else:
            results["failed"] += 1
            print(f"❌ {name} - Status {r.status_code}: {r.text[:80]}")
            return None
    except Exception as e:
        results["failed"] += 1
        print(f"❌ {name} - Erro: {str(e)[:80]}")
        return None

print("\n" + "="*60)
print("TESTE CRUD CONSOLIDADO - TODAS ENTIDADES")
print("="*60)

# PROJECTS
print("\n📁 PROJECTS")
client_data = {"company_name": f"TEST_Client_Projects_{TIMESTAMP}", "cnpj": "11122233000144", "segment": "test", "plan": "basic", "status": "active"}
client = test("Criar cliente", "POST", f"{BASE_URL}/api/clients", client_data, 201)
if client:
    project_data = {"client_id": client["id"], "name": f"TEST_Project_{TIMESTAMP}", "description": "Test", "type": "survey", "status": "active"}
    project = test("Criar projeto", "POST", f"{BASE_URL}/api/projects", project_data, 201)
    if project:
        test("Buscar projeto", "GET", f"{BASE_URL}/api/projects/{project['id']}", expected=200)
        update_data = {**project_data, "name": f"TEST_Project_Updated_{TIMESTAMP}", "status": "paused"}
        test("Atualizar projeto", "PUT", f"{BASE_URL}/api/projects/{project['id']}", update_data, 200)
        test("Deletar projeto", "DELETE", f"{BASE_URL}/api/projects/{project['id']}", expected=204)
    test("Deletar cliente", "DELETE", f"{BASE_URL}/api/clients/{client['id']}", expected=204)

# CONVERSATIONS
print("\n💬 CONVERSATIONS")
client_data = {"company_name": f"TEST_Client_Conv_{TIMESTAMP}", "cnpj": "55566677000133", "segment": "test", "plan": "basic", "status": "active"}
client = test("Criar cliente", "POST", f"{BASE_URL}/api/clients", client_data, 201)
if client:
    lead_data = {"client_id": client["id"], "name": f"TEST_Lead_{TIMESTAMP}", "phone": "+5511977777777", "source": "pesquisa", "status": "novo"}
    lead = test("Criar lead", "POST", f"{BASE_URL}/api/leads", lead_data, 201)
    if lead:
        conv_data = {"lead_id": lead["id"], "client_id": client["id"], "status": "open"}
        conv = test("Criar conversa", "POST", f"{BASE_URL}/api/conversations", conv_data, 201)
        if conv:
            test("Buscar conversa", "GET", f"{BASE_URL}/api/conversations/{conv['id']}", expected=200)
            msg_data = {"content": f"TEST_Message_{TIMESTAMP}", "role": "user"}
            test("Enviar mensagem", "POST", f"{BASE_URL}/api/conversations/{conv['id']}/messages", msg_data, 201)
            test("Listar mensagens", "GET", f"{BASE_URL}/api/conversations/{conv['id']}/messages", expected=200)
        test("Deletar lead", "DELETE", f"{BASE_URL}/api/leads/{lead['id']}", expected=204)
    test("Deletar cliente", "DELETE", f"{BASE_URL}/api/clients/{client['id']}", expected=204)

# INTERVIEWS
print("\n📋 INTERVIEWS")
client_data = {"company_name": f"TEST_Client_Interview_{TIMESTAMP}", "cnpj": "99988877000166", "segment": "test", "plan": "basic", "status": "active"}
client = test("Criar cliente", "POST", f"{BASE_URL}/api/clients", client_data, 201)
if client:
    lead_data = {"client_id": client["id"], "name": f"TEST_Lead_{TIMESTAMP}", "phone": "+5511966666666", "source": "pesquisa", "status": "novo"}
    lead = test("Criar lead", "POST", f"{BASE_URL}/api/leads", lead_data, 201)
    if lead:
        project_data = {"client_id": client["id"], "name": f"TEST_Project_{TIMESTAMP}", "description": "Test", "type": "survey", "status": "active"}
        project = test("Criar projeto", "POST", f"{BASE_URL}/api/projects", project_data, 201)
        if project:
            interview_data = {"lead_id": lead["id"], "project_id": project["id"]}
            interview = test("Iniciar entrevista", "POST", f"{BASE_URL}/api/interviews/start", interview_data, 201)
            if interview:
                test("Buscar entrevista", "GET", f"{BASE_URL}/api/interviews/{interview['id']}", expected=200)
            test("Deletar projeto", "DELETE", f"{BASE_URL}/api/projects/{project['id']}", expected=204)
        test("Deletar lead", "DELETE", f"{BASE_URL}/api/leads/{lead['id']}", expected=204)
    test("Deletar cliente", "DELETE", f"{BASE_URL}/api/clients/{client['id']}", expected=204)

# RESUMO
print("\n" + "="*60)
print("RESUMO")
print("="*60)
percentage = (results["success"] / results["total"] * 100) if results["total"] > 0 else 0
print(f"Total: {results['total']} testes")
print(f"Sucesso: {results['success']} ({percentage:.1f}%)")
print(f"Falhas: {results['failed']}")
if percentage == 100:
    print("\n✅ CRUD 100% FUNCIONAL")
elif percentage >= 80:
    print("\n⚠️ CRUD PARCIALMENTE FUNCIONAL")
else:
    print("\n❌ CRUD COM PROBLEMAS")
print("="*60)
