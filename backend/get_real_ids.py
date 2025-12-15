import psycopg2

conn = psycopg2.connect('postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres')
cursor = conn.cursor()

# Get a real client_id
cursor.execute("SELECT id FROM clients LIMIT 1;")
result = cursor.fetchone()
if result:
    print(f"client_id: {result[0]}")
else:
    print("No clients found - need to create one first")

# Get a real agent_id
cursor.execute("SELECT id, client_id FROM agents LIMIT 1;")
result = cursor.fetchone()
if result:
    print(f"agent_id: {result[0]}")
    print(f"agent's client_id: {result[1]}")
else:
    print("No agents found - need to create one first")

cursor.close()
conn.close()
