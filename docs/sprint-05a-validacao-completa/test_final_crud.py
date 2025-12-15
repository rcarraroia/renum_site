"""Teste CRUD FINAL - Sprint 05A - Com valores corretos"""
import requests
import time

BASE_URL = "http://localhost:8000"
TS = int(time.time())

with open("test_token.txt", "r") as f:
    TOKEN = f.read().strip()

H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

print("\n" + "="*60)
print("VALIDAÇÃO CRUD FINAL - FASE 2")
print("="*60)

# Contadores
total = success = 0

def t(name, method, url, data=None, exp=200):
    global total, success
    total += 1
    try:
        r = getattr(requests, method.lower())(url, headers=H, json=data, timeout=10) if data else getattr(requests, method.lower())(url, headers=H, timeout=10)
        if r.status_code == exp:
            success += 1
            print(f"✅ {name}")
            return r.json() if r.text else {}
        print(f"❌ {name} ({r.status_code})")
        return None
    except Exception as e:
        print(f"❌ {name} (erro: {str(e)[:40]})")
        return None

# CLIENTS
print("\n1️⃣ CLIENTS (4 testes)")
c = t("POST client", "POST", f"{BASE_URL}/api/clients", {"company_name": f"TEST_C_{TS}", "cnpj": "12345678000199", "segment": "test", "plan": "basic", "status": "active"}, 201)
if c:
    t("GET client", "GET", f"{BASE_URL}/api/clients/{c['id']}")
    t("PUT client", "PUT", f"{BASE_URL}/api/clients/{c['id']}", {**c, "plan": "pro"})
    t("DELETE client", "DELETE", f"{BASE_URL}/api/clients/{c['id']}", exp=204)

# LEADS
print("\n2️⃣ LEADS (4 testes)")
c = t("POST client", "POST", f"{BASE_URL}/api/clients", {"company_name": f"TEST_C2_{TS}", "cnpj": "98765432000188", "segment": "test", "plan": "basic", "status": "active"}, 201)
if c:
    l = t("POST lead", "POST", f"{BASE_URL}/api/leads", {"client_id": c["id"], "name": f"TEST_L_{TS}", "phone": "+5511999999999", "source": "pesquisa", "status": "novo"}, 201)
    if l:
        t("GET lead", "GET", f"{BASE_URL}/api/leads/{l['id']}")
        t("PUT lead", "PUT", f"{BASE_URL}/api/leads/{l['id']}", {**l, "status": "qualificado"})
        t("DELETE lead", "DELETE", f"{BASE_URL}/api/leads/{l['id']}", exp=204)
    t("DELETE client", "DELETE", f"{BASE_URL}/api/clients/{c['id']}", exp=204)

# PROJECTS
print("\n3️⃣ PROJECTS (4 testes)")
c = t("POST client", "POST", f"{BASE_URL}/api/clients", {"company_name": f"TEST_C3_{TS}", "cnpj": "11122233000144", "segment": "test", "plan": "basic", "status": "active"}, 201)
if c:
    p = t("POST project", "POST", f"{BASE_URL}/api/projects", {"client_id": c["id"], "name": f"TEST_P_{TS}", "description": "Test", "type": "AI Native", "status": "Em Andamento"}, 201)
    if p:
        t("GET project", "GET", f"{BASE_URL}/api/projects/{p['id']}")
        t("PUT project", "PUT", f"{BASE_URL}/api/projects/{p['id']}", {**p, "status": "Pausado"})
        t("DELETE project", "DELETE", f"{BASE_URL}/api/projects/{p['id']}", exp=204)
    t("DELETE client", "DELETE", f"{BASE_URL}/api/clients/{c['id']}", exp=204)

# CONVERSATIONS
print("\n4️⃣ CONVERSATIONS (4 testes)")
c = t("POST client", "POST", f"{BASE_URL}/api/clients", {"company_name": f"TEST_C4_{TS}", "cnpj": "55566677000133", "segment": "test", "plan": "basic", "status": "active"}, 201)
if c:
    l = t("POST lead", "POST", f"{BASE_URL}/api/leads", {"client_id": c["id"], "name": f"TEST_L2_{TS}", "phone": "+5511977777777", "source": "home", "status": "novo"}, 201)
    if l:
        cv = t("POST conversation", "POST", f"{BASE_URL}/api/conversations", {"lead_id": l["id"], "client_id": c["id"], "status": "open"}, 201)
        if cv:
            t("GET conversation", "GET", f"{BASE_URL}/api/conversations/{cv['id']}")
            t("POST message", "POST", f"{BASE_URL}/api/conversations/{cv['id']}/messages", {"content": f"TEST_MSG_{TS}", "role": "user"}, 201)
            t("GET messages", "GET", f"{BASE_URL}/api/conversations/{cv['id']}/messages")
        t("DELETE lead", "DELETE", f"{BASE_URL}/api/leads/{l['id']}", exp=204)
    t("DELETE client", "DELETE", f"{BASE_URL}/api/clients/{c['id']}", exp=204)

# INTERVIEWS
print("\n5️⃣ INTERVIEWS (2 testes)")
c = t("POST client", "POST", f"{BASE_URL}/api/clients", {"company_name": f"TEST_C5_{TS}", "cnpj": "99988877000166", "segment": "test", "plan": "basic", "status": "active"}, 201)
if c:
    l = t("POST lead", "POST", f"{BASE_URL}/api/leads", {"client_id": c["id"], "name": f"TEST_L3_{TS}", "phone": "+5511966666666", "source": "campanha", "status": "novo"}, 201)
    if l:
        p = t("POST project", "POST", f"{BASE_URL}/api/projects", {"client_id": c["id"], "name": f"TEST_P2_{TS}", "description": "Test", "type": "Workflow", "status": "Em Andamento"}, 201)
        if p:
            i = t("POST interview", "POST", f"{BASE_URL}/api/interviews/start", {"lead_id": l["id"], "project_id": p["id"]}, 201)
            if i:
                t("GET interview", "GET", f"{BASE_URL}/api/interviews/{i['id']}")
            t("DELETE project", "DELETE", f"{BASE_URL}/api/projects/{p['id']}", exp=204)
        t("DELETE lead", "DELETE", f"{BASE_URL}/api/leads/{l['id']}", exp=204)
    t("DELETE client", "DELETE", f"{BASE_URL}/api/clients/{c['id']}", exp=204)

# RESUMO
print("\n" + "="*60)
pct = (success / total * 100) if total > 0 else 0
print(f"RESULTADO: {success}/{total} ({pct:.1f}%)")
if pct == 100:
    print("✅ CRUD 100% FUNCIONAL")
elif pct >= 80:
    print("⚠️ CRUD PARCIALMENTE FUNCIONAL")
else:
    print("❌ CRUD COM PROBLEMAS")
print("="*60)
