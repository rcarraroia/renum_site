"""
Script de investigação: Agentes e Sub-Agentes
Valida estrutura do banco de dados e dados existentes
"""

import os
from supabase import create_client, Client
from datetime import datetime

# Credenciais
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def main():
    print("=" * 80)
    print("INVESTIGAÇÃO: AGENTES E SUB-AGENTES")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Conectar ao Supabase
    print("🔌 Conectando ao Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    print("✅ Conectado com sucesso!")
    print()
    
    # ========================================
    # PARTE 1: VALIDAR TABELAS
    # ========================================
    print("=" * 80)
    print("PARTE 1: VALIDAÇÃO DE TABELAS")
    print("=" * 80)
    print()
    
    # Verificar se tabelas existem
    print("📋 Verificando existência de tabelas...")
    
    tables_to_check = ['agents', 'sub_agents', 'renus_config']
    
    for table_name in tables_to_check:
        try:
            result = supabase.table(table_name).select("*").limit(1).execute()
            print(f"✅ Tabela '{table_name}' existe")
        except Exception as e:
            print(f"❌ Tabela '{table_name}' NÃO existe ou erro: {str(e)}")
    
    print()
    
    # ========================================
    # PARTE 2: TABELA AGENTS
    # ========================================
    print("=" * 80)
    print("PARTE 2: TABELA AGENTS")
    print("=" * 80)
    print()
    
    try:
        # Buscar todos os agentes
        agents_result = supabase.table('agents').select("*").execute()
        agents = agents_result.data
        
        print(f"📊 Total de agentes: {len(agents)}")
        print()
        
        if agents:
            print("Agentes encontrados:")
            print("-" * 80)
            for agent in agents:
                print(f"ID: {agent.get('id')}")
                print(f"Nome: {agent.get('name')}")
                print(f"Template: {agent.get('template_type')}")
                print(f"Status: {agent.get('status')}")
                print(f"Criado em: {agent.get('created_at')}")
                print("-" * 80)
        else:
            print("⚠️ Nenhum agente encontrado")
        
        print()
        
        # Verificar estrutura (colunas)
        if agents:
            print("Colunas da tabela 'agents':")
            columns = list(agents[0].keys())
            for col in columns:
                print(f"  - {col}")
        
    except Exception as e:
        print(f"❌ Erro ao consultar tabela 'agents': {str(e)}")
    
    print()
    
    # ========================================
    # PARTE 3: TABELA SUB_AGENTS
    # ========================================
    print("=" * 80)
    print("PARTE 3: TABELA SUB_AGENTS")
    print("=" * 80)
    print()
    
    try:
        # Buscar todos os sub-agentes
        subagents_result = supabase.table('sub_agents').select("*").execute()
        subagents = subagents_result.data
        
        print(f"📊 Total de sub-agentes: {len(subagents)}")
        print()
        
        if subagents:
            print("Sub-agentes encontrados:")
            print("-" * 80)
            for subagent in subagents:
                print(f"ID: {subagent.get('id')}")
                print(f"Agent ID: {subagent.get('agent_id')}")
                print(f"Nome: {subagent.get('name')}")
                print(f"Descrição: {subagent.get('description')}")
                print(f"Canal: {subagent.get('channel')}")
                print(f"Modelo: {subagent.get('model')}")
                print(f"Status: {subagent.get('status')}")
                print(f"Criado em: {subagent.get('created_at')}")
                print("-" * 80)
        else:
            print("⚠️ Nenhum sub-agente encontrado")
        
        print()
        
        # Verificar estrutura (colunas)
        if subagents:
            print("Colunas da tabela 'sub_agents':")
            columns = list(subagents[0].keys())
            for col in columns:
                print(f"  - {col}")
        
    except Exception as e:
        print(f"❌ Erro ao consultar tabela 'sub_agents': {str(e)}")
    
    print()
    
    # ========================================
    # PARTE 4: RELACIONAMENTO AGENTS ↔ SUB_AGENTS
    # ========================================
    print("=" * 80)
    print("PARTE 4: RELACIONAMENTO AGENTS ↔ SUB_AGENTS")
    print("=" * 80)
    print()
    
    try:
        # Buscar agentes com seus sub-agentes
        agents_result = supabase.table('agents').select("id, name").execute()
        agents = agents_result.data
        
        if agents:
            for agent in agents:
                agent_id = agent.get('id')
                agent_name = agent.get('name')
                
                # Buscar sub-agentes deste agente
                subagents_result = supabase.table('sub_agents').select("*").eq('agent_id', agent_id).execute()
                subagents = subagents_result.data
                
                print(f"Agente: {agent_name} (ID: {agent_id})")
                print(f"  Sub-agentes: {len(subagents)}")
                
                if subagents:
                    for subagent in subagents:
                        print(f"    - {subagent.get('name')} ({subagent.get('channel')}) - {subagent.get('status')}")
                else:
                    print("    (nenhum sub-agente)")
                
                print()
        
    except Exception as e:
        print(f"❌ Erro ao consultar relacionamento: {str(e)}")
    
    print()
    
    # ========================================
    # PARTE 5: TABELA RENUS_CONFIG
    # ========================================
    print("=" * 80)
    print("PARTE 5: TABELA RENUS_CONFIG")
    print("=" * 80)
    print()
    
    try:
        # Buscar configurações
        config_result = supabase.table('renus_config').select("*").execute()
        configs = config_result.data
        
        print(f"📊 Total de configurações: {len(configs)}")
        print()
        
        if configs:
            print("Configurações encontradas:")
            print("-" * 80)
            for config in configs:
                print(f"ID: {config.get('id')}")
                print(f"Client ID: {config.get('client_id')}")
                print(f"Agent Type: {config.get('agent_type')}")
                print(f"Ativo: {config.get('active')}")
                print(f"Config: {str(config.get('config'))[:100]}...")
                print("-" * 80)
        else:
            print("⚠️ Nenhuma configuração encontrada")
        
    except Exception as e:
        print(f"❌ Erro ao consultar tabela 'renus_config': {str(e)}")
    
    print()
    
    # ========================================
    # RESUMO
    # ========================================
    print("=" * 80)
    print("RESUMO DA INVESTIGAÇÃO")
    print("=" * 80)
    print()
    
    try:
        agents_count = len(supabase.table('agents').select("id").execute().data)
        subagents_count = len(supabase.table('sub_agents').select("id").execute().data)
        configs_count = len(supabase.table('renus_config').select("id").execute().data)
        
        print(f"✅ Tabela 'agents': {agents_count} registros")
        print(f"✅ Tabela 'sub_agents': {subagents_count} registros")
        print(f"✅ Tabela 'renus_config': {configs_count} registros")
        print()
        
        if subagents_count >= 2:
            print("✅ Sub-agentes esperados encontrados (Pesquisa MMN, Atendimento Clínicas)")
        else:
            print("⚠️ Menos de 2 sub-agentes encontrados")
        
    except Exception as e:
        print(f"❌ Erro ao gerar resumo: {str(e)}")
    
    print()
    print("=" * 80)
    print("FIM DA INVESTIGAÇÃO - BANCO DE DADOS")
    print("=" * 80)

if __name__ == "__main__":
    main()
