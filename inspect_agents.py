
import psycopg2
import os

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("Inspecionando tabela 'agents' existente...")
try:
    # Ver colunas
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'agents';
    """)
    columns = cursor.fetchall()
    print("\nColunas encontradas:")
    for col in columns:
        print(f"  {col}")

    # Ver contagem de dados
    cursor.execute("SELECT count(*) FROM agents;")
    count = cursor.fetchone()[0]
    print(f"\nTotal de registros: {count}")
    
    if count > 0:
        cursor.execute("SELECT * FROM agents LIMIT 5;")
        print("\nAmostra de dados:")
        print(cursor.fetchall())

except Exception as e:
    print(f"Erro: {e}")
finally:
    conn.close()
