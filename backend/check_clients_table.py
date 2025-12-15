import psycopg2

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("Columns in 'clients' table:")
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'clients' 
    ORDER BY ordinal_position;
""")

for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

cur.close()
conn.close()
