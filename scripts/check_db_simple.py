#!/usr/bin/env python3
"""
Script simples para verificar estrutura do banco Supabase
"""

import os
import sys
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def main():
    print("🔍 Verificando estrutura do banco Supabase...")
    
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # 1. Verificar tabela leads
        print("\n📋 Estrutura da tabela 'leads':")
        try:
            # Tentar buscar um registro para ver as colunas
            result = supabase.table('leads').select('*').limit(1).execute()
            if result.data:
                print("  Colunas encontradas:", list(result.data[0].keys()))
            else:
                print("  Tabela vazia, tentando inserir teste...")
                # Tentar inserir para ver quais colunas são aceitas
                test_data = {
                    'name': 'Teste',
                    'phone': '+5511999999999',
                    'email': 'teste@teste.com'
                }
                try:
                    supabase.table('leads').insert(test_data).execute()
                    print("  ✅ Inserção básica funcionou")
                except Exception as e:
                    print(f"  ❌ Erro na inserção: {e}")
        except Exception as e:
            print(f"  ❌ Erro ao acessar tabela leads: {e}")
        
        # 2. Verificar tabela messages
        print("\n💬 Estrutura da tabela 'messages':")
        try:
            result = supabase.table('messages').select('*').limit(1).execute()
            if result.data:
                print("  Colunas encontradas:", list(result.data[0].keys()))
            else:
                print("  Tabela vazia")
        except Exception as e:
            print(f"  ❌ Erro ao acessar tabela messages: {e}")
        
        # 3. Verificar tabela interview_messages
        print("\n🎤 Estrutura da tabela 'interview_messages':")
        try:
            result = supabase.table('interview_messages').select('*').limit(1).execute()
            if result.data:
                print("  Colunas encontradas:", list(result.data[0].keys()))
            else:
                print("  Tabela vazia")
        except Exception as e:
            print(f"  ❌ Erro ao acessar tabela interview_messages: {e}")
        
        # 4. Verificar tabela sub_agents
        print("\n🤖 Estrutura da tabela 'sub_agents':")
        try:
            result = supabase.table('sub_agents').select('*').limit(1).execute()
            if result.data:
                print("  Colunas encontradas:", list(result.data[0].keys()))
                print(f"  Total de sub-agentes: {len(result.data)}")
            else:
                print("  Tabela vazia")
        except Exception as e:
            print(f"  ❌ Erro ao acessar tabela sub_agents: {e}")
        
        # 5. Verificar tabela renus_config (agentes principais)
        print("\n⚙️ Estrutura da tabela 'renus_config':")
        try:
            result = supabase.table('renus_config').select('*').limit(1).execute()
            if result.data:
                print("  Colunas encontradas:", list(result.data[0].keys()))
                print(f"  Total de configurações: {len(result.data)}")
            else:
                print("  Tabela vazia")
        except Exception as e:
            print(f"  ❌ Erro ao acessar tabela renus_config: {e}")
        
        print("\n✅ Verificação concluída!")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()