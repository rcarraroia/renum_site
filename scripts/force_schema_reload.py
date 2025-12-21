import psycopg2
import sys

# Connection string from credentials file
DB_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def reload_schema():
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Executing NOTIFY pgrst, 'reload schema'...")
        cur.execute("NOTIFY pgrst, 'reload schema';")
        
        print("Schema reload notification sent successfully.")
        cur.close()
        conn.close()
        return True
    except ImportError:
        print("Error: psycopg2 module not found. Please install it with 'pip install psycopg2-binary'")
        return False
    except Exception as e:
        print(f"Error executing schema reload: {e}")
        return False

if __name__ == "__main__":
    success = reload_schema()
    if not success:
        sys.exit(1)
