#!/usr/bin/env python3
"""
Script para verificar status atual do wizard antes da correção
"""

import os
from supabase import create_client, Client

def verificar_estrutura_agents():
    """Verifica estrutura atual da tabela agents"""
    print("🔍 VERIFICANDO ESTRUTURA ATUAL DA TABELA AGENTS...")
    
    # Credenciais do Supabase
    url = 'https://vhixvzaxswphwoymdhgg.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw'
    
    try:
        supabase: Client = create_client(url, key)
        
        # Verificar se tabela existe e pegar estrutura
        result = supabase.table('agents').select('*').limit(1).execute()
        
        if result.data:
            columns = list(result.data[0].keys())
            print(f"✅ Tabela 'agents' encontrada com {len(columns)} colunas")
            
            # Verificar se coluna status existe
            status_cols = [col for col in columns if 'status' in col.lower()]
            if status_cols:
                print(f"✅ Colunas status encontradas: {status_cols}")
                
                # Verificar valores atuais
                result_all = supabase.table('agents').select('id, name, status').execute()
                print(f"\n📊 Agentes existentes ({len(result_all.data)}):")
                for agent in result_all.data:
                    print(f"  - {agent.get('name', 'Sem nome')}: status = {agent.get('status', 'NULL')}")
                
                return True, status_cols[0]
            else:
                print("❌ Nenhuma coluna status encontrada")
                return False, None
                
        else:
            print("⚠️ Tabela agents está vazia, mas existe")
            # Tentar verificar estrutura via SQL
            return False, None
            
    except Exception as e:
        print(f"❌ Erro conectando ao Supabase: {e}")
        return False, None

def verificar_enum_status():
    """Verifica se enum agent_status existe"""
    print("\n🔍 VERIFICANDO ENUM agent_status...")
    
    url = 'https://vhixvzaxswphwoymdhgg.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw'
    
    try:
        supabase: Client = create_client(url, key)
        
        # Verificar enums existentes
        result = supabase.rpc('get_enum_values', {'enum_name': 'agent_status'}).execute()
        
        if result.data:
            print(f"✅ Enum 'agent_status' encontrado com valores: {result.data}")
            return True
        else:
            print("❌ Enum 'agent_status' não encontrado")
            return False
            
    except Exception as e:
        print(f"⚠️ Não foi possível verificar enum (pode não existir): {e}")
        return False

def main():
    print("🚀 VERIFICAÇÃO INICIAL - STATUS DO WIZARD")
    print("=" * 50)
    
    # 1. Verificar estrutura da tabela
    has_status, status_col = verificar_estrutura_agents()
    
    # 2. Verificar enum
    has_enum = verificar_enum_status()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    if has_status:
        print(f"✅ Coluna status existe: '{status_col}'")
        print("🎯 AÇÃO: Testar wizard diretamente")
    else:
        print("❌ Coluna status NÃO existe")
        print("🎯 AÇÃO: Adicionar coluna status")
    
    if has_enum:
        print("✅ Enum agent_status existe")
    else:
        print("❌ Enum agent_status NÃO existe")
        print("🎯 AÇÃO: Criar enum agent_status")
    
    print("\n🔄 PRÓXIMO PASSO:")
    if has_status and has_enum:
        print("  → Testar wizard end-to-end")
    else:
        print("  → Executar correções de banco de dados")

if __name__ == "__main__":
    main()