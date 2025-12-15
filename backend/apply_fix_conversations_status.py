"""
Aplica fix no constraint de status de conversations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import psycopg2

print("=" * 60)
print("APLICANDO FIX: Status constraint de conversations")
print("=" * 60)

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

try:
    print("\n1. Conectando ao PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    print("   ✅ Conectado!")
    
    # 2. Remover constraint antigo
    print("\n2. Removendo constraint de status...")
    cur.execute("ALTER TABLE conversations DROP CONSTRAINT IF EXISTS conversations_status_check;")
    conn.commit()
    print("   ✅ Constraint removido!")
    
    # 3. Adicionar constraint correto
    print("\n3. Adicionando constraint correto...")
    cur.execute("""
        ALTER TABLE conversations ADD CONSTRAINT conversations_status_check 
        CHECK (status IN ('active', 'closed', 'pending'));
    """)
    conn.commit()
    print("   ✅ Constraint adicionado!")
    
    # 4. Verificar
    print("\n4. Verificando constraint...")
    cur.execute("""
        SELECT conname, pg_get_constraintdef(oid) 
        FROM pg_constraint 
        WHERE conrelid = 'conversations'::regclass 
        AND conname = 'conversations_status_check';
    """)
    result = cur.fetchone()
    if result:
        print(f"   ✅ Constraint: {result[0]}")
        print(f"   Definição: {result[1]}")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ FIX APLICADO COM SUCESSO!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    sys.exit(1)
