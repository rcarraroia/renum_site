#!/usr/bin/env python3
"""
Script para executar o SQL de criação das tabelas SICC diretamente no PostgreSQL
"""

import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def main():
    """Executa o script SQL para criar tabelas SICC"""
    
    # String de conexão direta ao PostgreSQL
    connection_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    print("🔧 Conectando ao PostgreSQL...")
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(connection_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Conectado com sucesso!")
        
        # Ler o arquivo SQL
        try:
            with open('scripts/create_sicc_tables.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
        except FileNotFoundError:
            print("❌ Arquivo create_sicc_tables.sql não encontrado!")
            return False
        
        print("📝 Executando script SQL completo...")
        
        # Executar o script completo
        try:
            cursor.execute(sql_content)
            print("✅ Script executado com sucesso!")
            
            # Verificar se as tabelas foram criadas
            print("\n🔍 Verificando tabelas criadas...")
            
            sicc_tables = ['memory_chunks', 'learning_logs', 'behavior_patterns', 'agent_snapshots', 'sicc_settings', 'agent_metrics']
            
            for table in sicc_tables:
                cursor.execute(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table}' AND table_schema = 'public'")
                exists = cursor.fetchone()[0] > 0
                
                if exists:
                    # Contar registros
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ {table} - {count} registros")
                else:
                    print(f"❌ {table} - NÃO ENCONTRADA")
            
            # Verificar configurações inseridas para agentes existentes
            print("\n📊 Verificando configurações SICC inseridas...")
            cursor.execute("SELECT COUNT(*) FROM sicc_settings")
            sicc_count = cursor.fetchone()[0]
            print(f"✅ {sicc_count} configurações SICC criadas")
            
            return True
            
        except psycopg2.Error as e:
            print(f"❌ Erro ao executar SQL: {e}")
            return False
            
    except psycopg2.Error as e:
        print(f"❌ Erro de conexão: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()
            print("🔌 Conexão fechada")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)