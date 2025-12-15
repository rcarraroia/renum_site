
from src.config.supabase import supabase_admin
import asyncio

async def check_tables():
    print("Checking tables...")
    try:
        # Check agent_documents
        try:
            supabase_admin.table('agent_documents').select('id').limit(1).execute()
            print("Table 'agent_documents': EXISTS")
        except Exception as e:
            print(f"Table 'agent_documents': MISSING ({e})")

        # Check agent_knowledge
        try:
            supabase_admin.table('agent_knowledge').select('id').limit(1).execute()
            print("Table 'agent_knowledge': EXISTS")
        except Exception as e:
            print(f"Table 'agent_knowledge': MISSING ({e})")
            
    except Exception as e:
        print(f"General Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_tables())
