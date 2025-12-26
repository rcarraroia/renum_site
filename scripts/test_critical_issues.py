#!/usr/bin/env python3
"""
TESTE DOS PROBLEMAS CRÍTICOS IDENTIFICADOS
==========================================

Este script testa especificamente os 3 problemas críticos:
1. Sistema de Sub-Agentes bloqueado
2. Incompatibilidade Frontend ↔ Backend APIs  
3. Sistema de Integrações incompleto

Executa apenas quando backend estiver rodando.
"""

import os
import sys
import requests
import json
from datetime import datetime
from typing import Dict, Any, List

# Adicionar path do backend para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

class CriticalIssuesTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.results = []
        
    def log_result(self, test_name: str, status: str, details: str, critical: bool = False):
        """Log resultado do teste"""
        result = {
            "test": test_name,
            "status": status,  # "PASS", "FAIL", "SKIP"
            "details": details,
            "critical": critical,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        critical_flag = " 🚨" if critical else ""
        print(f"{icon} {test_name}: {details}{critical_flag}")
    
    def test_backend_connectivity(self) -> bool:
        """Testa se backend está rodando"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_result("Backend Connectivity", "PASS", f"Status {response.status_code}")
                return True
            else:
                self.log_result("Backend Connectivity", "FAIL", f"Status {response.status_code}", critical=True)
                return False
        except Exception as e:
            self.log_result("Backend Connectivity", "FAIL", f"Erro: {str(e)[:100]}", critical=True)
            return False
    
    def test_subagent_api_compatibility(self):
        """Testa compatibilidade das APIs de sub-agentes"""
        print("\n🤖 TESTANDO COMPATIBILIDADE API SUB-AGENTES...")
        
        # Primeiro, buscar um agente para usar como parent
        try:
            # Listar agentes
            response = requests.get(f"{self.backend_url}/api/agents", timeout=10)
            if response.status_code != 200:
                self.log_result("List Agents API", "FAIL", f"Status {response.status_code}", critical=True)
                return
            
            agents = response.json()
            if not agents:
                self.log_result("List Agents API", "FAIL", "Nenhum agente encontrado", critical=True)
                return
            
            # Usar primeiro agente como parent
            parent_agent_id = agents[0]['id']
            self.log_result("List Agents API", "PASS", f"Encontrados {len(agents)} agentes")
            
            # Testar endpoint de listagem de sub-agentes
            response = requests.get(f"{self.backend_url}/api/agents/{parent_agent_id}/sub-agents", timeout=10)
            if response.status_code == 200:
                sub_agents = response.json()
                self.log_result("List Sub-Agents API", "PASS", f"Endpoint funciona, {len(sub_agents)} sub-agentes")
            else:
                self.log_result("List Sub-Agents API", "FAIL", f"Status {response.status_code}: {response.text[:200]}", critical=True)
                return
            
            # Testar criação de sub-agente
            test_subagent = {
                "name": "Teste API Compatibility",
                "description": "Sub-agente de teste para validar compatibilidade",
                "specialization": "test",
                "config": {
                    "channel": "whatsapp",
                    "model": "gpt-4o-mini",
                    "system_prompt": "Você é um agente de teste."
                },
                "inheritance_config": {}
            }
            
            response = requests.post(
                f"{self.backend_url}/api/agents/{parent_agent_id}/sub-agents",
                json=test_subagent,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                created_subagent = response.json()
                self.log_result("Create Sub-Agent API", "PASS", f"Sub-agente criado: {created_subagent.get('id', 'N/A')}")
                
                # Testar estrutura de resposta (compatibilidade frontend)
                expected_fields = ['id', 'name', 'description']
                missing_fields = [field for field in expected_fields if field not in created_subagent]
                
                if missing_fields:
                    self.log_result("Sub-Agent Response Structure", "FAIL", 
                                  f"Campos faltando: {missing_fields}", critical=True)
                else:
                    self.log_result("Sub-Agent Response Structure", "PASS", "Estrutura compatível")
                
                # Limpar teste - deletar sub-agente criado
                try:
                    delete_response = requests.delete(
                        f"{self.backend_url}/api/agents/{parent_agent_id}/sub-agents/{created_subagent['id']}",
                        timeout=5
                    )
                    if delete_response.status_code in [200, 204]:
                        self.log_result("Delete Sub-Agent API", "PASS", "Sub-agente de teste removido")
                    else:
                        self.log_result("Delete Sub-Agent API", "FAIL", f"Status {delete_response.status_code}")
                except Exception as e:
                    self.log_result("Delete Sub-Agent API", "FAIL", f"Erro: {str(e)[:100]}")
                    
            else:
                self.log_result("Create Sub-Agent API", "FAIL", 
                              f"Status {response.status_code}: {response.text[:200]}", critical=True)
                
        except Exception as e:
            self.log_result("Sub-Agent API Test", "FAIL", f"Erro geral: {str(e)[:100]}", critical=True)
    
    def test_integration_api_compatibility(self):
        """Testa compatibilidade das APIs de integrações"""
        print("\n🔌 TESTANDO COMPATIBILIDADE API INTEGRAÇÕES...")
        
        try:
            # Testar endpoint de listagem de integrações
            response = requests.get(f"{self.backend_url}/api/integrations", timeout=10)
            
            if response.status_code == 200:
                integrations = response.json()
                self.log_result("List Integrations API", "PASS", f"Endpoint funciona, {len(integrations)} integrações")
            elif response.status_code == 404:
                self.log_result("List Integrations API", "FAIL", "Endpoint não encontrado", critical=True)
            else:
                self.log_result("List Integrations API", "FAIL", f"Status {response.status_code}: {response.text[:200]}")
            
            # Testar endpoint específico de integração
            test_providers = ['uazapi', 'chatwoot', 'google', 'supabase_external']
            
            for provider in test_providers:
                try:
                    response = requests.get(f"{self.backend_url}/api/integrations/{provider}", timeout=5)
                    if response.status_code in [200, 404]:  # 404 é OK (não configurado)
                        status = "configurado" if response.status_code == 200 else "não configurado"
                        self.log_result(f"Integration {provider}", "PASS", f"Endpoint funciona - {status}")
                    else:
                        self.log_result(f"Integration {provider}", "FAIL", f"Status {response.status_code}")
                except Exception as e:
                    self.log_result(f"Integration {provider}", "FAIL", f"Erro: {str(e)[:50]}")
            
            # Testar criação de integração (mock)
            test_integration = {
                "provider": "test_provider",
                "config": {
                    "api_key": "test_key",
                    "url": "https://test.com"
                },
                "is_active": True
            }
            
            response = requests.post(
                f"{self.backend_url}/api/integrations",
                json=test_integration,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                self.log_result("Create Integration API", "PASS", "Endpoint de criação funciona")
                
                # Limpar teste
                try:
                    created_integration = response.json()
                    if 'id' in created_integration:
                        requests.delete(f"{self.backend_url}/api/integrations/{created_integration['id']}", timeout=5)
                except:
                    pass
                    
            elif response.status_code == 404:
                self.log_result("Create Integration API", "FAIL", "Endpoint não implementado", critical=True)
            else:
                self.log_result("Create Integration API", "FAIL", f"Status {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("Integration API Test", "FAIL", f"Erro geral: {str(e)[:100]}", critical=True)
    
    def test_conversation_memory_structure(self):
        """Testa estrutura de memória de conversas"""
        print("\n🧠 TESTANDO ESTRUTURA DE MEMÓRIA...")
        
        try:
            # Testar endpoint de conversas
            response = requests.get(f"{self.backend_url}/api/conversations", timeout=10)
            
            if response.status_code == 200:
                conversations = response.json()
                self.log_result("Conversations API", "PASS", f"Endpoint funciona, {len(conversations)} conversas")
                
                # Se há conversas, testar estrutura de mensagens
                if conversations:
                    conv_id = conversations[0]['id']
                    messages_response = requests.get(f"{self.backend_url}/api/conversations/{conv_id}/messages", timeout=5)
                    
                    if messages_response.status_code == 200:
                        messages = messages_response.json()
                        self.log_result("Conversation Messages API", "PASS", f"{len(messages)} mensagens encontradas")
                        
                        # Verificar se há múltiplas mensagens (indicativo de memória)
                        if len(messages) > 1:
                            self.log_result("Conversation Memory", "PASS", "Múltiplas mensagens - memória funcionando")
                        else:
                            self.log_result("Conversation Memory", "FAIL", "Apenas 1 mensagem - possível problema de memória")
                    else:
                        self.log_result("Conversation Messages API", "FAIL", f"Status {messages_response.status_code}")
                else:
                    self.log_result("Conversation Memory", "SKIP", "Nenhuma conversa para testar")
                    
            elif response.status_code == 404:
                self.log_result("Conversations API", "FAIL", "Endpoint não encontrado", critical=True)
            else:
                self.log_result("Conversations API", "FAIL", f"Status {response.status_code}: {response.text[:200]}")
                
        except Exception as e:
            self.log_result("Conversation Memory Test", "FAIL", f"Erro: {str(e)[:100]}")
    
    def test_api_documentation(self):
        """Testa se documentação da API está acessível"""
        print("\n📚 TESTANDO DOCUMENTAÇÃO DA API...")
        
        try:
            # Testar Swagger/OpenAPI docs
            response = requests.get(f"{self.backend_url}/docs", timeout=5)
            if response.status_code == 200:
                self.log_result("API Documentation", "PASS", "Swagger docs acessível")
                
                # Verificar se contém endpoints críticos
                docs_content = response.text.lower()
                critical_endpoints = [
                    "/api/agents/{agent_id}/sub-agents",
                    "/api/integrations",
                    "/api/conversations"
                ]
                
                for endpoint in critical_endpoints:
                    if endpoint.lower() in docs_content:
                        self.log_result(f"Docs - {endpoint}", "PASS", "Endpoint documentado")
                    else:
                        self.log_result(f"Docs - {endpoint}", "FAIL", "Endpoint não documentado")
                        
            else:
                self.log_result("API Documentation", "FAIL", f"Status {response.status_code}")
                
        except Exception as e:
            self.log_result("API Documentation", "FAIL", f"Erro: {str(e)[:100]}")
    
    def run_all_tests(self):
        """Executa todos os testes críticos"""
        print("🔍 TESTANDO PROBLEMAS CRÍTICOS IDENTIFICADOS")
        print(f"⏰ Timestamp: {datetime.now().isoformat()}")
        print("="*60)
        
        # Teste 1: Conectividade
        if not self.test_backend_connectivity():
            print("\n❌ Backend não está rodando - pulando testes de API")
            self.print_summary()
            return self.results
        
        # Teste 2: Sub-Agentes (Problema Crítico #1)
        self.test_subagent_api_compatibility()
        
        # Teste 3: Integrações (Problema Crítico #3)
        self.test_integration_api_compatibility()
        
        # Teste 4: Memória de Conversas (Problema Crítico #2)
        self.test_conversation_memory_structure()
        
        # Teste 5: Documentação
        self.test_api_documentation()
        
        # Resumo
        self.print_summary()
        
        return self.results
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*60)
        print("RESUMO DOS TESTES CRÍTICOS")
        print("="*60)
        
        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'PASS'])
        failed = len([r for r in self.results if r['status'] == 'FAIL'])
        skipped = len([r for r in self.results if r['status'] == 'SKIP'])
        critical_failures = len([r for r in self.results if r['status'] == 'FAIL' and r['critical']])
        
        print(f"Total de testes: {total}")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {failed}")
        print(f"⚠️ Pulado: {skipped}")
        print(f"🚨 Falhas críticas: {critical_failures}")
        
        if critical_failures > 0:
            print(f"\n🚨 FALHAS CRÍTICAS ENCONTRADAS:")
            for result in self.results:
                if result['status'] == 'FAIL' and result['critical']:
                    print(f"  - {result['test']}: {result['details']}")
        
        # Status geral
        if critical_failures > 0:
            print(f"\n🚨 STATUS: PROBLEMAS CRÍTICOS CONFIRMADOS")
            print("   Recomendação: Corrigir antes de usar sistema")
        elif failed > 0:
            print(f"\n⚠️ STATUS: PROBLEMAS NÃO-CRÍTICOS ENCONTRADOS")
            print("   Recomendação: Corrigir para melhor funcionamento")
        else:
            print(f"\n✅ STATUS: TODOS OS TESTES CRÍTICOS PASSARAM")
            print("   Recomendação: Sistema pronto para uso")
        
        # Salvar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"critical_issues_test_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Resultados salvos em: {report_file}")

def main():
    """Função principal"""
    tester = CriticalIssuesTester()
    results = tester.run_all_tests()
    
    # Código de saída baseado nos resultados
    critical_failures = len([r for r in results if r['status'] == 'FAIL' and r['critical']])
    total_failures = len([r for r in results if r['status'] == 'FAIL'])
    
    if critical_failures > 0:
        return 2  # Problemas críticos
    elif total_failures > 0:
        return 1  # Problemas não-críticos
    else:
        return 0  # Sucesso

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)