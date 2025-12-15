
import asyncio
import os
from dotenv import load_dotenv

# Fix path to allow importing backend modules correctly
import sys
# Adicionar 'backend' ao path para que 'src' seja um módulo
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Ensure env vars are loaded for supabase connection
load_dotenv('backend/.env')

# Override Config with hardcoded credentials validated in Phase 1
os.environ["SUPABASE_URL"] = "https://vhixvzaxswphwoymdhgg.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# Import usando caminho completo 'src.services...'
from src.services.agent_service import get_agent_service
from src.models.agent import AgentRole, AgentCreate

async def verify():
    print("🚀 Iniciando Verificação do AgentService...")
    service = get_agent_service()
    
    # 1. Get Renus
    print("\n1. Buscando RENUS...")
    renus = await service.get_system_agent(AgentRole.SYSTEM_ORCHESTRATOR)
    if renus:
        print(f"✅ Renus encontrado: {renus.name} (ID: {renus.id})")
        print(f"   Model: {renus.model}")
    else:
        print("❌ Renus NÃO encontrado!")

    # 2. Get ISA
    print("\n2. Buscando ISA...")
    isa = await service.get_system_agent(AgentRole.SYSTEM_SUPERVISOR)
    if isa:
        print(f"✅ ISA encontrada: {isa.name} (ID: {isa.id})")
    else:
        print("❌ ISA NÃO encontrada!")
        
    # 3. Create Test Agent
    print("\n3. Criando Agente de Teste...")
    try:
        test_agent_data = AgentCreate(
            role=AgentRole.CLIENT_AGENT,
            name="Agente Teste Verificacao",
            description="Agente temporario para teste de integridade",
            is_active=True,
            config={"model": "gpt-4o-mini", "channel": "web", "system_prompt": "You are a test agent."},
            # Client ID fake or real? Need a valid UUID or None if schema allows nullable for CLIENT_AGENT?
            # Schema says client_id REFERENCES clients. It is nullable in model but foreign key constraint exists?
            # Let's check schema: client_id UUID REFERENCES clients... ON DELETE CASCADE. Not NOT NULL explicitly in CREATE TABLE?
            # Wait, migration said: client_id UUID REFERENCES clients...
            # If I pass None, it works if column is nullable.
            # But let's try with a random UUID if we don't have a real client? No, FK violation.
            # I must use a REAL client ID. I don't have one handy unless I list them.
            # Or I can try to create a System Agent (no client_id needed constraint?).
            # Let's try creating a SYSTEM_SUPERVISOR test agent which allows null client_id usually.
            is_public=False
        )
        # Hack: Schema definition in migration 20251213000000:
        # parent_id UUID REFERENCES agents...
        # role agent_role NOT NULL
        # client_id UUID REFERENCES clients(id) ON DELETE CASCADE
        # It doesn't say NOT NULL for client_id. So None should be valid.
        
        created_agent = await service.create_agent(test_agent_data)
        print(f"✅ Agente criado: {created_agent.name} (ID: {created_agent.id})")
        created_id = created_agent.id
    except Exception as e:
        print(f"❌ Falha ao criar agente: {e}")
        created_id = None

    # 4. List Agents
    print("\n4. Listando Agentes...")
    agents = await service.list_agents(limit=5)
    for a in agents:
        print(f"   - {a.name} ({a.role})")
        
    # 5. Delete Test Agent
    if created_id:
        print(f"\n5. Deletando Agente de Teste ({created_id})...")
        try:
            success = await service.delete_agent(created_id)
            if success:
                print("✅ Agente deletado com sucesso.")
            else:
                print("❌ Falha na deleção.")
        except Exception as e:
            print(f"❌ Erro ao deletar: {e}")

    print("\n✅ Verificação Concluída.")

if __name__ == "__main__":
    asyncio.run(verify())
