#!/usr/bin/env python3
"""
Investigação: Como RENUS/ISA foram criados
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from src.config.supabase import supabase_admin
import json

def investigar_agentes():
    print("🔍 INVESTIGAÇÃO: Como RENUS/ISA Foram Criados")
    print("=" * 60)
    
    # 1. Buscar todos os agentes
    result = supabase_admin.table('agents').select('*').execute()
    
    if not result.data:
        print("❌ Nenhum agente encontrado")
        return
    
    print(f"📊 Total de agentes: {len(result.data)}")
    print()
    
    # 2. Analisar cada agente
    for i, agent in enumerate(result.data, 1):
        print(f"🤖 AGENTE {i}: {agent['name']}")
        print(f"   ID: {agent['id']}")
        print(f"   Type: {agent.get('type', 'NULL')}")
        print(f"   Role: {agent.get('role', 'NULL')}")
        print(f"   Status: {agent.get('status', 'NULL')}")
        print(f"   Client ID: {agent.get('client_id', 'NULL')}")
        print(f"   Created: {agent['created_at']}")
        print(f"   Updated: {agent['updated_at']}")
        
        # Config analysis
        config = agent.get('config', {})
        if config:
            print(f"   Config keys: {list(config.keys())}")
            if 'wizard_session' in config:
                print(f"   ⚠️  É sessão wizard: {config['wizard_session']}")
                print(f"   Step atual: {config.get('current_step', 'N/A')}")
        else:
            print("   Config: VAZIO")
        
        # System prompt
        prompt = agent.get('system_prompt', '')
        if prompt:
            print(f"   System Prompt: {prompt[:100]}...")
        else:
            print("   System Prompt: VAZIO")
        
        print("   " + "-" * 50)
    
    print()
    print("🧪 TESTE: Criar agente via SQL")
    print("=" * 40)
    
    # 3. Tentar criar agente similar
    try:
        test_agent = {
            'name': 'Teste SQL',
            'type': 'system',
            'role': 'assistant',
            'status': 'active',
            'config': {},
            'system_prompt': 'Você é um agente de teste criado via SQL direto.'
        }
        
        # Inserir
        insert_result = supabase_admin.table('agents').insert(test_agent).execute()
        
        if insert_result.data:
            created_agent = insert_result.data[0]
            print(f"✅ Agente criado com sucesso!")
            print(f"   ID: {created_agent['id']}")
            print(f"   Nome: {created_agent['name']}")
            
            # Limpar teste
            supabase_admin.table('agents').delete().eq('id', created_agent['id']).execute()
            print("🧹 Agente de teste removido")
        else:
            print("❌ Falha ao criar agente")
            
    except Exception as e:
        print(f"❌ Erro ao criar agente: {e}")
    
    print()
    print("📋 CAMPOS OBRIGATÓRIOS IDENTIFICADOS:")
    print("   - name (text, NOT NULL)")
    print("   - id (uuid, auto-generated)")
    print("   - created_at (timestamp, auto)")
    print("   - updated_at (timestamp, auto)")
    print()
    print("📋 CAMPOS OPCIONAIS COM DEFAULTS:")
    print("   - role (enum, default: 'assistant')")
    print("   - status (enum, default: 'draft')")
    print("   - config (jsonb, default: {})")
    print("   - system_prompt (text, default: NULL)")

if __name__ == "__main__":
    investigar_agentes()