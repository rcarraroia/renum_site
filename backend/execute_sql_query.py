"""
Script para executar queries SQL diretamente no Supabase
"""
from src.config.supabase import supabase_admin
import json

def execute_query(query, description):
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}\n")
    
    try:
        # Usar rpc para executar SQL (se disponível)
        # Caso contrário, precisaremos usar psycopg2 diretamente
        
        # Vamos tentar uma abordagem diferente: usar a API REST do PostgREST
        # para fazer queries mais complexas
        
        print(f"Query:\n{query}\n")
        print("⚠️ Não é possível executar SQL arbitrário via Supabase client Python")
        print("📝 SOLUÇÃO: Copie a query acima e execute no Supabase Dashboard → SQL Editor")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    # Ler arquivo SQL
    with open('query_constraint.sql', 'r', encoding='utf-8') as f:
        queries = f.read()
    
    print("\n" + "="*60)
    print("📋 QUERIES PARA EXECUTAR NO SUPABASE DASHBOARD")
    print("="*60)
    print("\n1. Acesse: https://supabase.com/dashboard")
    print("2. Selecione o projeto RENUM")
    print("3. Vá em SQL Editor")
    print("4. Execute as queries abaixo:\n")
    print("-"*60)
    print(queries)
    print("-"*60)
    
    # Vamos tentar uma abordagem alternativa: conectar via psycopg2
    print("\n\n🔧 Tentando conexão direta via psycopg2...\n")
    
    try:
        import psycopg2
        from src.config.settings import settings
        
        # Construir connection string
        conn_string = f"postgresql://postgres:{settings.SUPABASE_DB_PASSWORD}@db.{settings.SUPABASE_URL.split('//')[1].split('.')[0]}.supabase.co:5432/postgres"
        
        print(f"Conectando em: {conn_string[:50]}...")
        
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        # Query 1: Estrutura da tabela
        print("\n1️⃣ ESTRUTURA DA TABELA CLIENTS:")
        print("-"*60)
        cursor.execute("""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'clients'
            ORDER BY ordinal_position;
        """)
        
        for row in cursor.fetchall():
            print(f"   {row[0]:20} | {row[1]:15} | Nullable: {row[2]:3} | Default: {row[3]}")
        
        # Query 2: Constraints
        print("\n2️⃣ CONSTRAINTS:")
        print("-"*60)
        cursor.execute("""
            SELECT
                con.conname AS constraint_name,
                con.contype AS constraint_type,
                pg_get_constraintdef(con.oid) AS constraint_definition
            FROM pg_constraint con
            JOIN pg_class rel ON rel.oid = con.conrelid
            WHERE rel.relname = 'clients';
        """)
        
        for row in cursor.fetchall():
            print(f"\n   Nome: {row[0]}")
            print(f"   Tipo: {row[1]}")
            print(f"   Definição: {row[2]}")
        
        # Query 3: ENUMs
        print("\n3️⃣ ENUMS RELACIONADOS A STATUS:")
        print("-"*60)
        cursor.execute("""
            SELECT 
                t.typname AS enum_name,
                e.enumlabel AS enum_value
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid  
            WHERE t.typname LIKE '%status%'
            ORDER BY t.typname, e.enumsortorder;
        """)
        
        enums = cursor.fetchall()
        if enums:
            for row in enums:
                print(f"   {row[0]}: {row[1]}")
        else:
            print("   (Nenhum ENUM encontrado)")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Queries executadas com sucesso!")
        
    except ImportError:
        print("❌ psycopg2 não está instalado")
        print("📝 Instale com: pip install psycopg2-binary")
    except AttributeError as e:
        print(f"❌ Falta configuração: {e}")
        print("📝 Adicione SUPABASE_DB_PASSWORD no .env")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print("\n📝 SOLUÇÃO ALTERNATIVA:")
        print("Execute as queries manualmente no Supabase Dashboard")

if __name__ == "__main__":
    main()
