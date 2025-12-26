#!/usr/bin/env python3
"""
SMOKE TEST COMPLETO DO SISTEMA RENUM
====================================

Este script testa os fluxos críticos de negócio identificados:
1. Criação de sub-agentes (bloqueio identificado)
2. Memória de conversas do RENUS
3. Integrações funcionais vs implementadas
4. Delegação RENUS → Sub-agentes
5. Sistema de entrevistas

Executa testes reais contra Supabase e APIs.
"""

import os
import sys
import asyncio
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

# Adicionar path do backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

try:
    from config.supabase import supabase_admin
    from services.subagent_service import SubAgentService
    from services.integration_service import IntegrationService
    print("✅ Imports do backend carregados com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar backend: {e}")
    print("⚠️ Continuando apenas com testes de API externa...")
    supabase_admin = None

class SmokeTestResult:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []
        self.warnings = []
        self.critical_issues = []
    
    def add_test(self, name: str, passed: bool, details: str = "", critical: bool = False):
        self.tests_run += 1
        if passed:
            self.tests_passed += 1
            print(f"✅ {name}: {details}")
        else:
            self.tests_failed += 1
            print(f"❌ {name}: {details}")
            self.failures.append(f"{name}: {details}")
            if critical:
                self.critical_issues.append(f"{name}: {details}")
    
    def add_warning(self, message: str):
        self.warnings.append(message)
        print(f"⚠️ {message}")
    
    def print_summary(self):
        print("\n" + "="*60)
        print("RESUMO DO SMOKE TEST")
        print("="*60)
        print(f"Total de testes: {self.tests_run}")
        print(f"✅ Passou: {self.tests_passed}")
        print(f"❌ Falhou: {self.tests_failed}")
        print(f"⚠️ Avisos: {len(self.warnings)}")
        print(f"🚨 Críticos: {len(self.critical_issues)}")
        
        if self.critical_issues:
            print("\n🚨 PROBLEMAS CRÍTICOS (BLOQUEIAM NEGÓCIO):")
            for issue in self.critical_issues:
                print(f"  - {issue}")
        
        if self.failures:
            print("\n❌ FALHAS ENCONTRADAS:")
            for failure in self.failures:
                print(f"  - {failure}")
        
        if self.warnings:
            print("\n⚠️ AVISOS:")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        # Determinar status geral
        if self.critical_issues:
            print(f"\n🚨 STATUS GERAL: SISTEMA COM PROBLEMAS CRÍTICOS")
            print("   Recomendação: Corrigir problemas críticos antes de usar em produção")
        elif self.tests_failed > 0:
            print(f"\n⚠️ STATUS GERAL: SISTEMA PARCIALMENTE FUNCIONAL")
            print("   Recomendação: Corrigir falhas não-críticas")
        else:
            print(f"\n✅ STATUS GERAL: SISTEMA FUNCIONANDO")
            print("   Recomendação: Pronto para uso")

