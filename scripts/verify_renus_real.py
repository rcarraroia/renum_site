
import asyncio
import os
import sys
from dotenv import load_dotenv

# Configurar Path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

load_dotenv('backend/.env')

# Re-aplicar overrides de conexão se necessário (garantia)
os.environ["SUPABASE_URL"] = "https://vhixvzaxswphwoymdhgg.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

from src.services.agent_service import get_agent_service
from src.models.agent import AgentRole
from src.agents.renus import RenusAgent
from langchain_core.messages import HumanMessage

async def verify_renus():
    print("🚀 Verificando RENUS Real (Backend)...")
    
    # 1. Fetch from DB
    print("\n1. Buscando config no Banco via AgentService...")
    service = get_agent_service()
    db_agent = await service.get_system_agent(AgentRole.SYSTEM_ORCHESTRATOR)
    
    if not db_agent:
        print("❌ CRÍTICO: RENUS não encontrado no banco!")
        return
        
    print(f"✅ RENUS encontrado no DB.")
    print(f"   ID: {db_agent.id}")
    print(f"   Model (DB): {db_agent.model}")
    print(f"   Prompt Size: {len(db_agent.system_prompt)} chars")

    # 2. Instantiate Agent
    print("\n2. Instanciando RenusAgent com config do DB...")
    renus = RenusAgent(
        model=db_agent.model,
        system_prompt=db_agent.system_prompt
    )
    
    print(f"✅ Instância criada.")
    print(f"   Model (Instance): {renus.model}")
    
    if renus.model != db_agent.model:
        print("❌ ALERTA: Modelo da instância difere do Banco!")

    # 3. Test Invoke (General Chat)
    print("\n3. Testando Invoke (General Chat)...")
    print("   Msg: 'Quem é você e qual seu modelo?'")
    
    context = {
        "client_id": None, # System context
        "user_id": "tester"
    }
    
    try:
        messages = [HumanMessage(content="Quem é você e qual seu modelo?")]
        result = await renus.invoke(messages, context)
        
        print("\n📝 Resposta do RENUS:")
        print(f"   {result.get('response')}")
        print(f"   Intent: {result.get('intent')}")
        
        if result.get('intent') == 'general':
             print("✅ Intent 'general' detectado corretamente.")
        else:
             print(f"⚠️ Intent inesperado: {result.get('intent')}")

    except Exception as e:
        print(f"❌ Erro ao invocar agente: {e}")

if __name__ == "__main__":
    asyncio.run(verify_renus())
