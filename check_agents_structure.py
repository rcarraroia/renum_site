#!/usr/bin/env python3
"""
Script para verificar estrutura real das tabelas agents e sub_agents
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.config.supabase import supabase_admin

def check_agents_structure():
    print("=== VERIFICAÇÃO ESTRUTURA AGENTS/SUB_AGENTS ===")
    print()
    
    # Verificar tabela agents
    print("1. TABELA AGENTS:")
    try:
        response = supabase_admin.table('agents').select('*').limit(1).execute()
        if response.data:
            agent = response.data[0]
            print("   ✅ Tabela existe")
            print("   Colunas encontradas:")
            for key in sorted(agent.keys()):
                print(f"     - {key}")
        else:
            print("   ⚠️ Tabela existe mas está vazia")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # Verificar tabela sub_agents
    print("2. TABELA SUB_AGENTS:")
    try:
        response = supabase_admin.table('sub_agents').select('*').limit(1).execute()
        if response.data:
            subagent = response.data[0]
            print("   ✅ Tabela existe")
            print("   Colunas encontradas:")
            for key in sorted(subagent.keys()):
                print(f"     - {key}")
                
            # Verificar se tem agent_id ou client_id
            if 'agent_id' in subagent:
                print("   ✅ Tem coluna agent_id (estrutura correta)")
            else:
                print("   ❌ NÃO tem coluna agent_id")
                
            if 'client_id' in subagent:
                print("   ❌ Ainda tem coluna client_id (estrutura antiga)")
            else:
                print("   ✅ NÃO tem coluna client_id (migração completa)")
        else:
            print("   ⚠️ Tabela existe mas está vazia")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # Contar registros
    print("3. CONTAGEM DE REGISTROS:")
    try:
        agents_count = supabase_admin.table('agents').select('id', count='exact').execute()
        print(f"   Agents: {agents_count.count}")
        
        subagents_count = supabase_admin.table('sub_agents').select('id', count='exact').execute()
        print(f"   Sub-agents: {subagents_count.count}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()
    
    # Verificar se migrations existem
    print("4. MIGRATIONS:")
    migration_009 = os.path.exists('backend/migrations/009_create_agents_table.sql')
    migration_010 = os.path.exists('backend/migrations/010_migrate_subagents_to_agents.sql')
    
    print(f"   Migration 009 (create agents): {'✅' if migration_009 else '❌'}")
    print(f"   Migration 010 (migrate subagents): {'✅' if migration_010 else '❌'}")

if __name__ == "__main__":
    check_agents_structure()