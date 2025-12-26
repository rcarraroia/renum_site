#!/usr/bin/env python3
"""
Script para criar dados de teste para validação do TRACK 2
Cria sub-agente de teste usando o agente RENUS existente
"""

import sys
import os
from uuid import uuid4
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from src.config.supabase import supabase_admin

def create_test_data():
    """Cria dados de teste necessários para validação"""
    
    print("🔧 Criando dados de teste para TRACK 2...")
    print("=" * 50)
    
    try:
        # 1. Buscar agente RENUS existente
        print("\n🤖 Buscando agente RENUS...")
        renus_result = supabase_admin.table('agents').select('*').eq('name', 'RENUS').execute()
        
        if not renus_result.data:
            print("❌ Agente RENUS não encontrado!")
            return False
        
        renus_agent = renus_result.data[0]
        print(f"✅ Agente RENUS encontrado: {renus_agent['id']}")
        
        # 4. Verificar estrutura da tabela sub_agents
        print("\n📋 Verificando estrutura da tabela sub_agents...")
        try:
            subagents_sample = supabase_admin.table('sub_agents').select('*').limit(1).execute()
            if subagents_sample.data:
                print("Colunas encontradas:")
                for key in subagents_sample.data[0].keys():
                    print(f"  - {key}")
            else:
                print("⚠️ Tabela sub_agents vazia, tentando inserção simples...")
        except Exception as e:
            print(f"❌ Erro ao verificar sub_agents: {e}")
        
        # 2. Verificar se já existe sub-agente de teste
        test_subagent_id = "12345678-1234-5678-9012-123456789012"
        existing_subagent = supabase_admin.table('sub_agents').select('*').eq('id', test_subagent_id).execute()
        
        if existing_subagent.data:
            print(f"✅ Sub-agente de teste já existe: {existing_subagent.data[0]['name']}")
        else:
            # 3. Criar sub-agente de teste
            print("\n🔧 Criando sub-agente de teste...")
            
            subagent_data = {
                'id': test_subagent_id,
                'parent_agent_id': renus_agent['id'],
                'name': 'Vendas Especialista (Teste)',
                'specialization': 'vendas',
                'config': {
                    'channel': 'whatsapp',
                    'model': 'gpt-4o-mini',
                    'topics': ['vendas', 'precos', 'planos', 'orcamento'],
                    'identity': {
                        'system_prompt': 'Você é um especialista em vendas da RENUM. Ajude clientes com informações sobre preços, planos e orçamentos.',
                        'persona': 'Profissional, prestativo e focado em resultados',
                        'welcome_message': 'Olá! Sou especialista em vendas da RENUM. Como posso ajudá-lo com nossos planos e preços?'
                    }
                },
                'inheritance_config': {
                    'instructions': True,
                    'intelligence': True,
                    'tools': True,
                    'integrations': True,
                    'knowledge': True,
                    'triggers': False,
                    'guardrails': True
                },
                'routing_config': {
                    'keywords': ['preço', 'valor', 'custo', 'plano', 'orçamento', 'vendas', 'contratar'],
                    'user_profile': {},
                    'context_conditions': []
                },
                'is_active': True
            }
            
            result = supabase_admin.table('sub_agents').insert(subagent_data).execute()
            
            if result.data:
                print(f"✅ Sub-agente de teste criado: {result.data[0]['name']}")
            else:
                print("❌ Erro ao criar sub-agente de teste")
                return False
        
        # 4. Criar interview para as mensagens de teste
        print("\n📋 Criando interview de teste...")
        
        test_conversation_id = "87654321-4321-8765-2109-876543210987"
        
        # Verificar se interview já existe
        existing_interview = supabase_admin.table('interviews').select('*').eq('id', test_conversation_id).execute()
        
        if existing_interview.data:
            print(f"✅ Interview de teste já existe: {existing_interview.data[0]['id']}")
        else:
            # Criar interview de teste
            interview_data = {
                'id': test_conversation_id,
                'lead_id': None,  # Será criado durante o teste
                'project_id': None,  # Opcional para teste
                'status': 'in_progress',
                'started_at': datetime.now().isoformat(),
                'completed_at': None
            }
            
            try:
                interview_result = supabase_admin.table('interviews').insert(interview_data).execute()
                if interview_result.data:
                    print(f"✅ Interview de teste criada: {interview_result.data[0]['id']}")
                else:
                    print("❌ Erro ao criar interview de teste")
            except Exception as e:
                print(f"⚠️ Erro ao criar interview (pode não ser necessária): {e}")
        
        # 5. Criar algumas mensagens de teste para interview_messages
        # 5. Criar algumas mensagens de teste para interview_messages
        print("\n💬 Criando mensagens de teste...")
        
        test_conversation_id = "87654321-4321-8765-2109-876543210987"
        
        # Verificar se já existem mensagens
        existing_messages = supabase_admin.table('interview_messages').select('*').eq('interview_id', test_conversation_id).execute()
        
        if existing_messages.data:
            print(f"✅ Mensagens de teste já existem: {len(existing_messages.data)} mensagens")
        else:
            # Criar mensagens de teste
            test_messages = [
                {
                    'id': str(uuid4()),
                    'interview_id': test_conversation_id,
                    'role': 'user',
                    'content': 'Olá, meu nome é João Silva e meu email é joao@teste.com. Gostaria de saber os preços dos planos.',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {}
                },
                {
                    'id': str(uuid4()),
                    'interview_id': test_conversation_id,
                    'role': 'assistant',
                    'content': 'Olá João! Fico feliz em ajudá-lo com informações sobre nossos planos. Vou te enviar nossa tabela de preços por email.',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {}
                },
                {
                    'id': str(uuid4()),
                    'interview_id': test_conversation_id,
                    'role': 'user',
                    'content': 'Perfeito! Também gostaria de agendar uma demonstração. Meu telefone é +5511999887766.',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {}
                }
            ]
            
            for message in test_messages:
                try:
                    result = supabase_admin.table('interview_messages').insert(message).execute()
                    if result.data:
                        print(f"✅ Mensagem criada: {message['role']} - {message['content'][:50]}...")
                    else:
                        print(f"❌ Erro ao criar mensagem: {message['role']}")
                except Exception as e:
                    print(f"⚠️ Erro ao criar mensagem {message['role']}: {e}")
        
        # 6. Verificar se existe lead de teste
        print("\n👤 Verificando leads de teste...")
        
        test_leads = supabase_admin.table('leads').select('*').ilike('notes', '%teste%').execute()
        
        if test_leads.data:
            print(f"✅ Leads de teste existem: {len(test_leads.data)} leads")
        else:
            print("ℹ️ Nenhum lead de teste encontrado (será criado durante os testes)")
        
        print("\n" + "=" * 50)
        print("✅ Dados de teste criados com sucesso!")
        print("\nDados criados:")
        print(f"  🤖 Agente pai: RENUS ({renus_agent['id'][:8]}...)")
        print(f"  🔧 Sub-agente: Vendas Especialista (Teste) ({test_subagent_id[:8]}...)")
        print(f"  💬 Conversa: {test_conversation_id[:8]}... com 3 mensagens")
        print(f"  📋 Tópicos: vendas, precos, planos, orcamento")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_test_data()
    exit_code = 0 if success else 1
    print(f"\n🏁 Script concluído com código de saída: {exit_code}")
    sys.exit(exit_code)