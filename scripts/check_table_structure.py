#!/usr/bin/env python3
"""
Script para verificar a estrutura real das tabelas no Supabase
"""

import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def main():
    """Verifica a estrutura das tabelas existentes"""
    
    # String de conexão direta ao PostgreSQL
    connection_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    print("🔧 Conectando ao PostgreSQL...")
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(connection_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Conectado com sucesso!")
        
        # Verificar estrutura das tabelas principais
        tables_to_check = ['profiles', 'clients', 'agents']
        
        for table in tables_to_check:
            print(f"\n📋 Estrutura da tabela '{table}':")
            print("-" * 50)
            
            cursor.execute(f"""
                SELECT 
                    column_name, 
                    data_type, 
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            
            columns = cursor.fetchall()
            
            if columns:
                for col in columns:
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    default = f" DEFAULT {col[3]}" if col[3] else ""
                    print(f"  {col[0]:<20} {col[1]:<15} {nullable}{default}")
            else:
                print(f"  ❌ Tabela '{table}' não encontrada")
        
        # Verificar se existe função update_updated_at_column
        print(f"\n🔧 Verificando função update_updated_at_column:")
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM pg_proc 
                WHERE proname = 'update_updated_at_column'
            )
        """)
        
        function_exists = cursor.fetchone()[0]
        if function_exists:
            print("✅ Função update_updated_at_column existe")
        else:
            print("❌ Função update_updated_at_column NÃO existe")
            
        return True
            
    except psycopg2.Error as e:
        print(f"❌ Erro: {e}")
        return False
        
    finally:
        if 'conn' in locals():
            conn.close()
            print("\n🔌 Conexão fechada")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)