
import psycopg2
import os

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print("Listando clientes disponíveis para adoção de agentes órfãos:")
    cursor.execute("SELECT id, company_name, status FROM clients LIMIT 5;")
    clients = cursor.fetchall()
    
    for c in clients:
        print(f"ID: {c[0]} | Empresa: {c[1]} | Status: {c[2]}")
        
    if not clients:
        print("Nenhum cliente encontrado no banco!")

except Exception as e:
    print(f"Erro: {e}")
finally:
    if 'conn' in locals():
        conn.close()
