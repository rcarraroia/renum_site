"""
Teste ISA com contexto de admin para verificar se acessa banco REAL
"""
import asyncio
from langchain_core.messages import HumanMessage
from src.agents.isa import IsaAgent
from src.utils.supabase_client import get_client

async def test_isa_real():
    print("\n🔍 TESTE CRÍTICO: ISA acessa banco REAL ou usa MOCK?")
    print("="*70 + "\n")
    
    # Verificar dados reais no banco
    supabase = get_client()
    real_clients = supabase.table('clients').select('id, company_name').limit(5).execute().data
    real_leads = supabase.table('leads').select('id, name').limit(5).execute().data
    
    print(f"📊 Dados REAIS no banco:")
    print(f"   Clientes: {len(real_clients)}")
    print(f"   Leads: {len(real_leads)}")
    
    if real_clients:
        print(f"   Exemplo cliente: {real_clients[0].get('company_name', 'N/A')}")
    if real_leads:
        print(f"   Exemplo lead: {real_leads[0].get('name', 'N/A')}")
    
    # Testar ISA com contexto de admin
    print(f"\n🤖 Testando ISA com contexto de admin...")
    
    try:
        agent = IsaAgent()
        
        # Teste 1: Listar clientes
        print(f"\n1️⃣ Comando: 'Liste os clientes cadastrados'")
        result = await agent.invoke(
            messages=[HumanMessage(content="Liste os clientes cadastrados")],
            context={"user_id": "876be331-9553-4e9a-9f29-63cfa711e056", "is_admin": True}
        )
        
        response = result.get("response", "")
        print(f"   Resposta: {response[:200]}...")
        
        # Verificar se mencionou dados reais
        if real_clients and any(c['company_name'] in response for c in real_clients if c.get('company_name')):
            print(f"   ✅ CONFIRMADO: ISA acessou banco REAL! Mencionou cliente real.")
        elif "mock" in response.lower() or "exemplo" in response.lower():
            print(f"   ❌ ISA está usando MOCK!")
        elif len(real_clients) == 0 and ("nenhum" in response.lower() or "0" in response):
            print(f"   ✅ CONFIRMADO: ISA acessou banco REAL! Confirmou que não há clientes.")
        else:
            print(f"   ⚠️ Não foi possível confirmar se é real ou mock")
        
        # Teste 2: Criar lead de teste
        print(f"\n2️⃣ Comando: 'Crie um lead de teste'")
        result2 = await agent.invoke(
            messages=[HumanMessage(content="Crie um lead com nome 'Teste ISA Validação' e telefone '+5511999999999' e source 'home'")],
            context={"user_id": "876be331-9553-4e9a-9f29-63cfa711e056", "is_admin": True}
        )
        
        response2 = result2.get("response", "")
        print(f"   Resposta: {response2[:200]}...")
        
        # Verificar se lead foi realmente criado
        await asyncio.sleep(1)  # Aguardar criação
        test_lead = supabase.table('leads').select('*').eq('name', 'Teste ISA Validação').execute().data
        
        if test_lead:
            print(f"   ✅ CONFIRMADO: ISA criou lead REAL no banco! ID: {test_lead[0]['id']}")
            
            # Limpar
            supabase.table('leads').delete().eq('id', test_lead[0]['id']).execute()
            print(f"   (Lead de teste deletado)")
        else:
            print(f"   ❌ Lead NÃO foi criado no banco (ISA usa mock)")
        
        print(f"\n{'='*70}")
        print(f"CONCLUSÃO:")
        if test_lead or (len(real_clients) == 0 and "nenhum" in response.lower()):
            print(f"✅ ISA ACESSA BANCO REAL e executa comandos reais!")
        else:
            print(f"❌ ISA NÃO acessa banco real (usa mocks)")
        print(f"{'='*70}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_isa_real())
