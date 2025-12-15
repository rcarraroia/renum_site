"""
Script para conectar diretamente ao PostgreSQL e investigar constraints
"""
import psycopg2

def investigate_clients_table():
    # Connection string
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    print("🔍 Conectando ao PostgreSQL...\n")
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("✅ Conectado!\n")
        
        # Query 1: Estrutura da tabela
        print("="*70)
        print("1️⃣ ESTRUTURA DA TABELA CLIENTS")
        print("="*70)
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
        
        print(f"\n{'Coluna':<25} {'Tipo':<20} {'Nullable':<10} {'Default'}")
        print("-"*70)
        for row in cursor.fetchall():
            print(f"{row[0]:<25} {row[1]:<20} {row[2]:<10} {str(row[3])[:20]}")
        
        # Query 2: Constraints
        print("\n" + "="*70)
        print("2️⃣ CONSTRAINTS DA TABELA CLIENTS")
        print("="*70)
        cursor.execute("""
            SELECT
                con.conname AS constraint_name,
                con.contype AS constraint_type,
                pg_get_constraintdef(con.oid) AS constraint_definition
            FROM pg_constraint con
            JOIN pg_class rel ON rel.oid = con.conrelid
            WHERE rel.relname = 'clients';
        """)
        
        constraints = cursor.fetchall()
        for row in constraints:
            print(f"\n📋 {row[0]}")
            print(f"   Tipo: {row[1]}")
            print(f"   Definição: {row[2]}")
        
        # Query 3: ENUMs relacionados a status
        print("\n" + "="*70)
        print("3️⃣ ENUMS RELACIONADOS A STATUS")
        print("="*70)
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
            current_enum = None
            for row in enums:
                if row[0] != current_enum:
                    current_enum = row[0]
                    print(f"\n📌 ENUM: {row[0]}")
                print(f"   - {row[1]}")
        else:
            print("\n⚠️ Nenhum ENUM encontrado")
        
        # Query 4: Ver o tipo exato da coluna status
        print("\n" + "="*70)
        print("4️⃣ TIPO EXATO DA COLUNA STATUS")
        print("="*70)
        cursor.execute("""
            SELECT 
                a.attname AS column_name,
                pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
                t.typname AS type_name
            FROM pg_attribute a
            JOIN pg_class c ON a.attrelid = c.oid
            JOIN pg_type t ON a.atttypid = t.oid
            WHERE c.relname = 'clients'
            AND a.attname = 'status';
        """)
        
        type_info = cursor.fetchone()
        if type_info:
            print(f"\nColuna: {type_info[0]}")
            print(f"Tipo formatado: {type_info[1]}")
            print(f"Tipo base: {type_info[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*70)
        print("✅ INVESTIGAÇÃO CONCLUÍDA")
        print("="*70)
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigate_clients_table()
