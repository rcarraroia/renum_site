#!/usr/bin/env python3
"""
Execute migrations for Sprint 07A
Connects to Supabase and runs SQL migrations directly via psycopg2
"""
import os
import psycopg2

# Connection string
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def execute_sql_file(conn, filepath: str):
    """Execute SQL file"""
    # Remove backend/ prefix if present
    if filepath.startswith('backend/'):
        filepath = filepath.replace('backend/', '', 1)
    
    print(f"\n📄 Executando: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        
        print(f"✅ Migration executada com sucesso!")
        return True
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar migration: {e}")
        conn.rollback()
        return False

def main():
    print("=" * 80)
    print("🚀 EXECUTANDO MIGRATIONS - SPRINT 07A")
    print("=" * 80)
    
    # Conectar ao PostgreSQL
    print("\n📡 Conectando ao Supabase via PostgreSQL...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conectado!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # Migrations a executar
    migrations = [
        "migrations/007_create_integrations_table.sql",
        "migrations/008_create_triggers_table.sql",
        "migrations/009_create_trigger_executions_table.sql",
    ]
    
    print("\n" + "=" * 80)
    print("📋 EXECUTANDO MIGRATIONS")
    print("=" * 80)
    
    success_count = 0
    for migration in migrations:
        if execute_sql_file(conn, migration):
            success_count += 1
    
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"✅ {success_count}/{len(migrations)} MIGRATIONS EXECUTADAS COM SUCESSO")
    print("=" * 80)
    
    if success_count == len(migrations):
        print("\n🎉 Todas as migrations foram executadas!")
        print("\n📋 Próximos passos:")
        print("   1. Verificar tabelas criadas no Supabase")
        print("   2. Configurar frontend")
        print("   3. Configurar VPS (Redis + Celery)")
    else:
        print("\n⚠️  Algumas migrations falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main()
