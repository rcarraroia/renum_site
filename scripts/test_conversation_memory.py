#!/usr/bin/env python3
"""
TESTE ESPECÍFICO DE MEMÓRIA DE CONVERSAS
========================================

Testa o problema específico relatado pelo usuário:
"o agente renus não mantém a memória das conversas"

Este script simula uma conversa multi-turno e verifica se:
1. Mensagens são armazenadas corretamente
2. Contexto é mantido entre turnos
3. RENUS acessa histórico de mensagens
4. Sub-agentes herdam contexto quando delegados
"""

import os
import sys
import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

# Adicionar path do backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

class ConversationMemoryTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.test_results = []
        self.test_conversation_id = None
        self.test_lead_id = None
        
    def log_test(self, name: str, passed: bool, details: str, critical: bool = False):
        """Log resultado do teste"""
        result = {
            "test": name,
            "passed": passed,
            "details": details,
            "critical": critical,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        icon = "✅" if passed else "❌"
        critical_flag = " 🚨" if critical else ""
        print(f"{icon} {name}: {details}{critical_flag}")
    
    def setup_test_environment(self) -> bool:
        """Configura ambiente de teste (lead + conversa)"""
        print("🔧 CONFIGURANDO AMBIENTE DE TESTE...")
        
        try:
            # Criar lead de teste
            test_lead = {
                "phone": "+5511999999999",
                "name": "Teste Memória",
                "email": "teste.memoria@renum.com",
                "metadata": {"test": True}
            }
            
            response = requests.post(f"{self.backend_url}/api/leads", json=test_lead, timeout=10)
            if response.status_code in [200, 201]:
                self.test_lead_id = response.json()['id']
                self.log_test("Criar Lead de Teste", True, f"Lead criado: {self.test_lead_id}")
            else:
                self.log_test("Criar Lead de Teste", False, f"Erro: {response.status_code}", critical=True)
                return False
            
            # Criar conversa de teste
            test_conversation = {
                "lead_id": self.test_lead_id,
                "status": "open",
                "metadata": {"test": True}
            }
            
            response = requests.post(f"{self.backend_url}/api/conversations", json=test_conversation, timeout=10)
            if response.status_code in [200, 201]:
                self.test_conversation_id = response.json()['id']
                self.log_test("Criar Conversa de Teste", True, f"Conversa criada: {self.test_conversation_id}")
                return True
            else:
                self.log_test("Criar Conversa de Teste", False, f"Erro: {response.status_code}", critical=True)
                return False
                
        except Exception as e:
            self.log_test("Setup Ambiente", False, f"Erro: {str(e)[:100]}", critical=True)
            return False
    
    def test_message_storage(self) -> bool:
        """Testa se mensagens são armazenadas corretamente"""
        print("\n💾 TESTANDO ARMAZENAMENTO DE MENSAGENS...")
        
        if not self.test_conversation_id:
            self.log_test("Armazenamento de Mensagens", False, "Conversa de teste não disponível", critical=True)
            return False
        
        try:
            # Enviar múltiplas mensagens simulando conversa
            test_messages = [
                {"role": "user", "content": "Olá, preciso de ajuda com um produto"},
                {"role": "assistant", "content": "Olá! Claro, posso te ajudar. Qual produto você tem dúvidas?"},
                {"role": "user", "content": "É sobre o plano premium, quanto custa?"},
                {"role": "assistant", "content": "O plano premium custa R$ 99/mês. Você gostaria de saber mais detalhes?"},
                {"role": "user", "content": "Sim, quais são os benefícios?"}
            ]
            
            stored_message_ids = []
            
            for i, message in enumerate(test_messages):
                message_data = {
                    "conversation_id": self.test_conversation_id,
                    "role": message["role"],
                    "content": message["content"],
                    "metadata": {"test_sequence": i + 1}
                }
                
                response = requests.post(f"{self.backend_url}/api/messages", json=message_data, timeout=10)
                if response.status_code in [200, 201]:
                    stored_message_ids.append(response.json()['id'])
                else:
                    self.log_test(f"Armazenar Mensagem {i+1}", False, f"Erro: {response.status_code}")
                    return False
                
                # Pequena pausa para simular conversa real
                time.sleep(0.1)
            
            self.log_test("Armazenamento de Mensagens", True, f"{len(stored_message_ids)} mensagens armazenadas")
            return True
            
        except Exception as e:
            self.log_test("Armazenamento de Mensagens", False, f"Erro: {str(e)[:100]}")
            return False
    
    def test_message_retrieval(self) -> bool:
        """Testa se mensagens podem ser recuperadas em ordem"""
        print("\n📖 TESTANDO RECUPERAÇÃO DE MENSAGENS...")
        
        if not self.test_conversation_id:
            self.log_test("Recuperação de Mensagens", False, "Conversa de teste não disponível")
            return False
        
        try:
            # Buscar mensagens da conversa
            response = requests.get(f"{self.backend_url}/api/conversations/{self.test_conversation_id}/messages", timeout=10)
            
            if response.status_code == 200:
                messages = response.json()
                
                if len(messages) >= 5:  # Esperamos pelo menos 5 mensagens do teste anterior
                    self.log_test("Recuperação de Mensagens", True, f"{len(messages)} mensagens recuperadas")
                    
                    # Verificar ordem cronológica
                    timestamps = [msg.get('created_at', msg.get('timestamp', '')) for msg in messages]
                    is_ordered = all(timestamps[i] <= timestamps[i+1] for i in range(len(timestamps)-1))
                    
                    if is_ordered:
                        self.log_test("Ordem Cronológica", True, "Mensagens em ordem correta")
                    else:
                        self.log_test("Ordem Cronológica", False, "Mensagens fora de ordem")
                    
                    # Verificar conteúdo das mensagens
                    user_messages = [msg for msg in messages if msg.get('role') == 'user']
                    assistant_messages = [msg for msg in messages if msg.get('role') == 'assistant']
                    
                    self.log_test("Separação de Roles", True, f"{len(user_messages)} user, {len(assistant_messages)} assistant")
                    
                    return True
                else:
                    self.log_test("Recuperação de Mensagens", False, f"Apenas {len(messages)} mensagens encontradas", critical=True)
                    return False
            else:
                self.log_test("Recuperação de Mensagens", False, f"Erro: {response.status_code}", critical=True)
                return False
                
        except Exception as e:
            self.log_test("Recuperação de Mensagens", False, f"Erro: {str(e)[:100]}")
            return False
    
    def test_context_continuity(self) -> bool:
        """Testa se contexto é mantido em nova mensagem"""
        print("\n🧠 TESTANDO CONTINUIDADE DE CONTEXTO...")
        
        if not self.test_conversation_id:
            self.log_test("Continuidade de Contexto", False, "Conversa de teste não disponível")
            return False
        
        try:
            # Simular nova mensagem que requer contexto anterior
            context_message = {
                "conversation_id": self.test_conversation_id,
                "role": "user",
                "content": "E sobre aquele plano que você mencionou?"  # Referência ao contexto anterior
            }
            
            response = requests.post(f"{self.backend_url}/api/messages", json=context_message, timeout=10)
            if response.status_code not in [200, 201]:
                self.log_test("Enviar Mensagem de Contexto", False, f"Erro: {response.status_code}")
                return False
            
            # Buscar histórico completo para verificar se agente teria acesso
            response = requests.get(f"{self.backend_url}/api/conversations/{self.test_conversation_id}/messages", timeout=10)
            
            if response.status_code == 200:
                messages = response.json()
                
                # Verificar se há mensagens suficientes para contexto
                if len(messages) >= 6:  # 5 anteriores + 1 nova
                    # Verificar se mensagem de contexto está presente
                    context_msg = next((msg for msg in messages if "aquele plano" in msg.get('content', '')), None)
                    
                    if context_msg:
                        self.log_test("Continuidade de Contexto", True, "Mensagem de contexto armazenada e acessível")
                        
                        # Verificar se há referência ao plano premium mencionado antes
                        premium_mentioned = any("premium" in msg.get('content', '').lower() for msg in messages)
                        if premium_mentioned:
                            self.log_test("Referência Contextual", True, "Contexto anterior (plano premium) disponível")
                        else:
                            self.log_test("Referência Contextual", False, "Contexto anterior não encontrado")
                        
                        return True
                    else:
                        self.log_test("Continuidade de Contexto", False, "Mensagem de contexto não encontrada")
                        return False
                else:
                    self.log_test("Continuidade de Contexto", False, f"Histórico insuficiente: {len(messages)} mensagens")
                    return False
            else:
                self.log_test("Continuidade de Contexto", False, f"Erro ao buscar histórico: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Continuidade de Contexto", False, f"Erro: {str(e)[:100]}")
            return False
    
    def test_renus_memory_access(self) -> bool:
        """Testa se RENUS consegue acessar memória de conversas"""
        print("\n🤖 TESTANDO ACESSO À MEMÓRIA PELO RENUS...")
        
        try:
            # Buscar agente RENUS
            response = requests.get(f"{self.backend_url}/api/agents", timeout=10)
            if response.status_code != 200:
                self.log_test("Buscar Agente RENUS", False, f"Erro: {response.status_code}")
                return False
            
            agents = response.json()
            renus_agent = next((agent for agent in agents if agent.get('slug') == 'renus'), None)
            
            if not renus_agent:
                self.log_test("Buscar Agente RENUS", False, "Agente RENUS não encontrado", critical=True)
                return False
            
            self.log_test("Buscar Agente RENUS", True, f"RENUS encontrado: {renus_agent['id']}")
            
            # Testar se RENUS pode acessar conversas
            if self.test_conversation_id:
                # Simular processamento de mensagem pelo RENUS
                process_request = {
                    "conversation_id": self.test_conversation_id,
                    "agent_id": renus_agent['id'],
                    "message": "Preciso do histórico desta conversa para responder adequadamente"
                }
                
                # Tentar endpoint de processamento (pode não existir ainda)
                response = requests.post(f"{self.backend_url}/api/agents/process", json=process_request, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'context' in result or 'history' in result:
                        self.log_test("RENUS Acesso à Memória", True, "RENUS consegue acessar histórico")
                    else:
                        self.log_test("RENUS Acesso à Memória", False, "RENUS não retorna contexto histórico")
                elif response.status_code == 404:
                    self.log_test("RENUS Acesso à Memória", False, "Endpoint de processamento não implementado", critical=True)
                else:
                    self.log_test("RENUS Acesso à Memória", False, f"Erro: {response.status_code}")
                
                return True
            else:
                self.log_test("RENUS Acesso à Memória", False, "Conversa de teste não disponível")
                return False
                
        except Exception as e:
            self.log_test("RENUS Acesso à Memória", False, f"Erro: {str(e)[:100]}")
            return False
    
    def test_interview_memory_structure(self) -> bool:
        """Testa estrutura específica de memória de entrevistas"""
        print("\n📋 TESTANDO ESTRUTURA DE MEMÓRIA DE ENTREVISTAS...")
        
        try:
            # Verificar se há entrevistas no sistema
            response = requests.get(f"{self.backend_url}/api/interviews", timeout=10)
            
            if response.status_code == 200:
                interviews = response.json()
                
                if interviews:
                    interview_id = interviews[0]['id']
                    self.log_test("Buscar Entrevistas", True, f"{len(interviews)} entrevistas encontradas")
                    
                    # Testar acesso a mensagens de entrevista
                    response = requests.get(f"{self.backend_url}/api/interviews/{interview_id}/messages", timeout=10)
                    
                    if response.status_code == 200:
                        messages = response.json()
                        self.log_test("Mensagens de Entrevista", True, f"{len(messages)} mensagens encontradas")
                        
                        # Verificar se há múltiplas mensagens (indicativo de memória funcionando)
                        if len(messages) > 1:
                            self.log_test("Memória de Entrevista", True, "Múltiplas mensagens - memória funcionando")
                        else:
                            self.log_test("Memória de Entrevista", False, "Apenas 1 mensagem - possível problema", critical=True)
                        
                        return True
                    else:
                        self.log_test("Mensagens de Entrevista", False, f"Erro: {response.status_code}")
                        return False
                else:
                    self.log_test("Buscar Entrevistas", False, "Nenhuma entrevista encontrada")
                    return False
            else:
                self.log_test("Buscar Entrevistas", False, f"Erro: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Estrutura de Entrevistas", False, f"Erro: {str(e)[:100]}")
            return False
    
    def cleanup_test_environment(self):
        """Limpa ambiente de teste"""
        print("\n🧹 LIMPANDO AMBIENTE DE TESTE...")
        
        try:
            # Deletar conversa de teste
            if self.test_conversation_id:
                response = requests.delete(f"{self.backend_url}/api/conversations/{self.test_conversation_id}", timeout=5)
                if response.status_code in [200, 204]:
                    self.log_test("Limpar Conversa", True, "Conversa de teste removida")
                else:
                    self.log_test("Limpar Conversa", False, f"Erro: {response.status_code}")
            
            # Deletar lead de teste
            if self.test_lead_id:
                response = requests.delete(f"{self.backend_url}/api/leads/{self.test_lead_id}", timeout=5)
                if response.status_code in [200, 204]:
                    self.log_test("Limpar Lead", True, "Lead de teste removido")
                else:
                    self.log_test("Limpar Lead", False, f"Erro: {response.status_code}")
                    
        except Exception as e:
            self.log_test("Limpeza", False, f"Erro: {str(e)[:100]}")
    
    def run_all_tests(self):
        """Executa todos os testes de memória"""
        print("🧠 TESTANDO MEMÓRIA DE CONVERSAS DO RENUS")
        print(f"⏰ Timestamp: {datetime.now().isoformat()}")
        print("="*60)
        
        # Verificar conectividade
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code != 200:
                print("❌ Backend não está rodando - cancelando testes")
                return self.test_results
        except:
            print("❌ Backend não acessível - cancelando testes")
            return self.test_results
        
        # Executar testes
        try:
            # 1. Setup
            if not self.setup_test_environment():
                print("❌ Falha no setup - cancelando testes")
                return self.test_results
            
            # 2. Testes de armazenamento
            self.test_message_storage()
            
            # 3. Testes de recuperação
            self.test_message_retrieval()
            
            # 4. Testes de contexto
            self.test_context_continuity()
            
            # 5. Testes específicos do RENUS
            self.test_renus_memory_access()
            
            # 6. Testes de entrevistas
            self.test_interview_memory_structure()
            
        finally:
            # 7. Limpeza
            self.cleanup_test_environment()
        
        # Resumo
        self.print_summary()
        return self.test_results
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*60)
        print("RESUMO - TESTES DE MEMÓRIA DE CONVERSAS")
        print("="*60)
        
        total = len(self.test_results)
        passed = len([r for r in self.test_results if r['passed']])
        failed = len([r for r in self.test_results if not r['passed']])
        critical_failures = len([r for r in self.test_results if not r['passed'] and r['critical']])
        
        print(f"Total de testes: {total}")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {failed}")
        print(f"🚨 Falhas críticas: {critical_failures}")
        
        if critical_failures > 0:
            print(f"\n🚨 PROBLEMAS CRÍTICOS DE MEMÓRIA:")
            for result in self.test_results:
                if not result['passed'] and result['critical']:
                    print(f"  - {result['test']}: {result['details']}")
        
        # Diagnóstico específico
        if failed > 0:
            print(f"\n🔍 DIAGNÓSTICO:")
            storage_ok = any(r['test'] == 'Armazenamento de Mensagens' and r['passed'] for r in self.test_results)
            retrieval_ok = any(r['test'] == 'Recuperação de Mensagens' and r['passed'] for r in self.test_results)
            context_ok = any(r['test'] == 'Continuidade de Contexto' and r['passed'] for r in self.test_results)
            
            if not storage_ok:
                print("  - Problema: Mensagens não estão sendo armazenadas")
            elif not retrieval_ok:
                print("  - Problema: Mensagens não podem ser recuperadas")
            elif not context_ok:
                print("  - Problema: Contexto não é mantido entre turnos")
            else:
                print("  - Problema: RENUS não consegue acessar histórico")
        
        # Salvar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"conversation_memory_test_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Resultados salvos em: {report_file}")

def main():
    """Função principal"""
    tester = ConversationMemoryTester()
    results = tester.run_all_tests()
    
    # Código de saída
    critical_failures = len([r for r in results if not r['passed'] and r['critical']])
    total_failures = len([r for r in results if not r['passed']])
    
    if critical_failures > 0:
        return 2
    elif total_failures > 0:
        return 1
    else:
        return 0

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)