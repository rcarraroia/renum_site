"""
🔍 ANÁLISE RÁPIDA - VERSÃO FAST
Testa apenas endpoints críticos sem LLM
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

try:
    with open('test_token.txt', 'r') as f:
        TOKEN = f.read().strip()
    HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
except:
    TOKEN = None
    HEADERS = {"Content-Type": "application/json"}

def test(name, method, url, data=None, expected=200):
    try:
        if method == "GET":
            r = requests.get(url, headers=HEADERS, timeout=3)
        elif method == "POST":
            r = requests.post(url, headers=HEADERS, json=data, timeout=3)
        success = r.status_code == expected
        return {"ok": success, "status": r.status_code, "data": r.json() if r.status_code < 500 else None}
    except Exception as e:
        return {"ok": False, "status": None, "error": str(e)[:50]}

print("\n" + "="*70)
print("🔍 ANÁLISE RÁPIDA DO SISTEMA")
print("="*70)
print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

# BACKEND
print("🔧 BACKEND (APIs Críticas)")
print("-" * 70)

tests = {
    "Auth": test("auth", "GET", f"{BASE_URL}/api/auth/me"),
    "Clients List": test("clients", "GET", f"{BASE_URL}/api/clients"),
    "Leads List": test("leads", "GET", f"{BASE_URL}/api/leads"),
    "Projects List": test("projects", "GET", f"{BASE_URL}/api/projects"),
    "Conversations": test("conv", "GET", f"{BASE_URL}/api/conversations"),
    "Interviews": test("int", "GET", f"{BASE_URL}/api/interviews"),
    "Sub-Agents": test("sub", "GET", f"{BASE_URL}/api/sub-agents"),
    "Dashboard": test("dash", "GET", f"{BASE_URL}/api/dashboard/stats"),
}

for name, result in tests.items():
    status = "✅" if result["ok"] else "❌"
    code = result.get("status", "ERR")
    print(f"  {status} {name}: {code}")
    if name == "Dashboard" and result["ok"] and result["data"]:
        print(f"     Dados: {json.dumps(result['data'], indent=6)[:120]}...")

backend_ok = sum(1 for r in tests.values() if r["ok"])
backend_total = len(tests)
backend_pct = (backend_ok / backend_total * 100)

print(f"\n📊 Backend: {backend_ok}/{backend_total} ({backend_pct:.0f}%)")

# FRONTEND (APIs que alimentam menus)
print(f"\n{'='*70}")
print("🎨 FRONTEND (APIs dos Menus)")
print("-" * 70)

menus = {
    "1. Overview": tests["Dashboard"]["ok"],
    "2. Clientes": tests["Clients List"]["ok"],
    "3. Leads": tests["Leads List"]["ok"],
    "4. Projetos": tests["Projects List"]["ok"],
    "5. Conversas": tests["Conversations"]["ok"],
    "6. Entrevistas": tests["Interviews"]["ok"],
    "7. ISA": False,  # Não testado (timeout)
    "8. Config Renus": tests["Sub-Agents"]["ok"],
    "9. Relatórios": None,  # Não implementado
    "10. Configurações": tests["Auth"]["ok"],
}

for name, ok in menus.items():
    if ok is None:
        print(f"  ⏳ {name}: Não implementado")
    elif ok:
        print(f"  ✅ {name}: API funcional")
    else:
        print(f"  ❌ {name}: API com problema")

frontend_ok = sum(1 for v in menus.values() if v is True)
frontend_total = len([v for v in menus.values() if v is not None])
frontend_pct = (frontend_ok / frontend_total * 100) if frontend_total > 0 else 0

print(f"\n📊 Frontend: {frontend_ok}/{frontend_total} menus com API OK ({frontend_pct:.0f}%)")

# PROBLEMAS ENCONTRADOS
print(f"\n{'='*70}")
print("⚠️ PROBLEMAS ENCONTRADOS")
print("-" * 70)

problems = []
if not tests["Auth"]["ok"]:
    problems.append("❌ Auth: GET /api/auth/me retorna 404 (endpoint não existe?)")
if not tests["Dashboard"]["ok"]:
    problems.append("❌ Dashboard: Métricas não carregam")

if problems:
    for p in problems:
        print(f"  {p}")
else:
    print("  ✅ Nenhum problema crítico encontrado")

# RESUMO FINAL
print(f"\n{'='*70}")
print("🎯 RESUMO FINAL")
print("="*70)

total_ok = backend_ok + frontend_ok
total_tests = backend_total + frontend_total
total_pct = (total_ok / total_tests * 100) if total_tests > 0 else 0

print(f"\n📊 Status Geral: {total_ok}/{total_tests} ({total_pct:.0f}%)")
print(f"  - Backend: {backend_pct:.0f}%")
print(f"  - Frontend: {frontend_pct:.0f}%")

if total_pct >= 90:
    print(f"\n✅ Sistema está PRONTO para continuar desenvolvimento")
    print(f"✅ Pode avançar para próximo sprint")
elif total_pct >= 70:
    print(f"\n⚠️ Sistema PARCIALMENTE funcional")
    print(f"⚠️ Recomenda-se corrigir bugs antes de avançar")
else:
    print(f"\n❌ Sistema com PROBLEMAS GRAVES")
    print(f"❌ Focar em correções antes de novo desenvolvimento")

print(f"\n{'='*70}")
print(f"Análise concluída: {datetime.now().strftime('%H:%M:%S')}")
print("="*70 + "\n")
