#!/usr/bin/env python3
"""
Script para verificar e criar dados de teste necessários
"""

import os
import sys
from supabase import create_client, Client
from uuid import UUID

# Configurações do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# IDs de teste
TEST_SUB_AGENT_ID = "12345678-1234-5678-9012-123456789012"
TEST_AGENT_ID = "00000000-0000-0000-0000-000000000001"

def main():
    print("🔍 Verificando dados de teste...")
    
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # 1. Verificar se agente RENUS existe
        print(f"\n🤖 Verificando agente RENUS ({TEST_AGENT_ID}):")
        try:
            result = supabase.table('renus_config').select('*').eq('agent_id', TEST_AGENT_ID).execute()
            if result.data:
                print("  ✅ Agente RENUS encontrado")
                print(f"  Config: {result.data[0].get('config', {})}")
            else:
                print("  ❌ Agente RENUS não encontrado")
                # Criar agente RENUS
                print("  📝 Criando agente RENUS...")
                agent_data = {
                    'agent_id': TEST_AGENT_ID,
                    'config': {
                        'name': 'RENUS',
                        'type': 'main_agent',
                        'integrations': {
                            'whatsapp': {'enabled': True},
                            'email': {'enabled': True},
                            'calendar': {'enabled': True}
                        }
                    },
                    'prompts': {
                        'system': 'Você é o RENUS, agente principal de automação.'
                    },
                    'active': True
                }
                supabase.table('renus_config').insert(agent_data).execute()
                print("  ✅ Agente RENUS criado")
        except Exception as e:
            print(f"  ❌ Erro ao verificar agente RENUS: {e}")
        
        # 2. Verificar se sub-agente de teste existe
        print(f"\n🎯 Verificando sub-agente de teste ({TEST_SUB_AGENT_ID}):")
        try:
            result = supabase.table('sub_agents').select('*').eq('id', TEST_SUB_AGENT_ID).execute()
            if result.data:
                print("  ✅ Sub-agente de teste encontrado")
                print(f"  Nome: {result.data[0].get('name')}")
                print(f"  Especialização: {result.data[0].get('specialization')}")
            else:
                print("  ❌ Sub-agente de teste não encontrado")
                # Criar sub-agente de teste
                print("  📝 Criando sub-agente de teste...")
                sub_agent_data = {
                    'id': TEST_SUB_AGENT_ID,
                    'parent_agent_id': TEST_AGENT_ID,
                    'name': 'Agente de Vendas',
                    'specialization': 'sales',
                    'config': {
                        'personality': 'friendly',
                        'expertise': ['pricing', 'plans', 'demos'],
                        'integrations': {
                            'whatsapp': {'enabled': True},
                            'email': {'enabled': True}
                        }
                    },
                    'inheritance_config': {
                        'integrations': True,
                        'prompts': False,
                        'tools': True
                    },
                    'routing_config': {
                        'keywords': ['preço', 'valor', 'plano', 'comprar', 'contratar'],
                        'topics': ['sales', 'pricing', 'commercial']
                    },
                    'is_active': True
                }
                supabase.table('sub_agents').insert(sub_agent_data).execute()
                print("  ✅ Sub-agente de teste criado")
        except Exception as e:
            print(f"  ❌ Erro ao verificar sub-agente: {e}")
        
        # 3. Verificar dados existentes
        print(f"\n📊 Resumo dos dados:")
        
        # Contar sub-agentes
        try:
            result = supabase.table('sub_agents').select('id', count='exact').execute()
            print(f"  Sub-agentes: {result.count}")
        except Exception as e:
            print(f"  Erro contando sub-agentes: {e}")
        
        # Contar agentes principais
        try:
            result = supabase.table('renus_config').select('id', count='exact').execute()
            print(f"  Agentes principais: {result.count}")
        except Exception as e:
            print(f"  Erro contando agentes principais: {e}")
        
        # Contar leads
        try:
            result = supabase.table('leads').select('id', count='exact').execute()
            print(f"  Leads: {result.count}")
        except Exception as e:
            print(f"  Erro contando leads: {e}")
        
        print("\n✅ Verificação de dados concluída!")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()