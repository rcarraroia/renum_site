"""
🔍 AUDITORIA COMPLETA DO SISTEMA RENUM
Testa TODOS os endpoints, menus e funcionalidades
"""
import httpx
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Configurações
BASE_URL = "http://localhost:8000"
TIMEOUT = 10.0

# Cores para output
GREEN = "✅"
YELLOW = "⚠️"
RED = "❌"
CLOCK = "⏳"

class SystemAuditor:
    def __init__(self):
        self.results = {
            "backend": {},
            "summary": {
                "total": 0,
                "passed": 0,
                "partial": 0,
                "failed": 0,
                "not_tested": 0
            }
        }
        self.token = None
        self.test_user_id = None
        self.test_client_id = None
        self.test_lead_id = None
        self.test_project_id = None
        self.test_conversation_id = None
        self.test_interview_id = None
        
    def log(self, message: str, status: str = ""):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status} {message}")
    
    def update_summary(self, status: str):
        """Atualiza contadores do resumo"""
        self.results["summary"]["total"] += 1
        if status == "passed":
            self.results["summary"]["passed"] += 1
        elif status == "partial":
            self.results["summary"]["partial"] += 1
        elif status == "failed":
            self.results["summary"]["failed"] += 1
        else:
            self.results["summary"]["not_tested"] += 1
    
    async def test_endpoint(self, method: str, path: str, name: str, 
                           data: Dict = None, headers: Dict = None,
                           expected_status: List[int] = [200, 201]) -> Dict:
        """Testa um endpoint e retorna resultado"""
        self.log(f"Testando: {name}", CLOCK)
        
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                url = f"{BASE_URL}{path}"
                
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, json=data, headers=headers)
                elif method == "PUT":
                    response = await client.put(url, json=data, headers=headers)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    raise ValueError(f"Método não suportado: {method}")
                
                # Verificar status
                if response.status_code in expected_status:
                    self.log(f"{name}: OK (status {response.status_code})", GREEN)
                    self.update_summary("passed")
                    return {
                        "status": "passed",
                        "code": response.status_code,
                        "data": response.json() if response.text else None
                    }
                else:
                    self.log(f"{name}: Status inesperado {response.status_code}", YELLOW)
                    self.update_summary("partial")
                    return {
                        "status": "partial",
                        "code": response.status_code,
                        "error": response.text
                    }
                    
        except httpx.TimeoutException:
            self.log(f"{name}: TIMEOUT", RED)
            self.update_summary("failed")
            return {"status": "failed", "error": "Timeout"}
        except Exception as e:
            self.log(f"{name}: ERRO - {str(e)}", RED)
            self.update_summary("failed")
            return {"status": "failed", "error": str(e)}
    
    async def test_health(self):
        """Testa endpoints de health"""
        self.log("\n" + "="*60)
        self.log("🏥 TESTANDO HEALTH CHECKS")
        self.log("="*60)
        
        result = await self.test_endpoint("GET", "/health", "Health Check")
        self.results["backend"]["health"] = result
        
        result = await self.test_endpoint("GET", "/", "Root Endpoint")
        self.results["backend"]["root"] = result
    
    async def test_auth(self):
        """Testa autenticação"""
        self.log("\n" + "="*60)
        self.log("🔐 TESTANDO AUTENTICAÇÃO")
        self.log("="*60)
        
        # 1. Tentar login com usuário existente
        login_data = {
            "email": "kiro.auditoria@renum.com",
            "password": "Auditoria@2025!"
        }
        
        result = await self.test_endpoint(
            "POST", "/auth/login", 
            "Login com kiro.auditoria@renum.com",
            data=login_data
        )
        self.results["backend"]["auth_login"] = result
        
        # Salvar token se login funcionou
        if result["status"] == "passed" and result.get("data"):
            self.token = result["data"].get("access_token")
            self.test_user_id = result["data"].get("user", {}).get("id")
            self.log(f"Token obtido: {self.token[:20]}...", GREEN)
        
        # 2. Testar /me com token
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            result = await self.test_endpoint(
                "GET", "/auth/me",
                "GET /auth/me (usuário autenticado)",
                headers=headers
            )
            self.results["backend"]["auth_me"] = result
        else:
            self.log("Pulando teste /me - sem token", YELLOW)
            self.update_summary("not_tested")
            self.results["backend"]["auth_me"] = {"status": "not_tested", "reason": "No token"}
        
        # 3. Testar register (criar novo usuário de teste)
        register_data = {
            "email": f"test_{datetime.now().timestamp()}@test.com",
            "password": "test123",
            "full_name": "Test User Audit"
        }
        
        result = await self.test_endpoint(
            "POST", "/auth/register",
            "POST /auth/register (criar usuário)",
            data=register_data
        )
        self.results["backend"]["auth_register"] = result
    
    async def test_clients(self):
        """Testa CRUD de clientes"""
        self.log("\n" + "="*60)
        self.log("👥 TESTANDO CLIENTS (CRUD)")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Clients - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. GET /api/clients (listar)
        result = await self.test_endpoint(
            "GET", "/api/clients",
            "GET /api/clients (listar)",
            headers=headers
        )
        self.results["backend"]["clients_list"] = result
        
        # 2. POST /api/clients (criar)
        client_data = {
            "company_name": f"Empresa Teste Audit {datetime.now().timestamp()}",
            "cnpj": "12345678000199",
            "plan": "basic",
            "status": "active"
        }
        
        result = await self.test_endpoint(
            "POST", "/api/clients",
            "POST /api/clients (criar)",
            data=client_data,
            headers=headers,
            expected_status=[200, 201]
        )
        self.results["backend"]["clients_create"] = result
        
        # Salvar ID do cliente criado
        if result["status"] == "passed" and result.get("data"):
            self.test_client_id = result["data"].get("id")
            self.log(f"Cliente criado: {self.test_client_id}", GREEN)
        
        # 3. GET /api/clients/{id} (buscar específico)
        if self.test_client_id:
            result = await self.test_endpoint(
                "GET", f"/api/clients/{self.test_client_id}",
                "GET /api/clients/{id} (buscar específico)",
                headers=headers
            )
            self.results["backend"]["clients_get"] = result
        else:
            self.log("Pulando GET /api/clients/{id} - sem client_id", YELLOW)
            self.update_summary("not_tested")
        
        # 4. PUT /api/clients/{id} (atualizar)
        if self.test_client_id:
            update_data = {
                "company_name": "Empresa Teste ATUALIZADA",
                "plan": "pro"
            }
            result = await self.test_endpoint(
                "PUT", f"/api/clients/{self.test_client_id}",
                "PUT /api/clients/{id} (atualizar)",
                data=update_data,
                headers=headers
            )
            self.results["backend"]["clients_update"] = result
        else:
            self.log("Pulando PUT /api/clients/{id} - sem client_id", YELLOW)
            self.update_summary("not_tested")
        
        # 5. DELETE /api/clients/{id} (deletar) - NÃO vamos deletar para usar em outros testes
        self.log("DELETE /api/clients/{id} - Pulado (preservar para outros testes)", CLOCK)
        self.update_summary("not_tested")
    
    async def test_leads(self):
        """Testa CRUD de leads"""
        self.log("\n" + "="*60)
        self.log("📞 TESTANDO LEADS (CRUD)")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Leads - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. GET /api/leads (listar)
        result = await self.test_endpoint(
            "GET", "/api/leads",
            "GET /api/leads (listar)",
            headers=headers
        )
        self.results["backend"]["leads_list"] = result
        
        # 2. POST /api/leads (criar)
        if self.test_client_id:
            lead_data = {
                "client_id": self.test_client_id,
                "phone": "+5511999999999",
                "name": f"Lead Teste Audit {datetime.now().timestamp()}",
                "email": f"lead_{datetime.now().timestamp()}@test.com",
                "status": "active"
            }
            
            result = await self.test_endpoint(
                "POST", "/api/leads",
                "POST /api/leads (criar)",
                data=lead_data,
                headers=headers,
                expected_status=[200, 201]
            )
            self.results["backend"]["leads_create"] = result
            
            # Salvar ID do lead criado
            if result["status"] == "passed" and result.get("data"):
                self.test_lead_id = result["data"].get("id")
                self.log(f"Lead criado: {self.test_lead_id}", GREEN)
        else:
            self.log("Pulando POST /api/leads - sem client_id", YELLOW)
            self.update_summary("not_tested")
        
        # 3. GET /api/leads/{id}
        if self.test_lead_id:
            result = await self.test_endpoint(
                "GET", f"/api/leads/{self.test_lead_id}",
                "GET /api/leads/{id} (buscar específico)",
                headers=headers
            )
            self.results["backend"]["leads_get"] = result
        else:
            self.log("Pulando GET /api/leads/{id} - sem lead_id", YELLOW)
            self.update_summary("not_tested")
        
        # 4. PUT /api/leads/{id}
        if self.test_lead_id:
            update_data = {
                "name": "Lead Teste ATUALIZADO",
                "status": "inactive"
            }
            result = await self.test_endpoint(
                "PUT", f"/api/leads/{self.test_lead_id}",
                "PUT /api/leads/{id} (atualizar)",
                data=update_data,
                headers=headers
            )
            self.results["backend"]["leads_update"] = result
        else:
            self.log("Pulando PUT /api/leads/{id} - sem lead_id", YELLOW)
            self.update_summary("not_tested")
    
    async def test_projects(self):
        """Testa CRUD de projetos"""
        self.log("\n" + "="*60)
        self.log("📁 TESTANDO PROJECTS (CRUD)")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Projects - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. GET /api/projects
        result = await self.test_endpoint(
            "GET", "/api/projects",
            "GET /api/projects (listar)",
            headers=headers
        )
        self.results["backend"]["projects_list"] = result
        
        # 2. POST /api/projects
        if self.test_client_id:
            project_data = {
                "client_id": self.test_client_id,
                "name": f"Projeto Teste Audit {datetime.now().timestamp()}",
                "description": "Projeto criado durante auditoria",
                "type": "survey",
                "status": "active"
            }
            
            result = await self.test_endpoint(
                "POST", "/api/projects",
                "POST /api/projects (criar)",
                data=project_data,
                headers=headers,
                expected_status=[200, 201]
            )
            self.results["backend"]["projects_create"] = result
            
            if result["status"] == "passed" and result.get("data"):
                self.test_project_id = result["data"].get("id")
                self.log(f"Projeto criado: {self.test_project_id}", GREEN)
        else:
            self.log("Pulando POST /api/projects - sem client_id", YELLOW)
            self.update_summary("not_tested")
        
        # 3. GET /api/projects/{id}
        if self.test_project_id:
            result = await self.test_endpoint(
                "GET", f"/api/projects/{self.test_project_id}",
                "GET /api/projects/{id} (buscar específico)",
                headers=headers
            )
            self.results["backend"]["projects_get"] = result
        else:
            self.log("Pulando GET /api/projects/{id} - sem project_id", YELLOW)
            self.update_summary("not_tested")
        
        # 4. PUT /api/projects/{id}
        if self.test_project_id:
            update_data = {
                "name": "Projeto Teste ATUALIZADO",
                "status": "paused"
            }
            result = await self.test_endpoint(
                "PUT", f"/api/projects/{self.test_project_id}",
                "PUT /api/projects/{id} (atualizar)",
                data=update_data,
                headers=headers
            )
            self.results["backend"]["projects_update"] = result
        else:
            self.log("Pulando PUT /api/projects/{id} - sem project_id", YELLOW)
            self.update_summary("not_tested")
    
    async def test_conversations(self):
        """Testa endpoints de conversas"""
        self.log("\n" + "="*60)
        self.log("💬 TESTANDO CONVERSATIONS")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Conversations - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. GET /api/conversations
        result = await self.test_endpoint(
            "GET", "/api/conversations",
            "GET /api/conversations (listar)",
            headers=headers
        )
        self.results["backend"]["conversations_list"] = result
        
        # 2. POST /api/conversations
        if self.test_lead_id and self.test_client_id:
            conversation_data = {
                "lead_id": self.test_lead_id,
                "client_id": self.test_client_id,
                "status": "open"
            }
            
            result = await self.test_endpoint(
                "POST", "/api/conversations",
                "POST /api/conversations (criar)",
                data=conversation_data,
                headers=headers,
                expected_status=[200, 201]
            )
            self.results["backend"]["conversations_create"] = result
            
            if result["status"] == "passed" and result.get("data"):
                self.test_conversation_id = result["data"].get("id")
                self.log(f"Conversa criada: {self.test_conversation_id}", GREEN)
        else:
            self.log("Pulando POST /api/conversations - sem lead_id ou client_id", YELLOW)
            self.update_summary("not_tested")
        
        # 3. GET /api/conversations/{id}
        if self.test_conversation_id:
            result = await self.test_endpoint(
                "GET", f"/api/conversations/{self.test_conversation_id}",
                "GET /api/conversations/{id} (buscar específica)",
                headers=headers
            )
            self.results["backend"]["conversations_get"] = result
        else:
            self.log("Pulando GET /api/conversations/{id} - sem conversation_id", YELLOW)
            self.update_summary("not_tested")
        
        # 4. GET /api/conversations/{id}/messages
        if self.test_conversation_id:
            result = await self.test_endpoint(
                "GET", f"/api/conversations/{self.test_conversation_id}/messages",
                "GET /api/conversations/{id}/messages (listar mensagens)",
                headers=headers
            )
            self.results["backend"]["conversations_messages"] = result
        else:
            self.log("Pulando GET /api/conversations/{id}/messages - sem conversation_id", YELLOW)
            self.update_summary("not_tested")
    
    async def test_messages(self):
        """Testa endpoints de mensagens"""
        self.log("\n" + "="*60)
        self.log("✉️ TESTANDO MESSAGES")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Messages - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # POST /api/conversations/{id}/messages
        if self.test_conversation_id:
            message_data = {
                "content": "Mensagem de teste da auditoria",
                "role": "user"
            }
            
            result = await self.test_endpoint(
                "POST", f"/api/conversations/{self.test_conversation_id}/messages",
                "POST /api/conversations/{id}/messages (enviar mensagem)",
                data=message_data,
                headers=headers,
                expected_status=[200, 201]
            )
            self.results["backend"]["messages_create"] = result
        else:
            self.log("Pulando POST messages - sem conversation_id", YELLOW)
            self.update_summary("not_tested")
    
    async def test_interviews(self):
        """Testa endpoints de entrevistas"""
        self.log("\n" + "="*60)
        self.log("📋 TESTANDO INTERVIEWS")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Interviews - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. GET /api/interviews
        result = await self.test_endpoint(
            "GET", "/api/interviews",
            "GET /api/interviews (listar)",
            headers=headers
        )
        self.results["backend"]["interviews_list"] = result
        
        # 2. POST /api/interviews/start
        if self.test_lead_id and self.test_project_id:
            interview_data = {
                "lead_id": self.test_lead_id,
                "project_id": self.test_project_id
            }
            
            result = await self.test_endpoint(
                "POST", "/api/interviews/start",
                "POST /api/interviews/start (iniciar entrevista)",
                data=interview_data,
                headers=headers,
                expected_status=[200, 201]
            )
            self.results["backend"]["interviews_start"] = result
            
            if result["status"] == "passed" and result.get("data"):
                self.test_interview_id = result["data"].get("id")
                self.log(f"Entrevista criada: {self.test_interview_id}", GREEN)
        else:
            self.log("Pulando POST /api/interviews/start - sem lead_id ou project_id", YELLOW)
            self.update_summary("not_tested")
        
        # 3. GET /api/interviews/{id}
        if self.test_interview_id:
            result = await self.test_endpoint(
                "GET", f"/api/interviews/{self.test_interview_id}",
                "GET /api/interviews/{id} (buscar específica)",
                headers=headers
            )
            self.results["backend"]["interviews_get"] = result
        else:
            self.log("Pulando GET /api/interviews/{id} - sem interview_id", YELLOW)
            self.update_summary("not_tested")
    
    async def test_sub_agents(self):
        """Testa endpoints de sub-agentes"""
        self.log("\n" + "="*60)
        self.log("🤖 TESTANDO SUB-AGENTS")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Sub-Agents - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # GET /api/sub-agents
        result = await self.test_endpoint(
            "GET", "/api/sub-agents",
            "GET /api/sub-agents (listar)",
            headers=headers
        )
        self.results["backend"]["sub_agents_list"] = result
    
    async def test_dashboard(self):
        """Testa endpoints de dashboard"""
        self.log("\n" + "="*60)
        self.log("📊 TESTANDO DASHBOARD")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de Dashboard - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # GET /api/dashboard/stats
        result = await self.test_endpoint(
            "GET", "/api/dashboard/stats",
            "GET /api/dashboard/stats (métricas)",
            headers=headers
        )
        self.results["backend"]["dashboard_stats"] = result
    
    async def test_isa(self):
        """Testa endpoints do ISA"""
        self.log("\n" + "="*60)
        self.log("🧠 TESTANDO ISA AGENT")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de ISA - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # POST /api/isa/chat
        isa_data = {
            "message": "Liste os últimos clientes"
        }
        
        result = await self.test_endpoint(
            "POST", "/api/isa/chat",
            "POST /api/isa/chat (enviar mensagem)",
            data=isa_data,
            headers=headers
        )
        self.results["backend"]["isa_chat"] = result
    
    async def test_renus_config(self):
        """Testa endpoints de configuração RENUS"""
        self.log("\n" + "="*60)
        self.log("⚙️ TESTANDO RENUS CONFIG")
        self.log("="*60)
        
        if not self.token:
            self.log("Pulando testes de RENUS Config - sem autenticação", YELLOW)
            return
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # GET /api/renus-config
        result = await self.test_endpoint(
            "GET", "/api/renus-config",
            "GET /api/renus-config (buscar configuração)",
            headers=headers
        )
        self.results["backend"]["renus_config_get"] = result
    
    async def run_all_tests(self):
        """Executa todos os testes"""
        self.log("\n" + "="*60)
        self.log("🚀 INICIANDO AUDITORIA COMPLETA DO SISTEMA")
        self.log("="*60)
        self.log(f"Base URL: {BASE_URL}")
        self.log(f"Timestamp: {datetime.now().isoformat()}")
        
        # Executar testes em ordem
        await self.test_health()
        await self.test_auth()
        await self.test_clients()
        await self.test_leads()
        await self.test_projects()
        await self.test_conversations()
        await self.test_messages()
        await self.test_interviews()
        await self.test_sub_agents()
        await self.test_dashboard()
        await self.test_isa()
        await self.test_renus_config()
        
        # Gerar relatório final
        self.generate_report()
    
    def generate_report(self):
        """Gera relatório final"""
        self.log("\n" + "="*60)
        self.log("📊 RELATÓRIO FINAL DA AUDITORIA")
        self.log("="*60)
        
        summary = self.results["summary"]
        total = summary["total"]
        passed = summary["passed"]
        partial = summary["partial"]
        failed = summary["failed"]
        not_tested = summary["not_tested"]
        
        # Calcular percentuais
        passed_pct = (passed / total * 100) if total > 0 else 0
        partial_pct = (partial / total * 100) if total > 0 else 0
        failed_pct = (failed / total * 100) if total > 0 else 0
        not_tested_pct = (not_tested / total * 100) if total > 0 else 0
        
        self.log(f"\nTotal de testes: {total}")
        self.log(f"{GREEN} Passou: {passed} ({passed_pct:.1f}%)")
        self.log(f"{YELLOW} Parcial: {partial} ({partial_pct:.1f}%)")
        self.log(f"{RED} Falhou: {failed} ({failed_pct:.1f}%)")
        self.log(f"{CLOCK} Não testado: {not_tested} ({not_tested_pct:.1f}%)")
        
        # Status geral
        if passed_pct >= 90:
            status = f"{GREEN} Sistema 90%+ funcional - PRONTO"
        elif passed_pct >= 70:
            status = f"{YELLOW} Sistema 70-90% funcional - PRECISA CORREÇÕES"
        else:
            status = f"{RED} Sistema <70% funcional - MUITOS PROBLEMAS"
        
        self.log(f"\nStatus Geral: {status}")
        
        # Salvar resultados em arquivo
        with open("AUDITORIA_RESULTADOS.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.log(f"\n{GREEN} Resultados salvos em: AUDITORIA_RESULTADOS.json")
        self.log("="*60)


async def main():
    auditor = SystemAuditor()
    await auditor.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
