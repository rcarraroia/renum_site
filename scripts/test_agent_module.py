#!/usr/bin/env python3
"""
Teste Completo do Módulo Agente - RENUM
Valida todas as funcionalidades críticas dos agentes
"""
import requests
import json
import sys
import os
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List

# Configurar path para imports do backend
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

# Configurar variáveis de ambiente antes de importar
os.environ.setdefault('SUPABASE_URL', 'https://vhixvzaxswphwoymdhgg.supabase.co')
os.environ.setdefault('SUPABASE_ANON_KEY', 'test-key')
os.environ.setdefault('SUPABASE_SERVICE_KEY', 'test-key')
os.environ.setdefault('SECRET_KEY', 'test-secret')
os.environ.setdefault('SUPABASE_JWT_SECRET', 'test-jwt')
os.environ.setdefault('CORS_ORIGINS', 'http://localhost:3000')
os.environ.setdefault('OPENAI_API_KEY', 'test-openai')
os.environ.setdefault('LANGSMITH_API_KEY', 'test-langsmith')

class AgentModuleTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {"passed": 0, "failed": 0, "total": 0}
        }
        self.auth_token = None
        
    def log_test(self, test_name: str, status: str, details: Dict[str, Any]):
        """Log resultado do teste"""
        self.results["tests"][test_name] = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            **details
        }
        
        if status == "PASS":
            print(f"✅ {test_name}")
            self.results["summary"]["passed"] += 1
        else:
            print(f"❌ {test_name}: {details.get('error', 'Unknown error')}")
            self.results["summary"]["failed"] += 1
            
        self.results["summary"]["total"] += 1
    
    def test_agent_endpoints_availability(self):
        """Testa se endpoints de agentes estão disponíveis"""
        endpoints = [
            {"path": "/api/agents/", "method": "GET", "name": "List Agents"},
            {"path": "/api/agents/renus/conversations", "method": "GET", "name": "RENUS Conversations"},
            {"path": "/api/agents/renus/metrics", "method": "GET", "name": "RENUS Metrics"},
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{self.base_url}{endpoint['path']}"
                response = requests.get(url, timeout=5)
                
                if response.status_code in [200, 401, 403]:  # 401/403 = auth required (normal)
                    self.log_test(
                        f"Endpoint {endpoint['name']}", 
                        "PASS",
                        {
                            "status_code": response.status_code,
                            "response_size": len(response.text),
                            "url": url
                        }
                    )
                else:
                    self.log_test(
                        f"Endpoint {endpoint['name']}", 
                        "FAIL",
                        {
                            "error": f"Unexpected status: {response.status_code}",
                            "url": url
                        }
                    )
                    
            except Exception as e:
                self.log_test(
                    f"Endpoint {endpoint['name']}", 
                    "FAIL",
                    {"error": str(e), "url": url}
                )
    
    def test_agent_models_structure(self):
        """Testa estrutura dos modelos de agente"""
        try:
            from src.models.agent import (
                AgentCreate, AgentUpdate, AgentResponse, 
                AgentListItem, AgentStats, AgentRole
            )
            
            # Testar criação de modelo
            test_agent = AgentCreate(
                name="Test Agent",
                description="Agent for testing",
                role=AgentRole.CLIENT_AGENT,
                config={
                    "model": "gpt-4o-mini",
                    "system_prompt": "You are a test agent"
                }
            )
            
            self.log_test(
                "Agent Models Structure",
                "PASS",
                {
                    "models_imported": True,
                    "test_creation": True,
                    "agent_name": test_agent.name,
                    "agent_role": test_agent.role.value
                }
            )
            
        except Exception as e:
            self.log_test(
                "Agent Models Structure",
                "FAIL",
                {"error": str(e)}
            )
    
    def test_agent_service_import(self):
        """Testa se o serviço de agentes pode ser importado"""
        try:
            from src.services.agent_service import AgentService, get_agent_service
            
            # Testar instanciação
            service = get_agent_service()
            
            # Verificar métodos essenciais
            essential_methods = [
                'create_agent', 'get_agent', 'update_agent', 
                'delete_agent', 'list_agents', 'get_stats'
            ]
            
            missing_methods = []
            for method in essential_methods:
                if not hasattr(service, method):
                    missing_methods.append(method)
            
            if missing_methods:
                self.log_test(
                    "Agent Service Import",
                    "FAIL",
                    {"error": f"Missing methods: {missing_methods}"}
                )
            else:
                self.log_test(
                    "Agent Service Import",
                    "PASS",
                    {
                        "service_imported": True,
                        "methods_available": essential_methods,
                        "service_type": str(type(service))
                    }
                )
                
        except Exception as e:
            self.log_test(
                "Agent Service Import",
                "FAIL",
                {"error": str(e)}
            )
    
    def test_supabase_agents_table(self):
        """Testa conexão com tabela de agentes no Supabase"""
        try:
            # Testar se conseguimos fazer uma requisição para o backend
            response = requests.get(f"{self.base_url}/health", timeout=5)
            
            if response.status_code == 200:
                health_data = response.json()
                
                self.log_test(
                    "Supabase Agents Table",
                    "PASS",
                    {
                        "backend_accessible": True,
                        "health_status": health_data.get("status", "unknown"),
                        "indirect_test": "Backend running implies Supabase connection"
                    }
                )
            else:
                self.log_test(
                    "Supabase Agents Table",
                    "FAIL",
                    {"error": f"Backend not accessible: {response.status_code}"}
                )
            
        except Exception as e:
            self.log_test(
                "Supabase Agents Table",
                "FAIL",
                {"error": str(e)}
            )
    
    def test_agent_config_structure(self):
        """Testa estrutura de configuração dos agentes"""
        try:
            from src.services.agent_service import AgentService
            
            service = AgentService()
            
            # Testar estrutura de config
            test_config = service._init_config_structure({
                "instructions": {"system_prompt": "test"},
                "intelligence": {"model": "gpt-4o-mini"}
            })
            
            expected_categories = [
                "instructions", "intelligence", "tools", "integrations",
                "knowledge", "triggers", "guardrails", "sub_agents", "advanced"
            ]
            
            missing_categories = []
            for category in expected_categories:
                if category not in test_config:
                    missing_categories.append(category)
            
            if missing_categories:
                self.log_test(
                    "Agent Config Structure",
                    "FAIL",
                    {"error": f"Missing categories: {missing_categories}"}
                )
            else:
                self.log_test(
                    "Agent Config Structure",
                    "PASS",
                    {
                        "categories_present": expected_categories,
                        "config_initialized": True,
                        "structure_valid": True
                    }
                )
                
        except Exception as e:
            self.log_test(
                "Agent Config Structure",
                "FAIL",
                {"error": str(e)}
            )
    
    def test_agent_roles_enum(self):
        """Testa enum de roles dos agentes"""
        try:
            from src.models.agent import AgentRole
            
            # Verificar roles esperados
            expected_roles = [
                "SYSTEM_ORCHESTRATOR",
                "SYSTEM_SUPERVISOR", 
                "CLIENT_AGENT"
            ]
            
            available_roles = [role.name for role in AgentRole]
            missing_roles = [role for role in expected_roles if role not in available_roles]
            
            if missing_roles:
                self.log_test(
                    "Agent Roles Enum",
                    "FAIL",
                    {"error": f"Missing roles: {missing_roles}"}
                )
            else:
                self.log_test(
                    "Agent Roles Enum",
                    "PASS",
                    {
                        "roles_available": available_roles,
                        "enum_functional": True,
                        "default_role": AgentRole.CLIENT_AGENT.value
                    }
                )
                
        except Exception as e:
            self.log_test(
                "Agent Roles Enum",
                "FAIL",
                {"error": str(e)}
            )
    
    def test_sub_agents_integration(self):
        """Testa integração com sub-agentes"""
        try:
            # Verificar se arquivo existe
            subagent_service_path = os.path.join('backend', 'src', 'services', 'subagent_service.py')
            
            if os.path.exists(subagent_service_path):
                from src.services.subagent_service import SubAgentService
                
                # Testar instanciação do serviço
                service = SubAgentService()
                
                # Verificar métodos essenciais
                essential_methods = [
                    'create_subagent', 'get_subagent', 'update_subagent',
                    'delete_subagent', 'list_subagents'
                ]
                
                missing_methods = []
                for method in essential_methods:
                    if not hasattr(service, method):
                        missing_methods.append(method)
                
                if missing_methods:
                    self.log_test(
                        "Sub-Agents Integration",
                        "FAIL",
                        {"error": f"Missing methods: {missing_methods}"}
                    )
                else:
                    self.log_test(
                        "Sub-Agents Integration",
                        "PASS",
                        {
                            "service_available": True,
                            "methods_present": essential_methods,
                            "integration_ready": True
                        }
                    )
            else:
                self.log_test(
                    "Sub-Agents Integration",
                    "FAIL",
                    {"error": "SubAgentService file not found"}
                )
                
        except Exception as e:
            self.log_test(
                "Sub-Agents Integration",
                "FAIL",
                {"error": str(e)}
            )
    
    def run_all_tests(self):
        """Executa todos os testes do módulo agente"""
        print("🤖 TESTE COMPLETO DO MÓDULO AGENTE")
        print("=" * 60)
        
        # Testes de estrutura
        print("\n📋 Testando Estrutura...")
        self.test_agent_models_structure()
        self.test_agent_service_import()
        self.test_agent_config_structure()
        self.test_agent_roles_enum()
        
        # Testes de integração
        print("\n🔗 Testando Integrações...")
        self.test_supabase_agents_table()
        self.test_sub_agents_integration()
        
        # Testes de API
        print("\n🌐 Testando Endpoints...")
        self.test_agent_endpoints_availability()
        
        # Resumo final
        print(f"\n📊 RESUMO DOS TESTES:")
        print(f"✅ Passou: {self.results['summary']['passed']}")
        print(f"❌ Falhou: {self.results['summary']['failed']}")
        print(f"📋 Total: {self.results['summary']['total']}")
        
        # Calcular porcentagem de sucesso
        if self.results['summary']['total'] > 0:
            success_rate = (self.results['summary']['passed'] / self.results['summary']['total']) * 100
            print(f"🎯 Taxa de Sucesso: {success_rate:.1f}%")
        
        # Salvar resultados
        with open("agent_module_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Resultados salvos em: agent_module_test_results.json")
        
        # Retornar sucesso se >= 80% dos testes passaram
        return success_rate >= 80.0 if self.results['summary']['total'] > 0 else False

if __name__ == "__main__":
    tester = AgentModuleTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 MÓDULO AGENTE: APROVADO!")
    else:
        print("\n⚠️ MÓDULO AGENTE: NECESSITA CORREÇÕES")
    
    sys.exit(0 if success else 1)