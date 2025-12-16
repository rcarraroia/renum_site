
import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis (se houver)
load_dotenv('backend/.env')

# Connection String Direta (conforme SUPABASE_CREDENTIALS.md validado)
# postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

print(f"Conectando ao Supabase (DB: {DATABASE_URL.split('@')[1]})...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False  # Transação manual
    cursor = conn.cursor()
    
    # Caminho do arquivo SQL
    migration_file = 'backend/migrations/20251213000000_unify_agents.sql'
    
    print(f"Lendo arquivo de migração: {migration_file}")
    with open(migration_file, 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    print("Executando migration SQL...")
    cursor.execute(migration_sql)
    
    # Validação 1: Contagem por Role
    print("\nVerificando roles criadas...")
    cursor.execute("""
        SELECT role, count(*) 
        FROM agents 
        GROUP BY role
        ORDER BY role;
    """)
    results = cursor.fetchall()
    
    roles_ok = False
    print("\n✅ PRE-COMMIT VALIDAÇÃO:")
    for role, count in results:
        print(f"  Role: {role} | Count: {count}")
        if role in ['system_orchestrator', 'system_supervisor']:
            roles_ok = True
            
    if not roles_ok:
        print("\n⚠️ AVISO: Roles de sistema não encontradas! Verifique o INSERT.")
    
    # Validação 2: Lista de Agentes
    cursor.execute("""
        SELECT id, role, name, config->>'model' as model
        FROM agents
        ORDER BY role, name;
    """)
    
    print("\n📋 Lista de Agentes (Snapshot):")
    agents_list = cursor.fetchall()
    for row in agents_list:
        print(f"  {row}")

    # Confirmar Transação
    conn.commit()
    print("\n✅ TRANSACTION COMMITTED - MIGRATION SUCESSO")
    
except Exception as e:
    print(f"\n❌ ERRO NA MIGRATION: {e}")
    if 'conn' in locals() and conn:
        conn.rollback()
        print("✓ ROLLBACK EXECUTADO - Banco preservado")
    raise
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
