
import sys
import os

# Adiciona o diretório atual ao path para importar módulos
sys.path.append(os.path.join(os.getcwd(), 'backend', 'src'))

# Mock para evitar erros de importação se as variáveis de ambiente não estiverem setadas
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/renum_db" # Ajuste se necessário

try:
    from backend.src.services.subagent_service import SubAgentService
    
    service = SubAgentService()
    agents = service.list_all()
    
    print("-" * 50)
    print(f"Total Agents Found: {len(agents)}")
    print("-" * 50)
    for agent in agents:
        print(f"Name: {agent.get('name')}")
        print(f"Slug: {agent.get('slug')}")
        print(f"Role: {agent.get('role')}")
        print(f"ID: {agent.get('id')}")
        print("-" * 30)

except Exception as e:
    print(f"Error: {e}")
