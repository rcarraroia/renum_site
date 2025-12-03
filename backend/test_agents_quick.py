"""
Teste rápido e direto dos agentes - foco em descobrir se funcionam
"""
import asyncio
from langchain_core.messages import HumanMessage
from src.agents.renus import RenusAgent
from src.agents.isa import IsaAgent
from src.agents.discovery_agent import DiscoveryAgent

async def test_renus():
    print("\n🤖 RENUS AGENT")
    print("-" * 50)
    
    try:
        agent = RenusAgent()
        print("✅ Inicializado")
        
        # Teste simples
        result = await agent.invoke(
            messages=[HumanMessage(content="Olá, quem é você?")],
            context={"client_id": "test"}
        )
        
        if result and "response" in result:
            print(f"✅ Responde: {result['response'][:80]}...")
            return True
        else:
            print(f"⚠️ Resposta estranha: {str(result)[:80]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

async def test_isa():
    print("\n🤖 ISA AGENT")
    print("-" * 50)
    
    try:
        agent = IsaAgent()
        print("✅ Inicializado")
        
        # Teste simples
        result = await agent.invoke(
            messages=[HumanMessage(content="Olá ISA")],
            context={"user_id": "test-user"}
        )
        
        if result and "response" in result:
            print(f"✅ Responde: {result['response'][:80]}...")
            
            # Teste CRÍTICO: acessa banco real?
            print("\n🔍 Teste crítico: Acessa banco real?")
            result2 = await agent.invoke(
                messages=[HumanMessage(content="Quantos clientes temos?")],
                context={"user_id": "test-user"}
            )
            
            response = result2.get("response", "")
            if "mock" in response.lower() or "exemplo" in response.lower():
                print("❌ USANDO MOCK!")
                return False
            else:
                print(f"✅ Resposta: {response[:100]}")
                print("⚠️ Não confirmado se é real ou mock")
                return True
        else:
            print(f"⚠️ Resposta estranha: {str(result)[:80]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

async def test_discovery():
    print("\n🤖 DISCOVERY AGENT")
    print("-" * 50)
    
    try:
        agent = DiscoveryAgent()
        print("✅ Inicializado")
        
        # Teste simples
        result = await agent.invoke(
            messages=[HumanMessage(content="Meu nome é João Silva")],
            context={"interview_id": "test"}
        )
        
        if result:
            print(f"✅ Processa mensagem: {str(result)[:80]}...")
            return True
        else:
            print("⚠️ Sem resposta")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {str(e)[:100]}")
        return False

async def main():
    print("\n" + "="*70)
    print("🧪 TESTE RÁPIDO DOS AGENTES LANGCHAIN")
    print("="*70)
    
    results = {
        "RENUS": await test_renus(),
        "ISA": await test_isa(),
        "Discovery": await test_discovery()
    }
    
    print("\n" + "="*70)
    print("📊 RESUMO")
    print("="*70)
    
    for agent, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {agent}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} agentes funcionando ({passed/total*100:.0f}%)")

if __name__ == "__main__":
    asyncio.run(main())
