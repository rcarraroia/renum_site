"""
🔍 AUDITORIA DO SISTEMA RENUM - ANÁLISE DE CÓDIGO-FONTE
Analisa implementação de rotas, modelos, services, agentes e frontend
"""
import os
import json
from datetime import datetime
from pathlib import Path

GREEN = "✅"
YELLOW = "⚠️"
RED = "❌"
PARTIAL = "⏹️"

class CodeAuditor:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "backend": {},
            "frontend": {},
            "agents": {},
            "integrations": {},
            "summary": {}
        }
        self.root = Path("/home/user/renum_site")

    def log(self, message: str, status: str = ""):
        """Log"""
        print(f"{status} {message}")

    # ===== PARTE 1: BACKEND =====

    def audit_backend_routes(self):
        """Audita rotas do backend"""
        self.log("\n" + "="*70)
        self.log("🔧 PARTE 1: BACKEND - ANÁLISE DE ROTAS/ENDPOINTS", "")
        self.log("="*70)

        routes_dir = self.root / "backend/src/api/routes"

        # Rotas esperadas
        expected_routes = [
            ("auth.py", "Autenticação"),
            ("clients.py", "Clientes"),
            ("leads.py", "Leads"),
            ("projects.py", "Projetos"),
            ("conversations.py", "Conversas"),
            ("messages.py", "Mensagens"),
            ("interviews.py", "Entrevistas"),
            ("sub_agents.py", "Sub-Agentes"),
            ("dashboard.py", "Dashboard"),
            ("isa.py", "ISA Agent"),
            ("renus_config.py", "RENUS Config"),
            ("tools.py", "Tools"),
            ("websocket.py", "WebSocket"),
            ("public_chat.py", "Public Chat"),
            ("health.py", "Health Check")
        ]

        route_status = {}

        for filename, name in expected_routes:
            filepath = routes_dir / filename
            exists = filepath.exists()

            if exists:
                # Contar endpoints (GET, POST, PUT, DELETE)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    endpoints = {
                        "GET": content.count("@router.get") + content.count('@router.get'),
                        "POST": content.count("@router.post") + content.count('@router.post'),
                        "PUT": content.count("@router.put") + content.count('@router.put'),
                        "DELETE": content.count("@router.delete") + content.count('@router.delete'),
                        "PATCH": content.count("@router.patch") + content.count('@router.patch'),
                    }

                    total_endpoints = sum(endpoints.values())
                    status = GREEN if total_endpoints > 0 else YELLOW
                    self.log(f"{name}: {total_endpoints} endpoints", status)

                    route_status[name] = {
                        "implemented": True,
                        "endpoints": endpoints,
                        "total": total_endpoints
                    }
            else:
                self.log(f"{name}: NÃO IMPLEMENTADO", RED)
                route_status[name] = {"implemented": False}

        self.results["backend"]["routes"] = route_status

    def audit_backend_models(self):
        """Audita modelos do backend"""
        self.log("\n📦 BACKEND - MODELS")

        models_dir = self.root / "backend/src/models"

        expected_models = [
            "user.py", "client.py", "lead.py", "project.py",
            "conversation.py", "message.py", "interview.py",
            "sub_agent.py", "tool.py", "renus_config.py",
            "isa_command.py"
        ]

        model_status = {}

        for model in expected_models:
            filepath = models_dir / model
            exists = filepath.exists()
            status = GREEN if exists else RED
            name = model.replace(".py", "")
            self.log(f"  Model {name}: {'IMPLEMENTADO' if exists else 'FALTANDO'}", status)

            model_status[name] = exists

        implemented = sum(1 for v in model_status.values() if v)
        total = len(model_status)

        self.results["backend"]["models"] = {
            "status": model_status,
            "implemented": implemented,
            "total": total,
            "percentage": round((implemented / total * 100) if total > 0 else 0, 1)
        }

    def audit_backend_services(self):
        """Audita services do backend"""
        self.log("\n🛠️  BACKEND - SERVICES")

        services_dir = self.root / "backend/src/services"

        expected_services = [
            "auth_service.py", "client_service.py", "lead_service.py",
            "project_service.py", "conversation_service.py", "message_service.py",
            "interview_service.py", "subagent_service.py", "dashboard_service.py",
            "isa_command_service.py", "renus_config_service.py", "tool_service.py"
        ]

        service_status = {}

        for service in expected_services:
            filepath = services_dir / service
            exists = filepath.exists()
            status = GREEN if exists else RED
            name = service.replace("_service.py", "")
            self.log(f"  Service {name}: {'IMPLEMENTADO' if exists else 'FALTANDO'}", status)

            service_status[name] = exists

        implemented = sum(1 for v in service_status.values() if v)
        total = len(service_status)

        self.results["backend"]["services"] = {
            "status": service_status,
            "implemented": implemented,
            "total": total,
            "percentage": round((implemented / total * 100) if total > 0 else 0, 1)
        }

    # ===== PARTE 2: FRONTEND =====

    def audit_frontend_menus(self):
        """Audita menus do frontend"""
        self.log("\n" + "="*70)
        self.log("🎨 PARTE 2: FRONTEND - ANÁLISE DE MENUS", "")
        self.log("="*70)

        # Verificar se existe pasta do frontend
        frontend_dirs = [
            self.root / "frontend",
            self.root / "admin",
            self.root / "client",
        ]

        frontend_dir = None
        for dir_path in frontend_dirs:
            if dir_path.exists():
                frontend_dir = dir_path
                break

        if not frontend_dir:
            self.log("Frontend não encontrado", RED)
            self.results["frontend"]["status"] = "NOT_FOUND"
            return

        self.log(f"Frontend encontrado em: {frontend_dir.name}", GREEN)

        # Procurar arquivos de páginas/menus
        menu_patterns = [
            "**/pages/**/*.tsx",
            "**/pages/**/*.jsx",
            "**/views/**/*.tsx",
            "**/views/**/*.jsx",
            "**/screens/**/*.tsx"
        ]

        all_pages = []
        for pattern in menu_patterns:
            all_pages.extend(frontend_dir.glob(pattern))

        # Menus esperados
        expected_menus = [
            "overview", "dashboard",
            "client", "clientes",
            "lead", "leads",
            "project", "projetos",
            "conversation", "conversas",
            "interview", "entrevista", "pesquisa",
            "isa", "assistant",
            "renus", "config",
            "report", "relatorio",
            "setting", "configurac"
        ]

        found_menus = {}

        for page in all_pages:
            page_name = page.stem.lower()
            for menu in expected_menus:
                if menu in page_name:
                    if menu not in found_menus:
                        found_menus[menu] = []
                    found_menus[menu].append(str(page.relative_to(frontend_dir)))

        self.log(f"\nEncontrados {len(found_menus)} tipos de menus:", GREEN)
        for menu, files in found_menus.items():
            self.log(f"  - {menu}: {len(files)} arquivos", GREEN)

        self.results["frontend"] = {
            "status": "FOUND",
            "location": str(frontend_dir.name),
            "total_pages": len(all_pages),
            "menu_types_found": len(found_menus),
            "menus": {k: len(v) for k, v in found_menus.items()}
        }

    # ===== PARTE 3: AGENTES =====

    def audit_agents(self):
        """Audita agentes LangChain"""
        self.log("\n" + "="*70)
        self.log("🤖 PARTE 3: AGENTES LANGCHAIN", "")
        self.log("="*70)

        agents_dir = self.root / "backend/src/agents"

        expected_agents = [
            ("renus.py", "RENUS Agent"),
            ("isa.py", "ISA Agent"),
            ("discovery_agent.py", "Discovery Agent"),
        ]

        agent_status = {}

        for filename, name in expected_agents:
            filepath = agents_dir / filename
            exists = filepath.exists()

            if exists:
                # Verificar implementação básica
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    has_class = "class" in content
                    has_langgraph = "langgraph" in content.lower() or "StateGraph" in content
                    has_langchain = "langchain" in content.lower() or "ChatOpenAI" in content or "ChatAnthropic" in content

                    completeness = sum([has_class, has_langgraph, has_langchain])
                    percentage = round(completeness / 3 * 100, 1)

                    if percentage >= 80:
                        status = GREEN
                        impl_status = "COMPLETO"
                    elif percentage >= 50:
                        status = YELLOW
                        impl_status = f"PARCIAL ({percentage}%)"
                    else:
                        status = RED
                        impl_status = f"INCOMPLETO ({percentage}%)"

                    self.log(f"{name}: {impl_status}", status)

                    agent_status[name] = {
                        "implemented": True,
                        "has_class": has_class,
                        "has_langgraph": has_langgraph,
                        "has_langchain": has_langchain,
                        "completeness": percentage
                    }
            else:
                self.log(f"{name}: NÃO IMPLEMENTADO", RED)
                agent_status[name] = {"implemented": False}

        self.results["agents"] = agent_status

    # ===== PARTE 4: INTEGRAÇÕES =====

    def audit_integrations(self):
        """Audita integrações"""
        self.log("\n" + "="*70)
        self.log("🔌 PARTE 4: INTEGRAÇÕES", "")
        self.log("="*70)

        # WebSocket
        ws_file = self.root / "backend/src/api/routes/websocket.py"
        ws_handler = self.root / "backend/src/api/websocket/ws_handler.py"

        ws_implemented = ws_file.exists() or ws_handler.exists()
        status = GREEN if ws_implemented else RED
        self.log(f"WebSocket: {'IMPLEMENTADO' if ws_implemented else 'NÃO IMPLEMENTADO'}", status)

        # Supabase
        supabase_file = self.root / "backend/src/config/supabase.py"
        supabase_implemented = supabase_file.exists()
        status = GREEN if supabase_implemented else RED
        self.log(f"Supabase Client: {'IMPLEMENTADO' if supabase_implemented else 'NÃO IMPLEMENTADO'}", status)

        # LangSmith
        langsmith_file = self.root / "backend/src/config/langsmith.py"
        langsmith_implemented = langsmith_file.exists()
        status = GREEN if langsmith_implemented else RED
        self.log(f"LangSmith: {'IMPLEMENTADO' if langsmith_implemented else 'NÃO IMPLEMENTADO'}", status)

        # Tools
        tools_dir = self.root / "backend/src/tools"
        tools = list(tools_dir.glob("*.py")) if tools_dir.exists() else []
        tool_names = [t.stem for t in tools if t.stem != "__init__"]

        self.log(f"Tools: {len(tool_names)} implementadas", GREEN if len(tool_names) > 0 else YELLOW)
        if tool_names:
            for tool in tool_names:
                self.log(f"  - {tool}", GREEN)

        self.results["integrations"] = {
            "websocket": ws_implemented,
            "supabase": supabase_implemented,
            "langsmith": langsmith_implemented,
            "tools": tool_names
        }

    # ===== RESUMO FINAL =====

    def generate_final_summary(self):
        """Gera resumo final"""
        self.log("\n" + "="*70)
        self.log("📊 RESUMO FINAL DA AUDITORIA", "")
        self.log("="*70)

        # Backend
        backend_routes = len([r for r in self.results["backend"]["routes"].values() if r.get("implemented", False)])
        total_routes = len(self.results["backend"]["routes"])
        backend_models = self.results["backend"]["models"]["implemented"]
        total_models = self.results["backend"]["models"]["total"]
        backend_services = self.results["backend"]["services"]["implemented"]
        total_services = self.results["backend"]["services"]["total"]

        self.log("\n🔧 BACKEND:")
        self.log(f"  Rotas: {backend_routes}/{total_routes} implementadas ({round(backend_routes/total_routes*100, 1)}%)")
        self.log(f"  Models: {backend_models}/{total_models} implementados ({round(backend_models/total_models*100, 1)}%)")
        self.log(f"  Services: {backend_services}/{total_services} implementados ({round(backend_services/total_services*100, 1)}%)")

        backend_completeness = round((backend_routes + backend_models + backend_services) / (total_routes + total_models + total_services) * 100, 1)

        # Frontend
        frontend_status = self.results["frontend"].get("status", "NOT_FOUND")
        frontend_menus = self.results["frontend"].get("menu_types_found", 0)

        self.log("\n🎨 FRONTEND:")
        self.log(f"  Status: {frontend_status}")
        if frontend_status == "FOUND":
            self.log(f"  Menus encontrados: {frontend_menus}")
            frontend_completeness = min(round(frontend_menus / 10 * 100, 1), 100)
        else:
            frontend_completeness = 0

        # Agentes
        agents_implemented = sum(1 for a in self.results["agents"].values() if a.get("implemented", False))
        total_agents = len(self.results["agents"])

        self.log("\n🤖 AGENTES:")
        self.log(f"  Implementados: {agents_implemented}/{total_agents}")

        if agents_implemented > 0:
            avg_completeness = round(sum(a.get("completeness", 0) for a in self.results["agents"].values() if a.get("implemented", False)) / agents_implemented, 1)
            self.log(f"  Completude média: {avg_completeness}%")
            agents_completeness = avg_completeness
        else:
            agents_completeness = 0

        # Integrações
        integrations = self.results["integrations"]
        integrations_count = sum([
            integrations.get("websocket", False),
            integrations.get("supabase", False),
            integrations.get("langsmith", False),
            len(integrations.get("tools", [])) > 0
        ])

        self.log("\n🔌 INTEGRAÇÕES:")
        self.log(f"  Implementadas: {integrations_count}/4")

        # Status Geral
        overall = round((backend_completeness + frontend_completeness + agents_completeness + (integrations_count/4*100)) / 4, 1)

        self.log("\n" + "="*70)
        self.log(f"🎯 STATUS GERAL DO SISTEMA: {overall}%", "")
        self.log("="*70)

        if overall >= 90:
            status = f"{GREEN} Sistema 90%+ implementado - PRONTO para produção"
        elif overall >= 70:
            status = f"{YELLOW} Sistema 70-90% implementado - PRECISA ajustes"
        elif overall >= 50:
            status = f"{PARTIAL} Sistema 50-70% implementado - EM DESENVOLVIMENTO"
        else:
            status = f"{RED} Sistema <50% implementado - INÍCIO de desenvolvimento"

        self.log(f"\n{status}")

        # Problemas Críticos
        self.log("\n⚠️  PROBLEMAS CRÍTICOS ENCONTRADOS:")
        self.log("  1. Backend NÃO ESTÁ RODANDO - Conflito de dependências (cryptography)")
        self.log("  2. Banco de dados NÃO ACESSÍVEL - Sem conectividade de rede")
        self.log("  3. Testes funcionais NÃO PUDERAM SER EXECUTADOS")

        self.log("\n✅ PONTOS POSITIVOS:")
        self.log(f"  - {backend_routes} rotas de API implementadas")
        self.log(f"  - {backend_models} modelos de dados definidos")
        self.log(f"  - {agents_implemented} agentes de IA implementados")
        self.log(f"  - Frontend existe com {frontend_menus} tipos de menus")

        self.results["summary"] = {
            "overall_completeness": overall,
            "backend_completeness": backend_completeness,
            "frontend_completeness": frontend_completeness,
            "agents_completeness": agents_completeness,
            "integrations_completeness": round(integrations_count/4*100, 1),
            "critical_issues": [
                "Backend não está rodando (dependências)",
                "Banco de dados não acessível (rede)",
                "Testes funcionais não executados"
            ]
        }

    def save_results(self):
        """Salva resultados"""
        with open("AUDITORIA_CODIGO_COMPLETA.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        self.log(f"\n{GREEN} Resultados salvos em: AUDITORIA_CODIGO_COMPLETA.json")

    def run_full_audit(self):
        """Executa auditoria completa"""
        print("\n" + "="*70)
        print("🔍 AUDITORIA COMPLETA DO SISTEMA RENUM")
        print("Análise de Código-Fonte")
        print("="*70)
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

        self.audit_backend_routes()
        self.audit_backend_models()
        self.audit_backend_services()
        self.audit_frontend_menus()
        self.audit_agents()
        self.audit_integrations()
        self.generate_final_summary()
        self.save_results()

        print("\n" + "="*70)
        print("✅ AUDITORIA COMPLETA CONCLUÍDA")
        print("="*70 + "\n")


if __name__ == "__main__":
    auditor = CodeAuditor()
    auditor.run_full_audit()
