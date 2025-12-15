#!/usr/bin/env python3
"""
Script para verificar agentes no banco de dados
"""
import os
import sys
sys.path.append('backend/src')

from src.config.supabase import get_supabase_client

def check_agents():
    """Verifica agentes no banco"""
    print("=== VERIFICANDO AGENTES NO BANCO ===")
    
    try:
        supabase = get_supabase_client()
        
        # Verificar tabela agents
        print("\n1. TABELA AGENTS:")
        response = supabase.table('agents').select('*').execute()
        agents = response.data
        print(f"Agentes encontrados: {len(agents)}")
        
        for agent in agents:
            print(f"- ID: {agent.get('id')}")
            print(f"  Nome: {agent.get('name')}")
            print(f"  Slug: {agent.get('slug')}")
            print(f"  Status: {agent.get('status')}")
            print(f"  Público: {agent.get('is_public')}")
            print()
        
        # Verificar tabela sub_agents (legacy)
        print("\n2. TABELA SUB_AGENTS:")
        response = supabase.table('sub_agents').select('*').execute()
        sub_agents = response.data
        print(f"Sub-agentes encontrados: {len(sub_agents)}")
        
        for sub_agent in sub_agents:
            print(f"- ID: {sub_agent.get('id')}")
            print(f"  Nome: {sub_agent.get('name')}")
            print(f"  Tipo: {sub_agent.get('type')}")
            print(f"  Ativo: {sub_agent.get('active')}")
            print()
            
        # Verificar tabela renus_config
        print("\n3. TABELA RENUS_CONFIG:")
        response = supabase.table('renus_config').select('*').execute()
        configs = response.data
        print(f"Configurações encontradas: {len(configs)}")
        
        for config in configs:
            print(f"- ID: {config.get('id')}")
            print(f"  Cliente: {config.get('client_id')}")
            print(f"  Tipo: {config.get('agent_type')}")
            print(f"  Ativo: {config.get('active')}")
            print()
            
        return agents, sub_agents, configs
        
    except Exception as e:
        print(f"Erro ao verificar banco: {e}")
        return [], [], []

def create_test_agent():
    """Cria um agente de teste"""
    print("\n=== CRIANDO AGENTE DE TESTE ===")
    
    try:
        supabase = get_supabase_client()
        
        agent_data = {
            "name": "Agente de Vendas Slim",
            "slug": "agente-vendas-slim",
            "description": "Agente especializado em vendas e atendimento ao cliente",
            "status": "active",
            "is_public": True,
            "system_prompt": "Você é um agente de vendas especializado. Seja profissional, prestativo e focado em ajudar o cliente.",
            "model": "gpt-4o-mini",
            "template_type": "sales",
            "client_id": "876be331-9553-4e9a-9f29-63cfa711e056",  # ID do admin
            "project_id": None,
            "public_url": "https://agente-vendas-slim.renum.com.br",
            "config": {
                "temperature": 0.7,
                "max_tokens": 500,
                "tools": ["web_search", "calculator"]
            }
        }
        
        response = supabase.table('agents').insert(agent_data).execute()
        
        if response.data:
            agent = response.data[0]
            print(f"✅ Agente criado com sucesso!")
            print(f"ID: {agent.get('id')}")
            print(f"Nome: {agent.get('name')}")
            print(f"Slug: {agent.get('slug')}")
            return agent
        else:
            print(f"❌ Erro ao criar agente: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao criar agente: {e}")
        return None

if __name__ == "__main__":
    # Verificar estado atual
    agents, sub_agents, configs = check_agents()
    
    # Se não houver agentes, criar um de teste
    if not agents:
        print("\n🔧 Nenhum agente encontrado. Criando agente de teste...")
        test_agent = create_test_agent()
        
        if test_agent:
            print("\n✅ Agente de teste criado! Agora você pode testar o chat.")
        else:
            print("\n❌ Falha ao criar agente de teste.")
    else:
        print(f"\n✅ {len(agents)} agente(s) encontrado(s) no banco.")