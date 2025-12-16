
import asyncio
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(dotenv_path="e:\\PROJETOS SITE\\Projeto Renum\\Projeto Site Renum\\renum_site\\.env")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("Error: credentials not found")
    exit()

supabase: Client = create_client(url, key)

async def check_system_agents():
    # Check if a 'Renus' or 'ISA' agent exists in the agents table
    response = supabase.table('agents').select('*').in_('name', ['Renus', 'ISA', 'Admin Assistant']).execute()
    
    print("\n--- System Agents in 'agents' table ---")
    if not response.data:
        print("No agents found with names Renus or ISA.")
    else:
        for agent in response.data:
            print(f"Found: {agent['name']} (ID: {agent['id']}) - Role: {agent.get('role', 'N/A')}")

    # Check renus_config table
    try:
        renus_response = supabase.table('renus_config').select('*').limit(1).execute()
        print("\n--- 'renus_config' table existence ---")
        if renus_response.data:
            print(f"Renus Config found for client: {renus_response.data[0]['client_id']}")
        else:
            print("Renus Config table is empty.")
    except Exception as e:
        print(f"Error checking renus_config: {e}")

if __name__ == "__main__":
    asyncio.run(check_system_agents())
