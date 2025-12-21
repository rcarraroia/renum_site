import psycopg2
import sys

# Connection string from credentials file
DB_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def check_schema():
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("Querying columns for 'agents' table...")
        cur.execute("""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'agents'
            ORDER BY column_name;
        """)
        
        columns = cur.fetchall()
        print(f"\nFound {len(columns)} columns in 'agents' table:")
        print("-" * 60)
        print(f"{'Column Name':<30} | {'Type':<15} | {'Default'}")
        print("-" * 60)
        
        found_target_columns = []
        target_columns = ['template_type', 'category', 'is_public', 'marketplace_visible', 'system_prompt']
        
        for col in columns:
            name, dtype, default = col
            print(f"{name:<30} | {dtype:<15} | {default}")
            if name in target_columns:
                found_target_columns.append(name)
        
        print("-" * 60)
        
        missing = set(target_columns) - set(found_target_columns)
        if missing:
            print(f"\n❌ MISSING COLUMNS: {missing}")
        else:
            print("\n✅ All target columns found in database.")

        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error checking schema: {e}")
        return False

if __name__ == "__main__":
    check_schema()
