#!/usr/bin/env python3
"""
Script de Validação do Orquestrador Multi-Agente
Testa toda a implementação do sistema de roteamento de sub-agentes
"""

import asyncio
import json
import sys
import os
import requests
import time
from typing import Dict, Any, List
from datetime import datetime

# Adicionar path do backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Carregar variáveis de ambiente do .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

class OrchestratorValidator:
    """Validador completo do sistema de orquestração"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.errors = []
        
    def log_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Registra resultado de um teste"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if not success:
            self.errors.append(f"{test_name}: {details}")
    
    def test_backend_health(self) -> bool:
        """Testa se o backend está rodando"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            success = response.status_code == 200
            
            self.log_result(
                "Backend Health Check",
                success,
                f"Status: {response.status_code}" if success else f"Failed: {response.status_code}",
                response.json() if success else None
            )
            return success
            
        except requests.exceptions.ConnectionError:
            self.log_result(
                "Backend Health Check",
                False,
                "Connection refused - Backend não está rodando"
            )
            return False
        except Exception as e:
            self.log_result(
                "Backend Health Check",
                False,
                f"Erro inesperado: {str(e)}"
            )
            return False
    
    def test_orchestrator_analyze_endpoint(self) -> bool:
        """Testa endpoint de análise de mensagens"""
        try:
            test_data = {
                "message": "Gostaria de saber sobre os preços dos planos",
                "context": {
                    "user_id": "test_user",
                    "channel": "whatsapp"
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/orchestrator/analyze",
                json=test_data,
                timeout=10
            )
            
            success = response.status_code == 200
            response_data = response.json() if success else None
            
            details = ""
            if success:
                topics = response_data.get("topics", [])
                confidence = response_data.get("confidence", 0)
                details = f"Topics: {topics}, Confidence: {confidence}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_result(
                "Orchestrator Analyze Endpoint",
                success,
                details,
                response_data
            )
            return success
            
        except Exception as e:
            self.log_result(
                "Orchestrator Analyze Endpoint",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_orchestrator_route_endpoint(self) -> bool:
        """Testa endpoint de roteamento"""
        try:
            test_data = {
                "message": "Preciso de ajuda com vendas e preços",
                "agent_id": "test-agent-id",
                "context": {
                    "user_profile": {"segment": "B2B"},
                    "conversation_history": []
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/orchestrator/route",
                json=test_data,
                timeout=15
            )
            
            success = response.status_code == 200
            response_data = response.json() if success else None
            
            details = ""
            if success:
                should_route = response_data.get("should_route", False)
                selected_agent = response_data.get("selected_subagent")
                reason = response_data.get("routing_reason", "")
                details = f"Route: {should_route}, Agent: {selected_agent}, Reason: {reason}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_result(
                "Orchestrator Route Endpoint",
                success,
                details,
                response_data
            )
            return success
            
        except Exception as e:
            self.log_result(
                "Orchestrator Route Endpoint",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_openrouter_integration(self) -> bool:
        """Testa integração com OpenRouter (se configurado)"""
        try:
            # Importar e testar OpenRouter client
            from src.utils.openrouter_client import OpenRouterClient
            
            client = OpenRouterClient()
            
            # Teste simples de análise
            test_message = "Quero comprar um produto"
            result = client.analyze_message(test_message)
            
            success = isinstance(result, dict) and "topics" in result
            
            details = ""
            if success:
                topics = result.get("topics", [])
                confidence = result.get("confidence", 0)
                details = f"Topics: {topics}, Confidence: {confidence}"
            else:
                details = "OpenRouter não retornou formato esperado"
            
            self.log_result(
                "OpenRouter Integration",
                success,
                details,
                result if success else None
            )
            return success
            
        except ImportError as e:
            self.log_result(
                "OpenRouter Integration",
                False,
                f"Erro de import: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "OpenRouter Integration",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_lead_creation_service(self) -> bool:
        """Testa criação de leads via serviço"""
        try:
            # Importar e testar LeadService
            from src.services.lead_service import lead_service
            
            # Teste de criação de lead
            test_phone = "+5511999999999"
            test_name = "Lead Teste Orquestrador"
            
            # Usar asyncio para chamar método async
            async def create_test_lead():
                return await lead_service.create_from_conversation(
                    phone=test_phone,
                    name=test_name,
                    source="orchestrator_test",
                    metadata={"test": True, "timestamp": datetime.now().isoformat()}
                )
            
            lead = asyncio.run(create_test_lead())
            
            success = lead is not None and hasattr(lead, 'id')
            
            details = ""
            if success:
                details = f"Lead criado: ID={lead.id}, Phone={lead.phone}"
            else:
                details = "Falha ao criar lead"
            
            self.log_result(
                "Lead Creation Service",
                success,
                details,
                {"lead_id": str(lead.id)} if success else None
            )
            return success
            
        except ImportError as e:
            self.log_result(
                "Lead Creation Service",
                False,
                f"Erro de import: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "Lead Creation Service",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_orchestrator_service_direct(self) -> bool:
        """Testa OrchestratorService diretamente"""
        try:
            from src.services.orchestrator_service import orchestrator_service
            
            # Teste de análise de mensagem
            test_message = "Preciso de suporte técnico urgente"
            
            async def test_analysis():
                return await orchestrator_service.analyze_message(
                    test_message,
                    {"user_id": "test", "channel": "test"}
                )
            
            analysis = asyncio.run(test_analysis())
            
            success = isinstance(analysis, dict) and "topics" in analysis
            
            details = ""
            if success:
                topics = analysis.get("topics", [])
                confidence = analysis.get("confidence", 0)
                details = f"Topics: {topics}, Confidence: {confidence}"
            else:
                details = "Análise não retornou formato esperado"
            
            self.log_result(
                "Orchestrator Service Direct",
                success,
                details,
                analysis if success else None
            )
            return success
            
        except ImportError as e:
            self.log_result(
                "Orchestrator Service Direct",
                False,
                f"Erro de import: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "Orchestrator Service Direct",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def test_public_chat_integration(self) -> bool:
        """Testa integração com public chat"""
        try:
            # Testar endpoint de agentes públicos
            response = requests.get(f"{self.base_url}/api/agents/public", timeout=10)
            
            success = response.status_code == 200
            response_data = response.json() if success else None
            
            details = ""
            if success:
                agents = response_data.get("agents", [])
                details = f"Encontrados {len(agents)} agentes públicos"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_result(
                "Public Chat Integration",
                success,
                details,
                response_data
            )
            return success
            
        except Exception as e:
            self.log_result(
                "Public Chat Integration",
                False,
                f"Erro: {str(e)}"
            )
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Executa todos os testes de validação"""
        print("🔍 INICIANDO VALIDAÇÃO DO ORQUESTRADOR MULTI-AGENTE")
        print("=" * 60)
        
        start_time = time.time()
        
        # Lista de testes a executar
        tests = [
            ("Backend Health", self.test_backend_health),
            ("Orchestrator Analyze", self.test_orchestrator_analyze_endpoint),
            ("Orchestrator Route", self.test_orchestrator_route_endpoint),
            ("OpenRouter Integration", self.test_openrouter_integration),
            ("Lead Creation", self.test_lead_creation_service),
            ("Orchestrator Service", self.test_orchestrator_service_direct),
            ("Public Chat", self.test_public_chat_integration),
        ]
        
        # Executar testes
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_result(test_name, False, f"Erro inesperado: {str(e)}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Resumo final
        print("\n" + "=" * 60)
        print("📊 RESUMO DA VALIDAÇÃO")
        print("=" * 60)
        print(f"✅ Testes Passaram: {passed}/{total}")
        print(f"❌ Testes Falharam: {total - passed}/{total}")
        print(f"⏱️  Tempo Total: {duration:.2f}s")
        
        success_rate = (passed / total) * 100
        print(f"📈 Taxa de Sucesso: {success_rate:.1f}%")
        
        if self.errors:
            print("\n❌ ERROS ENCONTRADOS:")
            for error in self.errors:
                print(f"  - {error}")
        
        # Status final
        if passed == total:
            print("\n🎉 TODOS OS TESTES PASSARAM - ORQUESTRADOR VALIDADO!")
            status = "VALIDADO"
        elif passed >= total * 0.8:
            print("\n⚠️  MAIORIA DOS TESTES PASSOU - REVISAR FALHAS")
            status = "PARCIALMENTE_VALIDADO"
        else:
            print("\n🚨 MUITOS TESTES FALHARAM - IMPLEMENTAÇÃO PRECISA CORREÇÃO")
            status = "FALHOU"
        
        return {
            "status": status,
            "passed": passed,
            "total": total,
            "success_rate": success_rate,
            "duration": duration,
            "errors": self.errors,
            "results": self.results,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_report(self, results: Dict[str, Any], filename: str = None):
        """Salva relatório detalhado em JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"validation_report_{timestamp}.json"
        
        filepath = os.path.join("docs", "validacoes", filename)
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: {filepath}")


def main():
    """Função principal"""
    print("🚀 VALIDADOR DO ORQUESTRADOR MULTI-AGENTE")
    print("Versão: 1.0")
    print("Data:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Verificar se backend está configurado
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # Criar validador
    validator = OrchestratorValidator(backend_url)
    
    # Executar validação
    results = validator.run_all_tests()
    
    # Salvar relatório
    validator.save_report(results)
    
    # Exit code baseado no resultado
    if results["status"] == "VALIDADO":
        sys.exit(0)
    elif results["status"] == "PARCIALMENTE_VALIDADO":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()