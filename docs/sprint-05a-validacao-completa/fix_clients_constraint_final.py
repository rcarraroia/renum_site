"""
Script para corrigir o constraint da tabela clients
"""
import psycopg2

def fix_constraint():
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    print("🔧 Corrigindo constraint da tabela clients...\n")
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("✅ Conectado ao PostgreSQL\n")
        
        # Passo 1: Remover constraint antigo
        print("1️⃣ Removendo constraint antigo...")
        cursor.execute("""
            ALTER TABLE clients 
            DROP CONSTRAINT IF EXISTS clients_status_check;
        """)
        print("   ✅ Constraint antigo removido\n")
        
        # Passo 2: Adicionar novo constraint com valores em inglês
        print("2️⃣ Adicionando novo constraint...")
        cursor.execute("""
            ALTER TABLE clients 
            ADD CONSTRAINT clients_status_check 
            CHECK (status = ANY (ARRAY['active'::text, 'inactive'::text, 'suspended'::text]));
        """)
        print("   ✅ Novo constraint adicionado\n")
        
        # Passo 3: Commit
        conn.commit()
        print("3️⃣ Commit realizado\n")
        
        # Passo 4: Verificar
        print("4️⃣ Verificando novo constraint...")
        cursor.execute("""
            SELECT pg_get_constraintdef(con.oid) AS constraint_definition
            FROM pg_constraint con
            JOIN pg_class rel ON rel.oid = con.conrelid
            WHERE rel.relname = 'clients'
            AND con.conname = 'clients_status_check';
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"   ✅ Constraint verificado: {result[0]}\n")
        
        cursor.close()
        conn.close()
        
        print("="*70)
        print("✅ CONSTRAINT CORRIGIDO COM SUCESSO!")
        print("="*70)
        print("\nValores aceitos agora:")
        print("  - 'active'")
        print("  - 'inactive'")
        print("  - 'suspended'")
        print("\n📝 Próximo passo: Testar criação de cliente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_constraint()
    exit(0 if success else 1)
