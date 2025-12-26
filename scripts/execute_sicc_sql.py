#!/usr/bin/env python3
"""
Script para executar o SQL de criação das tabelas SICC no Supabase
"""

import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def main():
    """Executa o script SQL para criar tabelas SICC"""
    
    # Configurar cliente Supabase
    url = "https://vhixvzaxswphwoymdhgg.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"
    
    supabase: Client = create_client(url, key)
    
    print("🔧 Executando criação das tabelas SICC...")
    
    # Ler o arquivo SQL
    try:
        with open('scripts/create_sicc_tables.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
    except FileNotFoundError:
        print("❌ Arquivo create_sicc_tables.sql não encontrado!")
        return False
    
    # Dividir o SQL em comandos individuais
    sql_commands = []
    current_command = ""
    
    for line in sql_content.split('\n'):
        line = line.strip()
        
        # Pular comentários e linhas vazias
        if not line or line.startswith('--'):
            continue
            
        current_command += line + " "
        
        # Se a linha termina com ';', é o fim de um comando
        if line.endswith(';'):
            sql_commands.append(current_command.strip())
            current_command = ""
    
    print(f"📝 Encontrados {len(sql_commands)} comandos SQL para executar")
    
    # Executar cada comando
    success_count = 0
    error_count = 0
    
    for i, command in enumerate(sql_commands, 1):
        if not command or command == ';':
            continue
            
        try:
            print(f"⚡ Executando comando {i}/{len(sql_commands)}...")
            
            # Usar rpc para executar SQL bruto
            result = supabase.rpc('exec_sql', {'query': command}).execute()
            
            print(f"✅ Comando {i} executado com sucesso")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Erro no comando {i}: {str(e)}")
            error_count += 1
            
            # Se for erro de função não encontrada, tentar método alternativo
            if "exec_sql" in str(e):
                print("🔄 Tentando método alternativo...")
                try:
                    # Tentar usar postgrest diretamente
                    response = supabase.postgrest.rpc('exec_sql', {'query': command}).execute()
                    print(f"✅ Comando {i} executado com método alternativo")
                    success_count += 1
                    error_count -= 1
                except Exception as e2:
                    print(f"❌ Método alternativo também falhou: {str(e2)}")
    
    print(f"\n📊 Resumo da execução:")
    print(f"✅ Comandos executados com sucesso: {success_count}")
    print(f"❌ Comandos com erro: {error_count}")
    
    if error_count == 0:
        print("\n🎉 Todas as tabelas SICC foram criadas com sucesso!")
        
        # Verificar se as tabelas foram criadas
        print("\n🔍 Verificando tabelas criadas...")
        try:
            result = supabase.table('information_schema.tables').select('table_name').eq('table_schema', 'public').execute()
            tables = [row['table_name'] for row in result.data]
            
            sicc_tables = ['memory_chunks', 'learning_logs', 'behavior_patterns', 'agent_snapshots', 'sicc_settings', 'agent_metrics']
            
            for table in sicc_tables:
                if table in tables:
                    print(f"✅ {table}")
                else:
                    print(f"❌ {table} - NÃO ENCONTRADA")
                    
        except Exception as e:
            print(f"⚠️ Não foi possível verificar as tabelas: {str(e)}")
        
        return True
    else:
        print(f"\n⚠️ Alguns comandos falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)