
import sys
import os
import asyncio
from dotenv import load_dotenv

# Configura paths
current_dir = os.getcwd() # e:\...\renum_site
backend_dir = os.path.join(current_dir, 'backend')
sys.path.append(backend_dir)

# Carrega ambiente
load_dotenv(os.path.join(backend_dir, '.env'))

# Mock para variáveis se não carregar do .env
if not os.getenv("DATABASE_URL"):
    print("WARNING: DATABASE_URL not found in .env, using default local")
    os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/renum_db"
if not os.getenv("SUPABASE_URL"):
    os.environ["SUPABASE_URL"] = "https://placeholder.supabase.co"
if not os.getenv("SUPABASE_KEY"):
    os.environ["SUPABASE_KEY"] = "placeholder"

try:
    from src.services.subagent_service import SubAgentService
    # Tenta importar models também para garantir conexao DB se service usar SQLModel/SQLAlchemy
    # from src.db.session import get_db 
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Sys Path: {sys.path}")
    sys.exit(1)

def main():
    try:
        print("Initializing Service...")
        service = SubAgentService()
        
        print("Listing Agents...")
        agents = service.list_all()
        
        print("-" * 50)
        print(f"Total Agents Found: {len(agents)}")
        print("-" * 50)
        renus_found = False
        
        for agent in agents:
            # agent é provavelmente um dict ou objeto retornado pelo supabase/sql
            # Se for dict:
            if isinstance(agent, dict):
                name = agent.get('name')
                slug = agent.get('slug')
                role = agent.get('role')
                aid = agent.get('id')
            else:
                # Se for objeto Pydantic/SQLModel
                name = getattr(agent, 'name', 'N/A')
                slug = getattr(agent, 'slug', 'N/A')
                role = getattr(agent, 'role', 'N/A')
                aid = getattr(agent, 'id', 'N/A')
                
            print(f"Name: {name}")
            print(f"Slug: {slug}")
            print(f"Role: {role}")
            print(f"ID: {aid}")
            print("-" * 30)
            
            if slug == 'renus':
                renus_found = True
        
        if not renus_found:
            print("ALERT: Agent with slug 'renus' NOT FOUND.")
            # TODO: Create if needed
            
    except Exception as e:
        print(f"Execution Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
