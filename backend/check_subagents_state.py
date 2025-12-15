#!/usr/bin/env python3
"""
Check current state of sub_agents table
"""
import psycopg2

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("=" * 80)
print("ESTADO ATUAL DE SUB_AGENTS")
print("=" * 80)

# Contar total
cursor.execute("SELECT COUNT(*) FROM sub_agents")
total = cursor.fetchone()[0]
print(f"\nTotal de registros: {total}")

# Contar com client_id
cursor.execute("SELECT COUNT(*) FROM sub_agents WHERE client_id IS NOT NULL")
with_client = cursor.fetchone()[0]
print(f"Com client_id: {with_client}")

# Contar sem client_id
cursor.execute("SELECT COUNT(*) FROM sub_agents WHERE client_id IS NULL")
without_client = cursor.fetchone()[0]
print(f"Sem client_id: {without_client}")

# Mostrar alguns registros
cursor.execute("SELECT id, name, client_id FROM sub_agents LIMIT 5")
records = cursor.fetchall()
print(f"\nPrimeiros 5 registros:")
for r in records:
    print(f"  - {r[1]} (client_id: {r[2]})")

# Verificar se coluna agent_id existe
cursor.execute("""
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'sub_agents' AND column_name = 'agent_id'
    )
""")
has_agent_id = cursor.fetchone()[0]
print(f"\nColuna agent_id existe: {has_agent_id}")

# Contar agents
cursor.execute("SELECT COUNT(*) FROM agents")
agents_count = cursor.fetchone()[0]
print(f"Total de agents: {agents_count}")

cursor.close()
conn.close()

print("=" * 80)
