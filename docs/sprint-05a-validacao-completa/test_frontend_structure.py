"""Validação estrutura Frontend - Sprint 05A - Fase 5"""
import os
import json

print("\n" + "="*60)
print("FASE 5 - VALIDAÇÃO FRONTEND (Estrutura)")
print("="*60)

results = {"total": 0, "success": 0}

# Frontend está na raiz do projeto (src/)
frontend_path = ".."

if not os.path.exists(os.path.join(frontend_path, "src")):
    print("\n❌ Diretório src (frontend) não encontrado!")
    print("="*60)
    exit(1)

print(f"\n📁 Frontend encontrado em: {frontend_path}/src")

# TESTE 1-10: Verificar páginas dos 10 menus
menus = [
    ("1. Overview (Dashboard)", "src/pages/dashboard", ["Dashboard", "Overview"]),
    ("2. Clientes", "src/pages/clients", ["Clients", "Client"]),
    ("3. Leads", "src/pages/leads", ["Leads", "Lead"]),
    ("4. Projetos", "src/pages/projects", ["Projects", "Project"]),
    ("5. Conversas", "src/pages/conversations", ["Conversations", "Conversation"]),
    ("6. Entrevistas", "src/pages/interviews", ["Interviews", "Interview"]),
    ("7. ISA", "src/pages/isa", ["ISA", "Isa", "Assistant"]),
    ("8. Config Renus", "src/pages/renus-config", ["Renus", "Config"]),
    ("9. Relatórios", "src/pages/reports", ["Reports", "Report"]),
    ("10. Configurações", "src/pages/settings", ["Settings", "Setting"])
]

print("\n" + "-"*60)
print("VERIFICANDO PÁGINAS DOS 10 MENUS")
print("-"*60)

for menu_name, path_hint, keywords in menus:
    results["total"] += 1
    print(f"\n{menu_name}")
    
    found = False
    # Procurar arquivos relacionados
    for root, dirs, files in os.walk(os.path.join(frontend_path, "src")):
        for file in files:
            if file.endswith((".tsx", ".ts", ".jsx", ".js")):
                file_lower = file.lower()
                if any(kw.lower() in file_lower for kw in keywords):
                    print(f"   ✅ Encontrado: {os.path.join(root, file).replace(frontend_path, '')}")
                    found = True
                    results["success"] += 1
                    break
        if found:
            break
    
    if not found:
        print(f"   ❌ Não encontrado (procurado: {keywords})")

# TESTE 11: Verificar package.json
results["total"] += 1
print("\n" + "-"*60)
print("VERIFICANDO DEPENDÊNCIAS")
print("-"*60)
package_json = os.path.join(frontend_path, "package.json")
if os.path.exists(package_json):
    with open(package_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        deps = list(data.get("dependencies", {}).keys())
        print(f"   ✅ {len(deps)} dependências encontradas")
        print(f"   React: {'react' in deps}")
        print(f"   Router: {'react-router-dom' in deps}")
        results["success"] += 1
else:
    print("   ❌ package.json não encontrado")

# TESTE 12: Verificar build
results["total"] += 1
print("\n" + "-"*60)
print("VERIFICANDO CONFIGURAÇÃO DE BUILD")
print("-"*60)
vite_config = os.path.join(frontend_path, "vite.config.ts")
if os.path.exists(vite_config):
    print("   ✅ vite.config.ts encontrado")
    results["success"] += 1
else:
    print("   ❌ vite.config.ts não encontrado")

# Resumo
print("\n" + "="*60)
pct = (results["success"] / results["total"] * 100) if results["total"] > 0 else 0
print(f"RESULTADO: {results['success']}/{results['total']} ({pct:.1f}%)")

if pct >= 80:
    print("✅ FRONTEND BEM ESTRUTURADO")
elif pct >= 60:
    print("⚠️ FRONTEND PARCIALMENTE ESTRUTURADO")
else:
    print("❌ FRONTEND MAL ESTRUTURADO")

print("\nℹ️ NOTA: Teste funcional (navegador) necessário para validação completa")
print("="*60)
