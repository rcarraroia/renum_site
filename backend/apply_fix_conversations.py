"""
Aplica fix no constraint de conversations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.supabase import supabase_admin
import psycopg2

print("=" * 60)
print("APLICANDO FIX: Constraint de conversations")
print("=" * 60)

# Conectar diretamente ao PostgreSQL
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

try:
    print("\n1. Conectando ao PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    print("   ✅ Conectado!")
    
    # 2. Remover constraint antigo
    print("\n2. Removendo constraint problemático...")
    cur.execute("ALTER TABLE conversations DROP CONSTRAINT IF EXISTS conversations_channel_check;")
    conn.commit()
    print("   ✅ Constraint removido!")
    
    # 3. Adicionar constraint correto
    print("\n3. Adicionando constraint correto...")
    cur.execute("""
        ALTER TABLE conversations ADD CONSTRAINT conversations_channel_check 
        CHECK (channel IN ('whatsapp', 'email', 'web', 'sms', 'telegram', 'phone'));
    """)
    conn.commit()
    print("   ✅ Constraint adicionado!")
    
    # 4. Verificar
    print("\n4. Verificando constraint...")
    cur.execute("""
        SELECT conname, pg_get_constraintdef(oid) 
        FROM pg_constraint 
        WHERE conrelid = 'conversations'::regclass 
        AND conname = 'conversations_channel_check';
    """)
    result = cur.fetchone()
    if result:
        print(f"   ✅ Constraint: {result[0]}")
        print(f"   Definição: {result[1]}")
    else:
        print("   ⚠️ Constraint não encontrado")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ FIX APLICADO COM SUCESSO!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\nPor favor, execute manualmente no Supabase SQL Editor:")
    print("ALTER TABLE conversations DROP CONSTRAINT IF EXISTS conversations_channel_check;")
    print("ALTER TABLE conversations ADD CONSTRAINT conversations_channel_check")
    print("CHECK (channel IN ('whatsapp', 'email', 'web', 'sms', 'telegram', 'phone'));")
    sys.exit(1)
