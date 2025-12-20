"""
Script para executar migration diretamente no banco REAL do Supabase
Usa psycopg2 para conexão direta ao PostgreSQL
"""
import os
import sys
from pathlib import Path

# Tentar importar psycopg2
try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("❌ psycopg2 não instalado!")
    print("Instale com: pip install psycopg2-binary")
    sys.exit(1)

# Importar dotenv para ler .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv não instalado, usando variáveis de ambiente do sistema")

def get_db_connection_string():
    """Monta string de conexão do Supabase"""
    # Tentar obter de diferentes fontes
    
    # Opção 1: DATABASE_URL completa
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        return db_url
    
    # Opção 2: Componentes separados
    host = os.getenv('SUPABASE_DB_HOST') or os.getenv('DB_HOST')
    port = os.getenv('SUPABASE_DB_PORT') or os.getenv('DB_PORT') or '5432'
    database = os.getenv('SUPABASE_DB_NAME') or os.getenv('DB_NAME') or 'postgres'
    user = os.getenv('SUPABASE_DB_USER') or os.getenv('DB_USER') or 'postgres'
    password = os.getenv('SUPABASE_DB_PASSWORD') or os.getenv('DB_PASSWORD')
    
    if not all([host, password]):
        return None
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def execute_migration():
    """Executa a migration no banco real"""
    print("=" * 60)
    print("EXECUTANDO MIGRATION NO BANCO REAL DO SUPABASE")
    print("=" * 60)
    
    # Obter string de conexão
    conn_string = get_db_connection_string()
    
    if not conn_string:
        print("\n❌ ERRO: Credenciais do banco não encontradas!")
        print("\nOpções:")
        print("1. Definir DATABASE_URL no .env")
        print("2. Definir SUPABASE_DB_HOST e SUPABASE_DB_PASSWORD no .env")
        print("\nOu execute manualmente no Supabase Dashboard:")
        print("https://app.supabase.com → SQL Editor → Colar SQL")
        return False
    
    # Ler arquivo de migration
    migration_file = Path(__file__).parent.parent / 'migrations' / '015_add_template_fields.sql'
    
    if not migration_file.exists():
        print(f"\n❌ ERRO: Arquivo de migration não encontrado!")
        print(f"Esperado em: {migration_file}")
        return False
    
    with open(migration_file, 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    print(f"\n📄 Migration: {migration_file.name}")
    print(f"📏 Tamanho: {len(migration_sql)} caracteres")
    
    # Conectar ao banco
    try:
        print("\n🔌 Conectando ao Supabase...")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("✅ Conectado com sucesso!")
        
        # Executar migration
        print("\n⚙️ Executando migration...")
        cursor.execute(migration_sql)
        conn.commit()
        
        print("✅ Migration executada com sucesso!")
        
        # Validar campos criados
        print("\n🔍 Validando campos criados...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'agents'
            AND column_name IN (
                'is_template',
                'category',
                'niche',
                'marketplace_visible',
                'available_tools',
                'available_integrations'
            )
            ORDER BY column_name;
        """)
        
        campos = cursor.fetchall()
        
        if len(campos) == 6:
            print(f"✅ {len(campos)} campos criados com sucesso:")
            for campo in campos:
                print(f"  - {campo[0]} ({campo[1]})")
        else:
            print(f"⚠️ Esperado 6 campos, encontrado {len(campos)}")
        
        # Validar índices
        print("\n🔍 Validando índices criados...")
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'agents'
            AND (
                indexname LIKE '%template%'
                OR indexname LIKE '%marketplace%'
                OR indexname LIKE '%category%'
                OR indexname LIKE '%niche%'
            )
            ORDER BY indexname;
        """)
        
        indices = cursor.fetchall()
        print(f"✅ {len(indices)} índices criados:")
        for indice in indices:
            print(f"  - {indice[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ MIGRATION CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("\n📋 Próximos passos:")
        print("1. Reiniciar backend (se estiver rodando)")
        print("2. Acessar: http://localhost:8081/dashboard/admin/agents/templates")
        print("3. Criar primeiro template via Wizard")
        
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ ERRO ao executar migration:")
        print(f"Código: {e.pgcode}")
        print(f"Mensagem: {e.pgerror}")
        
        if "already exists" in str(e):
            print("\n⚠️ Campos já existem! Migration já foi executada anteriormente.")
            return True
        
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")
        return False

if __name__ == "__main__":
    success = execute_migration()
    sys.exit(0 if success else 1)
