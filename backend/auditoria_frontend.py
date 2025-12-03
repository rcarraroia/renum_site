"""
🎨 AUDITORIA COMPLETA DO FRONTEND
Verifica implementação dos 10 menus principais
"""
from pathlib import Path

GREEN = "✅"
YELLOW = "⚠️"
RED = "❌"

def check_frontend_menus():
    """Verifica os 10 menus principais do frontend"""
    print("\n" + "="*70)
    print("🎨 AUDITORIA DOS 10 MENUS DO FRONTEND")
    print("="*70)

    root = Path("/home/user/renum_site/src/pages")

    # Definir os 10 menus esperados
    menus = {
        "1. Overview (Dashboard)": {
            "files": ["AdminOverview.tsx", "ClientOverview.tsx"],
            "path": "dashboard"
        },
        "2. Clientes": {
            "files": ["AdminClientsPage.tsx"],
            "path": "dashboard"
        },
        "3. Leads": {
            "files": ["AdminLeadsPage.tsx"],
            "path": "dashboard"
        },
        "4. Projetos": {
            "files": ["AdminProjectsPage.tsx"],
            "path": "dashboard"
        },
        "5. Conversas": {
            "files": ["AdminConversationsPage.tsx"],
            "path": "dashboard"
        },
        "6. Pesquisas/Entrevistas": {
            "files": [
                "PesquisasEntrevistasPage.tsx",
                "PesquisasResultadosPage.tsx",
                "PesquisasAnalisePage.tsx"
            ],
            "path": "dashboard"
        },
        "7. Assistente ISA": {
            "files": ["AssistenteIsaPage.tsx"],
            "path": "dashboard"
        },
        "8. Config. Renus": {
            "files": ["RenusConfigPage.tsx"],
            "path": "dashboard"
        },
        "9. Relatórios": {
            "files": ["AdminReportsPage.tsx"],
            "path": "dashboard"
        },
        "10. Configurações": {
            "files": ["AdminSettingsPage.tsx"],
            "path": "dashboard"
        }
    }

    results = {}

    for menu_name, config in menus.items():
        path = root / config["path"]
        files_found = []
        files_missing = []

        for file in config["files"]:
            file_path = path / file
            if file_path.exists():
                files_found.append(file)
            else:
                files_missing.append(file)

        # Status
        if len(files_found) == len(config["files"]):
            status = GREEN
            impl_status = "100%"
        elif len(files_found) > 0:
            percentage = round(len(files_found) / len(config["files"]) * 100)
            status = YELLOW
            impl_status = f"{percentage}%"
        else:
            status = RED
            impl_status = "0%"

        print(f"{status} {menu_name}: {impl_status} implementado")

        if files_found:
            for f in files_found:
                print(f"    ✓ {f}")
        if files_missing:
            for f in files_missing:
                print(f"    ✗ {f} (FALTANDO)")

        results[menu_name] = {
            "status": impl_status,
            "files_found": files_found,
            "files_missing": files_missing
        }

    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO FRONTEND")
    print("="*70)

    fully_implemented = sum(1 for r in results.values() if r["status"] == "100%")
    partially_implemented = sum(1 for r in results.values() if r["status"] not in ["100%", "0%"])
    not_implemented = sum(1 for r in results.values() if r["status"] == "0%")

    print(f"\n✅ Totalmente implementados: {fully_implemented}/10")
    print(f"⚠️  Parcialmente implementados: {partially_implemented}/10")
    print(f"❌ Não implementados: {not_implemented}/10")

    overall = round(fully_implemented / 10 * 100, 1)
    print(f"\n🎯 Status Geral Frontend: {overall}%")

    if overall >= 90:
        print(f"{GREEN} Frontend COMPLETO")
    elif overall >= 70:
        print(f"{YELLOW} Frontend QUASE COMPLETO")
    elif overall >= 50:
        print(f"{YELLOW} Frontend EM DESENVOLVIMENTO")
    else:
        print(f"{RED} Frontend INÍCIO de desenvolvimento")

    return results, overall


def check_components():
    """Verifica componentes principais"""
    print("\n🧩 COMPONENTES PRINCIPAIS")

    components_dir = Path("/home/user/renum_site/src/components")

    if not components_dir.exists():
        print(f"{RED} Pasta de componentes não encontrada")
        return

    # Contar componentes
    components = list(components_dir.glob("**/*.tsx"))
    print(f"{GREEN} Total de componentes: {len(components)}")

    # Componentes importantes
    important = [
        "Layout", "Sidebar", "Header", "Footer",
        "DataTable", "Form", "Chart", "Card"
    ]

    for comp in important:
        found = any(comp.lower() in str(c).lower() for c in components)
        status = GREEN if found else YELLOW
        print(f"{status}   {comp}: {'Encontrado' if found else 'Não encontrado'}")


def check_services():
    """Verifica services/API clients"""
    print("\n🔌 API SERVICES")

    services_dir = Path("/home/user/renum_site/src/services")

    if not services_dir.exists():
        print(f"{RED} Pasta de services não encontrada")
        return

    services = list(services_dir.glob("*.ts")) + list(services_dir.glob("*.tsx"))
    print(f"{GREEN} Total de services: {len(services)}")

    for service in services:
        print(f"{GREEN}   - {service.name}")


if __name__ == "__main__":
    results, overall = check_frontend_menus()
    check_components()
    check_services()

    print("\n" + "="*70)
    print("✅ AUDITORIA FRONTEND CONCLUÍDA")
    print("="*70 + "\n")
