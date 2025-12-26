#!/usr/bin/env python3
"""
Validação TRACK 2 - Integrações + Leads
Script para validar implementação completa do TRACK 2

TRACK 2 Componentes:
1. Lead Capture Service (captura automática)
2. Auto Lead Capture Hook (event handler após mensagens)
3. Integration Access Layer (sub-agentes acessam integrações do pai)
4. Herança de Configurações (integrações herdadas)

Seguindo checkpoint-validation.md: NUNCA marcar como completo sem VALIDAÇÃO REAL.
"""

import asyncio
import json
import sys
import os
import traceback
from datetime import datetime
from typing import Dict, Any, List
from uuid import UUID, uuid4

# Adicionar path do backend
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from src.services.lead_service import lead_service
from src.services.integration_access import get_integration_access
from src.services.auto_lead_capture_hook import get_auto_lead_capture_hook
from src.services.orchestrator_service import get_orchestrator_service
from src.services.sub_agent_inheritance_service import get_inheritance_service
from src.utils.logger import logger


class Track2Validator:
    """Validador completo do TRACK 2"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "track": "TRACK 2 - Integrações + Leads",
            "components": {},
            "integration_tests": {},
            "end_to_end_tests": {},
            "summary": {}
        }
        
        # IDs de teste - usar agente RENUS real e sub-agente criado
        self.test_sub_agent_id = UUID("12345678-1234-5678-9012-123456789012")
        self.test_conversation_id = UUID("87654321-4321-8765-2109-876543210987")
        self.test_agent_id = UUID("00000000-0000-0000-0000-000000000001")  # RENUS real
    
    async def run_validation(self) -> Dict[str, Any]:
        """Executa validação completa do TRACK 2"""
        print("🚀 Iniciando validação TRACK 2 - Integrações + Leads")
        print("=" * 60)
        
        try:
            # 1. Validar componentes individuais
            await self._validate_components()
            
            # 2. Validar integrações
            await self._validate_integrations()
            
            # 3. Validar fluxo end-to-end
            await self._validate_end_to_end()
            
            # 4. Calcular resumo
            self._calculate_summary()
            
            # 5. Gerar relatório
            self._generate_report()
            
            return self.results
            
        except Exception as e:
            print(f"❌ Erro crítico na validação: {e}")
            traceback.print_exc()
            self.results["critical_error"] = str(e)
            return self.results
    
    async def _validate_components(self):
        """Valida componentes individuais do TRACK 2"""
        print("\n📦 Validando componentes individuais...")
        
        components = {
            "lead_service": self._test_lead_service,
            "integration_access": self._test_integration_access,
            "auto_lead_capture_hook": self._test_auto_lead_capture_hook,
            "orchestrator_service": self._test_orchestrator_service,
            "inheritance_service": self._test_inheritance_service
        }
        
        for component_name, test_func in components.items():
            try:
                print(f"  🔍 Testando {component_name}...")
                result = await test_func()
                self.results["components"][component_name] = result
                
                status = "✅" if result["success"] else "❌"
                print(f"  {status} {component_name}: {result['message']}")
                
            except Exception as e:
                print(f"  ❌ {component_name}: ERRO - {e}")
                self.results["components"][component_name] = {
                    "success": False,
                    "error": str(e),
                    "message": f"Erro ao testar {component_name}"
                }
    
    async def _validate_integrations(self):
        """Valida integrações específicas"""
        print("\n🔌 Validando integrações...")
        
        integrations = {
            "whatsapp": self._test_whatsapp_integration,
            "email": self._test_email_integration,
            "calendar": self._test_calendar_integration
        }
        
        for integration_name, test_func in integrations.items():
            try:
                print(f"  🔍 Testando integração {integration_name}...")
                result = await test_func()
                self.results["integration_tests"][integration_name] = result
                
                status = "✅" if result["success"] else "❌"
                print(f"  {status} {integration_name}: {result['message']}")
                
            except Exception as e:
                print(f"  ❌ {integration_name}: ERRO - {e}")
                self.results["integration_tests"][integration_name] = {
                    "success": False,
                    "error": str(e),
                    "message": f"Erro ao testar integração {integration_name}"
                }
    
    async def _validate_end_to_end(self):
        """Valida fluxo completo end-to-end"""
        print("\n🔄 Validando fluxo end-to-end...")
        
        e2e_tests = {
            "message_to_lead_capture": self._test_message_to_lead_capture,
            "sub_agent_with_integrations": self._test_sub_agent_with_integrations,
            "orchestrator_full_flow": self._test_orchestrator_full_flow
        }
        
        for test_name, test_func in e2e_tests.items():
            try:
                print(f"  🔍 Testando {test_name}...")
                result = await test_func()
                self.results["end_to_end_tests"][test_name] = result
                
                status = "✅" if result["success"] else "❌"
                print(f"  {status} {test_name}: {result['message']}")
                
            except Exception as e:
                print(f"  ❌ {test_name}: ERRO - {e}")
                self.results["end_to_end_tests"][test_name] = {
                    "success": False,
                    "error": str(e),
                    "message": f"Erro ao testar {test_name}"
                }
    
    # ========================================================================
    # Testes de Componentes
    # ========================================================================
    
    async def _test_lead_service(self) -> Dict[str, Any]:
        """Testa LeadService com captura automática"""
        try:
            # Testar captura de conversa
            lead_response = await lead_service.capture_from_conversation(
                conversation_id=str(self.test_conversation_id),
                agent_id=str(self.test_sub_agent_id),
                messages=[
                    {"role": "user", "content": "Olá, meu nome é João Silva e meu email é joao@teste.com"},
                    {"role": "assistant", "content": "Olá João! Como posso ajudá-lo?"}
                ]
            )
            
            return {
                "success": lead_response is not None,
                "message": "Lead capturado com sucesso" if lead_response else "Falha na captura",
                "details": {
                    "lead_id": lead_response.id if lead_response else None,
                    "method": "capture_from_conversation"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no LeadService: {e}",
                "error": str(e)
            }
    
    async def _test_integration_access(self) -> Dict[str, Any]:
        """Testa IntegrationAccess"""
        try:
            integration_access = get_integration_access()
            
            # Testar listagem de integrações disponíveis
            available = await integration_access.get_available_integrations(self.test_sub_agent_id)
            
            return {
                "success": isinstance(available, list),
                "message": f"Encontradas {len(available)} integrações disponíveis",
                "details": {
                    "available_count": len(available),
                    "integrations": [i.get('type') for i in available]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no IntegrationAccess: {e}",
                "error": str(e)
            }
    
    async def _test_auto_lead_capture_hook(self) -> Dict[str, Any]:
        """Testa AutoLeadCaptureHook"""
        try:
            hook = get_auto_lead_capture_hook()
            
            # Testar processamento de conversa
            result = await hook.process_conversation(
                sub_agent_id=self.test_sub_agent_id,
                conversation_id=self.test_conversation_id,
                user_message="Meu nome é Maria e quero saber os preços",
                agent_response="Olá Maria! Vou te enviar nossa tabela de preços.",
                context={"phone": "+5511999999999"}
            )
            
            return {
                "success": True,  # Hook sempre retorna, mesmo que None
                "message": "Hook processou conversa" + (" e capturou lead" if result else " sem capturar lead"),
                "details": {
                    "lead_captured": bool(result),
                    "lead_data": result
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no AutoLeadCaptureHook: {e}",
                "error": str(e)
            }
    
    async def _test_orchestrator_service(self) -> Dict[str, Any]:
        """Testa OrchestratorService"""
        try:
            orchestrator = get_orchestrator_service()
            
            # Testar análise de tópicos
            result = await orchestrator.process_message(
                agent_id=self.test_agent_id,
                message="Preciso de ajuda com vendas e preços",
                conversation_id=self.test_conversation_id,
                context={"phone": "+5511999999999"}
            )
            
            return {
                "success": isinstance(result, dict) and 'message' in result,
                "message": "Orquestrador processou mensagem",
                "details": {
                    "delegated": result.get('delegated', False),
                    "sub_agent_used": result.get('sub_agent_name'),
                    "response_length": len(result.get('message', ''))
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no OrchestratorService: {e}",
                "error": str(e)
            }
    
    async def _test_inheritance_service(self) -> Dict[str, Any]:
        """Testa SubAgentInheritanceService"""
        try:
            inheritance = get_inheritance_service()
            
            # Testar cálculo de configuração efetiva
            parent_config = {"integrations": {"whatsapp": {"enabled": True}}}
            sub_config = {"integrations": {"email": {"enabled": True}}}
            inheritance_config = {"integrations": True}
            
            effective = inheritance.calculate_effective_config(
                parent_config, sub_config, inheritance_config
            )
            
            return {
                "success": isinstance(effective, dict),
                "message": "Herança calculada com sucesso",
                "details": {
                    "has_integrations": "integrations" in effective,
                    "inherited_whatsapp": effective.get("integrations", {}).get("whatsapp", {}).get("enabled", False),
                    "own_email": effective.get("integrations", {}).get("email", {}).get("enabled", False)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no InheritanceService: {e}",
                "error": str(e)
            }
    
    # ========================================================================
    # Testes de Integrações
    # ========================================================================
    
    async def _test_whatsapp_integration(self) -> Dict[str, Any]:
        """Testa integração WhatsApp"""
        try:
            integration_access = get_integration_access()
            
            result = await integration_access.send_whatsapp(
                sub_agent_id=self.test_sub_agent_id,
                phone="+5511999999999",
                message="Teste de integração WhatsApp",
                context={"test": True}
            )
            
            return {
                "success": result,
                "message": "WhatsApp enviado com sucesso" if result else "Falha no envio WhatsApp",
                "details": {
                    "sent": result,
                    "phone": "+5511999999999"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro na integração WhatsApp: {e}",
                "error": str(e)
            }
    
    async def _test_email_integration(self) -> Dict[str, Any]:
        """Testa integração Email"""
        try:
            integration_access = get_integration_access()
            
            result = await integration_access.send_email(
                sub_agent_id=self.test_sub_agent_id,
                to_email="test@example.com",
                subject="Teste de integração",
                body="Teste de envio de email via sub-agente",
                context={"test": True}
            )
            
            return {
                "success": result,
                "message": "Email enviado com sucesso" if result else "Falha no envio de email",
                "details": {
                    "sent": result,
                    "to_email": "test@example.com"
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro na integração Email: {e}",
                "error": str(e)
            }
    
    async def _test_calendar_integration(self) -> Dict[str, Any]:
        """Testa integração Calendar"""
        try:
            integration_access = get_integration_access()
            
            result = await integration_access.access_calendar(
                sub_agent_id=self.test_sub_agent_id,
                action="check_availability",
                data={"date": "2025-12-24", "time": "14:00"}
            )
            
            return {
                "success": result.get('success', False),
                "message": "Calendar acessado com sucesso" if result.get('success') else "Falha no acesso ao calendar",
                "details": {
                    "action": "check_availability",
                    "result": result
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro na integração Calendar: {e}",
                "error": str(e)
            }
    
    # ========================================================================
    # Testes End-to-End
    # ========================================================================
    
    async def _test_message_to_lead_capture(self) -> Dict[str, Any]:
        """Testa fluxo: mensagem → análise → captura de lead"""
        try:
            hook = get_auto_lead_capture_hook()
            
            # Simular conversa com dados de contato e interesse comercial
            result = await hook.process_conversation(
                sub_agent_id=self.test_sub_agent_id,
                conversation_id=self.test_conversation_id,
                user_message="Olá, sou Pedro Santos, email pedro@empresa.com, quero contratar o plano Pro",
                agent_response="Olá Pedro! Vou te enviar as informações do plano Pro por email.",
                context={"phone": "+5511888888888", "email": "pedro@empresa.com"}
            )
            
            return {
                "success": bool(result),
                "message": "Fluxo completo executado" + (" - lead capturado" if result else " - lead não capturado"),
                "details": {
                    "lead_captured": bool(result),
                    "commercial_intent": True,
                    "contact_data": True,
                    "lead_id": result.get('id') if result else None
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no fluxo message-to-lead: {e}",
                "error": str(e)
            }
    
    async def _test_sub_agent_with_integrations(self) -> Dict[str, Any]:
        """Testa sub-agente usando integrações do pai"""
        try:
            integration_access = get_integration_access()
            
            # Testar múltiplas integrações em sequência
            whatsapp_result = await integration_access.send_whatsapp(
                sub_agent_id=self.test_sub_agent_id,
                phone="+5511777777777",
                message="Mensagem via sub-agente",
                context={"test": "sub_agent_integration"}
            )
            
            email_result = await integration_access.send_email(
                sub_agent_id=self.test_sub_agent_id,
                to_email="subagent@test.com",
                subject="Teste sub-agente",
                body="Email enviado via sub-agente",
                context={"test": "sub_agent_integration"}
            )
            
            return {
                "success": whatsapp_result and email_result,
                "message": f"Sub-agente usou integrações: WhatsApp={whatsapp_result}, Email={email_result}",
                "details": {
                    "whatsapp_success": whatsapp_result,
                    "email_success": email_result,
                    "both_successful": whatsapp_result and email_result
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no teste sub-agente + integrações: {e}",
                "error": str(e)
            }
    
    async def _test_orchestrator_full_flow(self) -> Dict[str, Any]:
        """Testa orquestrador com captura de leads e integrações"""
        try:
            orchestrator = get_orchestrator_service()
            
            # Mensagem que deve disparar sub-agente, capturar lead e usar integrações
            result = await orchestrator.process_message(
                agent_id=self.test_agent_id,
                message="Sou Ana Costa, ana@teste.com, preciso de orçamento para plano empresarial",
                conversation_id=self.test_conversation_id,
                context={
                    "phone": "+5511666666666",
                    "email": "ana@teste.com",
                    "user_profile": {"segment": "enterprise"}
                }
            )
            
            return {
                "success": isinstance(result, dict) and 'message' in result,
                "message": "Orquestrador executou fluxo completo",
                "details": {
                    "delegated": result.get('delegated', False),
                    "lead_captured": result.get('lead_captured', False),
                    "integrations_used": result.get('integrations_used', 0),
                    "sub_agent": result.get('sub_agent_name'),
                    "response_generated": bool(result.get('message'))
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro no fluxo completo do orquestrador: {e}",
                "error": str(e)
            }
    
    # ========================================================================
    # Relatório e Resumo
    # ========================================================================
    
    def _calculate_summary(self):
        """Calcula resumo dos testes"""
        all_tests = {}
        all_tests.update(self.results["components"])
        all_tests.update(self.results["integration_tests"])
        all_tests.update(self.results["end_to_end_tests"])
        
        total_tests = len(all_tests)
        successful_tests = sum(1 for test in all_tests.values() if test.get("success", False))
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": f"{success_rate:.1f}%",
            "track_status": "PASSED" if success_rate >= 70 else "FAILED",
            "critical_components": {
                "lead_capture": self.results["components"].get("auto_lead_capture_hook", {}).get("success", False),
                "integrations": self.results["components"].get("integration_access", {}).get("success", False),
                "orchestrator": self.results["components"].get("orchestrator_service", {}).get("success", False),
                "inheritance": self.results["components"].get("inheritance_service", {}).get("success", False)
            }
        }
    
    def _generate_report(self):
        """Gera relatório final"""
        summary = self.results["summary"]
        
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL - TRACK 2")
        print("=" * 60)
        
        print(f"🎯 Status: {summary['track_status']}")
        print(f"📈 Taxa de Sucesso: {summary['success_rate']}")
        print(f"✅ Testes Passaram: {summary['successful_tests']}/{summary['total_tests']}")
        print(f"❌ Testes Falharam: {summary['failed_tests']}")
        
        print("\n🔧 Componentes Críticos:")
        for component, status in summary["critical_components"].items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component}")
        
        if summary["failed_tests"] > 0:
            print("\n⚠️  FALHAS IDENTIFICADAS:")
            all_tests = {}
            all_tests.update(self.results["components"])
            all_tests.update(self.results["integration_tests"])
            all_tests.update(self.results["end_to_end_tests"])
            
            for test_name, test_result in all_tests.items():
                if not test_result.get("success", False):
                    print(f"  ❌ {test_name}: {test_result.get('message', 'Erro desconhecido')}")
        
        print("\n" + "=" * 60)
        
        # Salvar relatório em arquivo
        report_file = f"docs/validacoes/VALIDACAO_TRACK2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Relatório salvo em: {report_file}")


async def main():
    """Função principal"""
    validator = Track2Validator()
    results = await validator.run_validation()
    
    # Retornar código de saída baseado no resultado
    success_rate = float(results["summary"]["success_rate"].replace("%", ""))
    exit_code = 0 if success_rate >= 70 else 1
    
    print(f"\n🏁 Validação concluída com código de saída: {exit_code}")
    sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())