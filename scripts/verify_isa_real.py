
import asyncio
import os
import sys
from dotenv import load_dotenv

# Configurar Path para encontrar módulos do backend
sys.path.append(os.path.join(os.getcwd(), 'backend'))

load_dotenv('backend/.env')

# Override Config
os.environ["SUPABASE_URL"] = "https://vhixvzaxswphwoymdhgg.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# Imports
from src.services.agent_service import get_agent_service
from src.models.agent import AgentRole
from src.agents.isa import IsaAgent
from langchain_core.messages import HumanMessage

async def verify_isa():
    print("🚀 Verificando ISA Real (Backend)...")
    
    # 1. Fetch from DB
    print("\n1. Buscando config no Banco via AgentService...")
    service = get_agent_service()
    db_agent = await service.get_system_agent(AgentRole.SYSTEM_SUPERVISOR)
    
    if not db_agent:
        print("❌ CRÍTICO: ISA não encontrada no banco!")
        return
        
    print(f"✅ ISA encontrada no DB.")
    print(f"   ID: {db_agent.id}")
    print(f"   Model (DB): {db_agent.model}")
    print(f"   Prompt Size: {len(db_agent.system_prompt)} chars")

    # 2. Instantiate Agent
    print("\n2. Instanciando IsaAgent com config do DB...")
    # Aqui simulamos o que a rota faz
    isa = IsaAgent(
        model=db_agent.model,
        system_prompt=db_agent.system_prompt
    )
    
    print(f"✅ Instância criada.")
    print(f"   Model (Instance): {isa.model}")
    
    if isa.model != db_agent.model:
        print("❌ ALERTA: Modelo da instância difere do Banco! O fallback foi usado indevidamente?")
    else:
        print("✅ Configuração injetada corretamente.")

    # 3. Test Invoke
    print("\n3. Testando Invoke (Simulação de Chat)...")
    print("   Msg: 'Quem é você e qual seu modelo?'")
    
    # Criar um contexto fake de admin
    context = {
        "admin_id": "00000000-0000-0000-0000-000000000000",
        "is_admin": True,
        "client_id": None
    }
    
    try:
        # Nota: O invoke real checa settings.OPENAI_API_KEY.
        # Precisamos garantir que está setada? O BaseAgent usa.
        # Se falhar por falta de key, tudo bem, o importante é chegar até a tentativa de chamada.
        
        # Vamos mockar o llm.invoke se não tiver key, mas melhor tentar real se tiver key no .env
        # O BaseAgent inicializa ChatOpenAI. Se a key não estiver no env do processo, vai falhar na init.
        # Mas IsaAgent init passou (passo 2). Então ChatOpenAI foi criado.
        
        messages = [HumanMessage(content="Quem é você e qual seu modelo?")]
        result = await isa.invoke(messages, context)
        
        print("\n📝 Resposta da ISA:")
        print(f"   {result.get('response')}")
        print(f"   Command Type: {result.get('command_type')}")
        
        if result.get('error'):
             print(f"❌ Erro na execução: {result.get('error')}")
        else:
             print("✅ Execução bem sucedida!")
             
    except Exception as e:
        print(f"❌ Erro ao invocar agente: {e}")
        print("   (Verifique se OPENAI_API_KEY está configurada no .env)")

if __name__ == "__main__":
    asyncio.run(verify_isa())
