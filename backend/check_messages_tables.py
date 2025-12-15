import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Check for messages tables in all schemas
cur.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_name = 'messages'
    ORDER BY table_schema
""")

print("Messages tables found:")
for row in cur.fetchall():
    print(f"  {row[0]}.{row[1]}")

# Check which schema we're using
cur.execute("SELECT current_schema()")
print(f"\nCurrent schema: {cur.fetchone()[0]}")

# Check columns in public.messages
cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'messages'
    ORDER BY ordinal_position
""")

print("\nColumns in public.messages:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

cur.close()
conn.close()
