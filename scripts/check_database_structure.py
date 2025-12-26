#!/usr/bin/env python3
"""
Script para verificar estrutura do banco de dados Supabase
Verifica colunas das tabelas leads e messages
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from src.config.supabase import supabase_admin

def check_table_structure():
    """Verifica estrutura das tabelas críticas"""
    
    print("🔍 Verificando estrutura do banco de dados...")
    print("=" * 50)
    
    try:
        # Verificar estrutura da tabela leads
        print("\n📋 Tabela: leads")
        try:
            result = supabase_admin.table('leads').select('*').limit(1).execute()
            if result.data:
                print("Colunas encontradas:")
                for key in result.data[0].keys():
                    print(f"  - {key}")
            else:
                print("⚠️ Tabela leads vazia, tentando inserção de teste...")
                # Tentar inserir um registro de teste para ver a estrutura
                test_lead = {
                    'name': 'Teste Estrutura',
                    'phone': '+5511999999999',
                    'email': 'teste@estrutura.com',
                    'source': 'test',
                    'status': 'novo'
                }
                insert_result = supabase_admin.table('leads').insert(test_lead).execute()
                if insert_result.data:
                    print("Estrutura inferida após inserção:")
                    for key in insert_result.data[0].keys():
                        print(f"  - {key}")
                    # Deletar o registro de teste
                    supabase_admin.table('leads').delete().eq('email', 'teste@estrutura.com').execute()
        except Exception as e:
            print(f"❌ Erro ao acessar tabela leads: {e}")
        
        # Verificar se coluna metadata existe
        try:
            test_metadata = supabase_admin.table('leads').select('metadata').limit(1).execute()
            print("✅ Coluna 'metadata' existe na tabela leads")
        except Exception as e:
            print(f"❌ Coluna 'metadata' NÃO existe na tabela leads")
        
        print("\n" + "-" * 50)
        
        # Verificar estrutura da tabela messages
        print("\n📋 Tabela: messages")
        try:
            messages_result = supabase_admin.table('messages').select('*').limit(1).execute()
            if messages_result.data:
                print("Colunas encontradas:")
                for key in messages_result.data[0].keys():
                    print(f"  - {key}")
            else:
                print("⚠️ Tabela messages vazia")
        except Exception as e:
            print(f"❌ Erro ao acessar tabela messages: {e}")
        
        # Verificar se coluna role existe
        try:
            test_role = supabase_admin.table('messages').select('role').limit(1).execute()
            print("✅ Coluna 'role' existe na tabela messages")
        except Exception as e:
            print(f"❌ Coluna 'role' NÃO existe na tabela messages")
        
        print("\n" + "-" * 50)
        
        # Verificar tabela interview_messages (alternativa)
        print("\n📋 Tabela: interview_messages")
        try:
            interview_result = supabase_admin.table('interview_messages').select('*').limit(1).execute()
            if interview_result.data:
                print("Colunas encontradas:")
                for key in interview_result.data[0].keys():
                    print(f"  - {key}")
            else:
                print("⚠️ Tabela interview_messages vazia")
        except Exception as e:
            print(f"❌ Erro ao acessar tabela interview_messages: {e}")
        
        print("\n" + "-" * 50)
        
        # Verificar agentes existentes
        print("\n🤖 Agentes existentes:")
        try:
            agents_result = supabase_admin.table('agents').select('id, name, client_id').execute()
            if agents_result.data:
                for agent in agents_result.data:
                    print(f"  - {agent['name']} (ID: {agent['id'][:8]}...)")
            else:
                print("❌ Nenhum agente encontrado")
        except Exception as e:
            print(f"❌ Erro ao buscar agentes: {e}")
        
        # Verificar sub-agentes existentes
        print("\n🔧 Sub-agentes existentes:")
        try:
            subagents_result = supabase_admin.table('sub_agents').select('id, name, parent_agent_id').execute()
            if subagents_result.data:
                for subagent in subagents_result.data:
                    print(f"  - {subagent['name']} (ID: {subagent['id'][:8]}..., Parent: {subagent['parent_agent_id'][:8]}...)")
            else:
                print("❌ Nenhum sub-agente encontrado")
        except Exception as e:
            print(f"❌ Erro ao buscar sub-agentes: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Verificação concluída!")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_structure()