class SystemSmokeTest:
    def __init__(self):
        self.result = SmokeTestResult()
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:5173"
        
    async def run_all_tests(self):
        """Executa todos os testes de smoke"""
        print("🚀 INICIANDO SMOKE TEST COMPLETO DO SISTEMA RENUM")
        print(f"⏰ Timestamp: {datetime.now().isoformat()}")
        print("="*60)
        
        # 1. Testes de Conectividade
        await self.test_connectivity()
        
        # 2. Testes de Banco de Dados
        await self.test_database_health()
        
        # 3. Testes de Sub-Agentes (PROBLEMA CRÍTICO IDENTIFICADO)
        await self.test_subagent_system()
        
        # 4. Testes de Integrações
        await self.test_integrations_system()
        
        # 5. Testes de Memória de Conversas
        await self.test_conversation_memory()
        
        # 6. Testes de Fluxo de Negócio
        await self.test_business_flows()
        
        # 7. Relatório Final
        self.result.print_summary()
        
        return self.result
    
    async def test_connectivity(self):
        """Testa conectividade básica"""
        print("\n📡 TESTANDO CONECTIVIDADE...")
        
        # Backend
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                self.result.add_test("Backend Health Check", True, f"Status: {response.status_code}")
            else:
                self.result.add_test("Backend Health Check", False, f"Status: {response.status_code}", critical=True)
        except Exception as e:
            self.result.add_test("Backend Health Check", False, f"Erro: {e}", critical=True)
        
        # Frontend (se estiver rodando)
        try:
            response = requests.get(self.frontend_url, timeout=5)
            self.result.add_test("Frontend Accessibility", True, f"Status: {response.status_code}")
        except Exception as e:
            self.result.add_test("Frontend Accessibility", False, f"Erro: {e}")
        
        # Supabase
        if supabase_admin:
            try:
                response = supabase_admin.table('profiles').select('id').limit(1).execute()
                self.result.add_test("Supabase Connection", True, f"Conectado, {len(response.data)} registros")
            except Exception as e:
                self.result.add_test("Supabase Connection", False, f"Erro: {e}", critical=True)
    
    async def test_database_health(self):
        """Testa saúde do banco de dados"""
        print("\n🗄️ TESTANDO BANCO DE DADOS...")
        
        if not supabase_admin:
            self.result.add_warning("Supabase não disponível - pulando testes de banco")
            return
        
        # Tabelas críticas
        critical_tables = [
            'profiles', 'clients', 'leads', 'interviews', 'interview_messages',
            'sub_agents', 'agent_integrations', 'conversations', 'messages'
        ]
        
        for table in critical_tables:
            try:
                response = supabase_admin.table(table).select('id').limit(1).execute()
                self.result.add_test(f"Tabela {table}", True, f"Existe e acessível")
            except Exception as e:
                self.result.add_test(f"Tabela {table}", False, f"Erro: {e}", critical=True)
        
        # Teste de RLS
        try:
            # Tentar acessar sem autenticação (deve falhar)
            from supabase import create_client
            supabase_anon = create_client(
                os.getenv('SUPABASE_URL', ''),
                os.getenv('SUPABASE_ANON_KEY', '')
            )
            response = supabase_anon.table('clients').select('*').execute()
            # Se chegou aqui, RLS pode estar desabilitado
            if response.data:
                self.result.add_test("RLS Security", False, "RLS pode estar desabilitado - dados vazaram", critical=True)
            else:
                self.result.add_test("RLS Security", True, "RLS bloqueou acesso não autorizado")
        except Exception as e:
            self.result.add_test("RLS Security", True, f"RLS funcionando - acesso negado: {str(e)[:100]}")
    
    async def test_subagent_system(self):
        """Testa sistema de sub-agentes (PROBLEMA CRÍTICO IDENTIFICADO)"""
        print("\n🤖 TESTANDO SISTEMA DE SUB-AGENTES...")
        
        # Teste 1: Listar sub-agentes existentes
        try:
            if supabase_admin:
                response = supabase_admin.table('sub_agents').select('*').execute()
                count = len(response.data) if response.data else 0
                self.result.add_test("Listar Sub-Agentes", True, f"{count} sub-agentes encontrados")
                
                if count == 0:
                    self.result.add_warning("Nenhum sub-agente encontrado - sistema pode estar vazio")
            else:
                self.result.add_warning("Não foi possível testar listagem de sub-agentes")
        except Exception as e:
            self.result.add_test("Listar Sub-Agentes", False, f"Erro: {e}")
        
        # Teste 2: Tentar criar sub-agente via API
        try:
            # Primeiro, buscar um agente pai (RENUS)
            if supabase_admin:
                agents_response = supabase_admin.table('agents').select('id').eq('slug', 'renus').execute()
                if agents_response.data:
                    agent_id = agents_response.data[0]['id']
                    
                    # Tentar criar sub-agente via API
                    test_subagent = {
                        "name": "Teste Entrevista",
                        "description": "Sub-agente de teste para entrevistas",
                        "role": "sub_agent",
                        "status": "active",
                        "config": {
                            "channel": "whatsapp",
                            "model": "gpt-4o-mini",
                            "topics": ["entrevistas", "pesquisas"],
                            "identity": {
                                "system_prompt": "Você é um especialista em conduzir entrevistas e pesquisas."
                            }
                        }
                    }
                    
                    response = requests.post(
                        f"{self.backend_url}/api/agents/{agent_id}/sub-agents",
                        json=test_subagent,
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201]:
                        self.result.add_test("Criar Sub-Agente via API", True, f"Status: {response.status_code}")
                        # Limpar teste
                        try:
                            created_data = response.json()
                            if 'id' in created_data:
                                requests.delete(f"{self.backend_url}/api/agents/{agent_id}/sub-agents/{created_data['id']}")
                        except:
                            pass
                    else:
                        self.result.add_test("Criar Sub-Agente via API", False, 
                                           f"Status: {response.status_code}, Erro: {response.text[:200]}", 
                                           critical=True)
                else:
                    self.result.add_test("Criar Sub-Agente via API", False, "Agente RENUS não encontrado", critical=True)
        except Exception as e:
            self.result.add_test("Criar Sub-Agente via API", False, f"Erro: {e}", critical=True)
        
        # Teste 3: Verificar endpoints de sub-agentes
        try:
            response = requests.get(f"{self.backend_url}/docs", timeout=5)
            if response.status_code == 200:
                docs_content = response.text
                if "/api/agents/{agent_id}/sub-agents" in docs_content:
                    self.result.add_test("Endpoints Sub-Agentes", True, "Endpoints documentados no Swagger")
                else:
                    self.result.add_test("Endpoints Sub-Agentes", False, "Endpoints não encontrados na documentação")
            else:
                self.result.add_warning("Não foi possível verificar documentação da API")
        except Exception as e:
            self.result.add_warning(f"Erro ao verificar documentação: {e}")
    
    async def test_integrations_system(self):
        """Testa sistema de integrações"""
        print("\n🔌 TESTANDO SISTEMA DE INTEGRAÇÕES...")
        
        # Teste 1: Listar integrações
        try:
            if supabase_admin:
                response = supabase_admin.table('agent_integrations').select('*').execute()
                count = len(response.data) if response.data else 0
                self.result.add_test("Listar Integrações", True, f"{count} integrações encontradas")
                
                # Verificar tipos de integrações
                if response.data:
                    providers = set(item['provider'] for item in response.data)
                    self.result.add_test("Tipos de Integrações", True, f"Providers: {', '.join(providers)}")
                else:
                    self.result.add_warning("Nenhuma integração configurada")
        except Exception as e:
            self.result.add_test("Listar Integrações", False, f"Erro: {e}")
        
        # Teste 2: Testar integrações específicas
        integration_tests = [
            ("WhatsApp/Uazapi", self.test_whatsapp_integration),
            ("Chatwoot", self.test_chatwoot_integration),
            ("Google", self.test_google_integration),
            ("Supabase Externo", self.test_external_supabase_integration)
        ]
        
        for name, test_func in integration_tests:
            try:
                await test_func()
            except Exception as e:
                self.result.add_test(f"Integração {name}", False, f"Erro no teste: {e}")
    
    async def test_whatsapp_integration(self):
        """Testa integração WhatsApp"""
        # Verificar se há configuração
        if supabase_admin:
            response = supabase_admin.table('agent_integrations')\
                .select('*')\
                .eq('provider', 'uazapi')\
                .execute()
            
            if response.data:
                config = response.data[0]['config']
                if config.get('token') and config.get('url'):
                    self.result.add_test("WhatsApp Config", True, "Configuração encontrada")
                    
                    # Teste básico de conectividade (sem enviar mensagem real)
                    try:
                        # Apenas verificar se a URL responde
                        test_url = config['url']
                        response = requests.get(test_url, timeout=5)
                        self.result.add_test("WhatsApp Connectivity", True, f"URL acessível: {response.status_code}")
                    except Exception as e:
                        self.result.add_test("WhatsApp Connectivity", False, f"URL inacessível: {e}")
                else:
                    self.result.add_test("WhatsApp Config", False, "Configuração incompleta")
            else:
                self.result.add_test("WhatsApp Config", False, "Não configurado")
    
    async def test_chatwoot_integration(self):
        """Testa integração Chatwoot"""
        if supabase_admin:
            response = supabase_admin.table('agent_integrations')\
                .select('*')\
                .eq('provider', 'chatwoot')\
                .execute()
            
            if response.data:
                self.result.add_test("Chatwoot Config", True, "Configuração encontrada")
            else:
                self.result.add_test("Chatwoot Config", False, "Não configurado")
    
    async def test_google_integration(self):
        """Testa integração Google"""
        if supabase_admin:
            response = supabase_admin.table('agent_integrations')\
                .select('*')\
                .eq('provider', 'google')\
                .execute()
            
            if response.data:
                self.result.add_test("Google Config", True, "Configuração encontrada")
            else:
                self.result.add_test("Google Config", False, "Não configurado")
    
    async def test_external_supabase_integration(self):
        """Testa integração Supabase Externo"""
        if supabase_admin:
            response = supabase_admin.table('agent_integrations')\
                .select('*')\
                .eq('provider', 'supabase_external')\
                .execute()
            
            if response.data:
                self.result.add_test("Supabase Externo Config", True, "Configuração encontrada")
            else:
                self.result.add_test("Supabase Externo Config", False, "Não configurado")
    
    async def test_conversation_memory(self):
        """Testa memória de conversas (PROBLEMA IDENTIFICADO)"""
        print("\n🧠 TESTANDO MEMÓRIA DE CONVERSAS...")
        
        # Teste 1: Verificar estrutura de conversas
        if supabase_admin:
            try:
                # Verificar tabela conversations
                conversations = supabase_admin.table('conversations').select('*').limit(5).execute()
                conv_count = len(conversations.data) if conversations.data else 0
                self.result.add_test("Tabela Conversations", True, f"{conv_count} conversas encontradas")
                
                # Verificar tabela messages
                messages = supabase_admin.table('messages').select('*').limit(5).execute()
                msg_count = len(messages.data) if messages.data else 0
                self.result.add_test("Tabela Messages", True, f"{msg_count} mensagens encontradas")
                
                # Verificar tabela interview_messages
                interview_msgs = supabase_admin.table('interview_messages').select('*').limit(5).execute()
                int_msg_count = len(interview_msgs.data) if interview_msgs.data else 0
                self.result.add_test("Tabela Interview Messages", True, f"{int_msg_count} mensagens de entrevista encontradas")
                
                # Verificar se há conversas com múltiplas mensagens (indicativo de memória)
                if conversations.data:
                    for conv in conversations.data[:3]:  # Testar primeiras 3 conversas
                        conv_messages = supabase_admin.table('messages')\
                            .select('*')\
                            .eq('conversation_id', conv['id'])\
                            .execute()
                        
                        msg_count = len(conv_messages.data) if conv_messages.data else 0
                        if msg_count > 1:
                            self.result.add_test(f"Memória Conversa {conv['id'][:8]}", True, f"{msg_count} mensagens")
                        else:
                            self.result.add_test(f"Memória Conversa {conv['id'][:8]}", False, 
                                               f"Apenas {msg_count} mensagem - possível problema de memória")
                
            except Exception as e:
                self.result.add_test("Estrutura de Conversas", False, f"Erro: {e}")
    
    async def test_business_flows(self):
        """Testa fluxos críticos de negócio"""
        print("\n💼 TESTANDO FLUXOS DE NEGÓCIO...")
        
        # Teste 1: Fluxo de Entrevista
        await self.test_interview_flow()
        
        # Teste 2: Fluxo de Delegação RENUS → Sub-agente
        await self.test_delegation_flow()
        
        # Teste 3: Fluxo de Conversação Geral
        await self.test_general_conversation_flow()
    
    async def test_interview_flow(self):
        """Testa fluxo de entrevistas"""
        if supabase_admin:
            try:
                # Verificar se há entrevistas
                interviews = supabase_admin.table('interviews').select('*').limit(5).execute()
                count = len(interviews.data) if interviews.data else 0
                
                if count > 0:
                    self.result.add_test("Fluxo de Entrevistas", True, f"{count} entrevistas encontradas")
                    
                    # Verificar status das entrevistas
                    statuses = {}
                    for interview in interviews.data:
                        status = interview.get('status', 'unknown')
                        statuses[status] = statuses.get(status, 0) + 1
                    
                    self.result.add_test("Status de Entrevistas", True, f"Status: {statuses}")
                else:
                    self.result.add_warning("Nenhuma entrevista encontrada - sistema pode estar vazio")
                    
            except Exception as e:
                self.result.add_test("Fluxo de Entrevistas", False, f"Erro: {e}")
    
    async def test_delegation_flow(self):
        """Testa fluxo de delegação RENUS → Sub-agente"""
        # Este teste requer lógica mais complexa
        # Por ora, verificamos se a estrutura existe
        if supabase_admin:
            try:
                # Verificar se há agente RENUS
                renus = supabase_admin.table('agents').select('*').eq('slug', 'renus').execute()
                if renus.data:
                    self.result.add_test("Agente RENUS", True, "Encontrado")
                    
                    # Verificar se há sub-agentes associados
                    renus_id = renus.data[0]['id']
                    sub_agents = supabase_admin.table('sub_agents')\
                        .select('*')\
                        .eq('parent_agent_id', renus_id)\
                        .execute()
                    
                    sub_count = len(sub_agents.data) if sub_agents.data else 0
                    if sub_count > 0:
                        self.result.add_test("Delegação RENUS", True, f"{sub_count} sub-agentes disponíveis")
                    else:
                        self.result.add_test("Delegação RENUS", False, 
                                           "Nenhum sub-agente encontrado - delegação impossível", 
                                           critical=True)
                else:
                    self.result.add_test("Agente RENUS", False, "Não encontrado", critical=True)
                    
            except Exception as e:
                self.result.add_test("Fluxo de Delegação", False, f"Erro: {e}")
    
    async def test_general_conversation_flow(self):
        """Testa fluxo de conversação geral"""
        if supabase_admin:
            try:
                # Verificar se há leads
                leads = supabase_admin.table('leads').select('*').limit(5).execute()
                lead_count = len(leads.data) if leads.data else 0
                
                if lead_count > 0:
                    self.result.add_test("Leads Disponíveis", True, f"{lead_count} leads encontrados")
                    
                    # Verificar se leads têm conversas
                    for lead in leads.data[:3]:
                        conversations = supabase_admin.table('conversations')\
                            .select('*')\
                            .eq('lead_id', lead['id'])\
                            .execute()
                        
                        conv_count = len(conversations.data) if conversations.data else 0
                        if conv_count > 0:
                            self.result.add_test(f"Conversas Lead {lead['id'][:8]}", True, f"{conv_count} conversas")
                        else:
                            self.result.add_warning(f"Lead {lead['id'][:8]} sem conversas")
                else:
                    self.result.add_warning("Nenhum lead encontrado - sistema pode estar vazio")
                    
            except Exception as e:
                self.result.add_test("Fluxo de Conversação", False, f"Erro: {e}")

async def main():
    """Função principal"""
    print("🔍 SMOKE TEST SISTEMA RENUM")
    print("Verificando saúde geral do sistema...")
    
    tester = SystemSmokeTest()
    result = await tester.run_all_tests()
    
    # Salvar resultado em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"smoke_test_report_{timestamp}.json"
    
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "tests_run": result.tests_run,
        "tests_passed": result.tests_passed,
        "tests_failed": result.tests_failed,
        "failures": result.failures,
        "warnings": result.warnings,
        "critical_issues": result.critical_issues
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório salvo em: {report_file}")
    
    # Retornar código de saída baseado no resultado
    if result.critical_issues:
        print("\n🚨 SAINDO COM CÓDIGO 2 (PROBLEMAS CRÍTICOS)")
        return 2
    elif result.tests_failed > 0:
        print("\n⚠️ SAINDO COM CÓDIGO 1 (PROBLEMAS NÃO-CRÍTICOS)")
        return 1
    else:
        print("\n✅ SAINDO COM CÓDIGO 0 (SUCESSO)")
        return 0

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)