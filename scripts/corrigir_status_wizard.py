#!/usr/bin/env python3
"""
Script para adicionar coluna status à tabela agents
MISSÃO: Correção Wizard - PASSO 1
"""

import os
from supabase import create_client, Client

def executar_sql_direto(sql_command):
    """Executa comando SQL direto no Supabase"""
    print(f"🔧 Executando SQL: {sql_command}")
    
    url = 'https://vhixvzaxswphwoymdhgg.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw'
    
    try:
        supabase: Client = create_client(url, key)
        result = supabase.rpc('exec_sql', {'sql': sql_command}).execute()
        print(f"✅ SQL executado com sucesso")
        return True, result
    except Exception as e:
        print(f"❌ Erro executando SQL: {e}")
        return False, str(e)

def adicionar_coluna_status():
    """Adiciona coluna status à tabela agents"""
    print("🚀 PASSO 1: ADICIONANDO COLUNA STATUS")
    print("=" * 50)
    
    # 1. Criar enum agent_status
    print("\n1️⃣ Criando enum agent_status...")
    sql_enum = "CREATE TYPE agent_status AS ENUM ('draft', 'active', 'paused', 'inactive');"
    
    success, result = executar_sql_direto(sql_enum)
    if not success:
        if "already exists" in str(result):
            print("✅ Enum agent_status já existe")
        else:
            print(f"❌ Erro criando enum: {result}")
            return False
    
    # 2. Adicionar coluna status
    print("\n2️⃣ Adicionando coluna status...")
    sql_column = "ALTER TABLE agents ADD COLUMN IF NOT EXISTS status agent_status DEFAULT 'draft';"
    
    success, result = executar_sql_direto(sql_column)
    if not success:
        print(f"❌ Erro adicionando coluna: {result}")
        return False
    
    # 3. Atualizar agentes existentes
    print("\n3️⃣ Atualizando agentes existentes...")
    sql_update = "UPDATE agents SET status = 'draft' WHERE status IS NULL;"
    
    success, result = executar_sql_direto(sql_update)
    if not success:
        print(f"❌ Erro atualizando agentes: {result}")
        return False
    
    return True

def validar_correcao():
    """Valida se a correção foi aplicada corretamente"""
    print("\n4️⃣ Validando correção...")
    
    url = 'https://vhixvzaxswphwoymdhgg.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw'
    
    try:
        supabase: Client = create_client(url, key)
        
        # Verificar estrutura
        result = supabase.table('agents').select('*').limit(1).execute()
        
        if result.data:
            columns = list(result.data[0].keys())
            status_cols = [col for col in columns if 'status' in col.lower()]
            
            if status_cols:
                print(f"✅ Coluna status encontrada: {status_cols[0]}")
                
                # Verificar dados
                result_all = supabase.table('agents').select('id, name, status').execute()
                print(f"\n📊 Validação - Agentes com status ({len(result_all.data)}):")
                
                for agent in result_all.data:
                    status_val = agent.get('status', 'NULL')
                    name_val = agent.get('name', 'Sem nome')
                    print(f"  ✅ {name_val}: status = '{status_val}'")
                
                # Verificar se todos têm status
                null_status = [a for a in result_all.data if not a.get('status')]
                if null_status:
                    print(f"⚠️ {len(null_status)} agentes ainda com status NULL")
                    return False
                else:
                    print("✅ Todos os agentes têm status definido")
                    return True
            else:
                print("❌ Coluna status ainda não existe")
                return False
        else:
            print("⚠️ Tabela agents vazia")
            return True  # Se vazia, não há problema
            
    except Exception as e:
        print(f"❌ Erro validando: {e}")
        return False

def main():
    print("🎯 MISSÃO: Correção Wizard - PASSO 1")
    print("Objetivo: Adicionar coluna 'status' à tabela agents")
    print("Tempo estimado: 30 minutos")
    print("=" * 60)
    
    # Executar correção
    if adicionar_coluna_status():
        print("\n✅ CORREÇÃO APLICADA COM SUCESSO!")
        
        # Validar
        if validar_correcao():
            print("\n🎉 PASSO 1 CONCLUÍDO COM SUCESSO!")
            print("✅ Coluna 'status' adicionada")
            print("✅ Enum 'agent_status' criado")
            print("✅ Agentes existentes atualizados")
            print("\n🔄 PRÓXIMO PASSO: Testar wizard end-to-end")
            return True
        else:
            print("\n❌ VALIDAÇÃO FALHOU!")
            print("🚨 Correção não foi aplicada corretamente")
            return False
    else:
        print("\n❌ CORREÇÃO FALHOU!")
        print("🚨 Não foi possível adicionar coluna status")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)