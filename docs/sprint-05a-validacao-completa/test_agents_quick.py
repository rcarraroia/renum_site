"""Teste rápido de Agentes - Sprint 05A - Fase 3"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("\n" + "="*60)
print("FASE 3 - VALIDAÇÃO DE AGENTES")
print("="*60)

results = {"total": 0, "success": 0, "failed": 0, "errors": []}

def test(name):
    """Decorator para testes"""
    def decorator(func):
        results["total"] += 1
        try:
            print(f"\n🧪 {name}")
            func()
            results["success"] += 1
            print(f"   ✅ PASSOU")
            return True
        except AssertionError as e:
            results["failed"] += 1
            error = f"{name}: {str(e)}"
            results["errors"].append(error)
            print(f"   ❌ FALHOU: {str(e)}")
            return False
        except Exception as e:
            results["failed"] += 1
            error = f"{name}: ERRO - {str(e)}"
            results["errors"].append(error)
            print(f"   ❌ ERRO: {str(e)}")
            return False
    return decorator

# TESTE 1: RENUS Agent
@test("1. RENUS Agent - Inicialização")
def test_renus_init():
    from src.agents.renus import RenusAgent
    agent = RenusAgent()
    assert agent is not None, "Agente não inicializou"

@test("2. RENUS Agent - Resposta simples")
def test_renus_response():
    from src.agents.renus import RenusAgent
    from langchain_core.messages import HumanMessage
    
    agent = RenusAgent()
    messages = [HumanMessage(content="Olá")]
    context = {"user_id": "test_user"}
    
    result = agent.invoke(messages, context)
    assert result is not None, "Agente não retornou resultado"

# TESTE 2: ISA Agent
@test("3. ISA Agent - Inicialização")
def test_isa_init():
    from src.agents.isa import IsaAgent
    agent = IsaAgent()
    assert agent is not None, "ISA não inicializou"

@test("4. ISA Agent - Comando simples")
def test_isa_command():
    from src.agents.isa import IsaAgent
    from langchain_core.messages import HumanMessage
    
    agent = IsaAgent()
    messages = [HumanMessage(content="Liste os últimos clientes")]
    context = {"admin_id": "test_admin", "is_admin": True}
    
    result = agent.invoke(messages, context)
    assert result is not None, "ISA não retornou resultado"

# TESTE 3: Discovery Agent
@test("5. Discovery Agent - Inicialização")
def test_discovery_init():
    from src.agents.discovery_agent import DiscoveryAgent
    agent = DiscoveryAgent()
    assert agent is not None, "Discovery não inicializou"

@test("6. Discovery Agent - Processar mensagem")
def test_discovery_process():
    from src.agents.discovery_agent import DiscoveryAgent
    from langchain_core.messages import HumanMessage
    
    agent = DiscoveryAgent()
    messages = [HumanMessage(content="Meu nome é João")]
    context = {"interview_id": "test_interview"}
    
    result = agent.invoke(messages, context)
    assert result is not None, "Discovery não retornou resultado"

# TESTE 4: LangSmith Traces (opcional)
@test("7. LangSmith - Verificar configuração")
def test_langsmith_config():
    import os
    api_key = os.getenv("LANGCHAIN_API_KEY")
    assert api_key, "LANGCHAIN_API_KEY não configurada"
    
    tracing = os.getenv("LANGCHAIN_TRACING_V2")
    assert tracing == "true", "LANGCHAIN_TRACING_V2 não habilitado"

# Executar testes
print("\n" + "="*60)
print("RESUMO DOS TESTES")
print("="*60)

pct = (results["success"] / results["total"] * 100) if results["total"] > 0 else 0
print(f"\nTotal: {results['total']} testes")
print(f"Sucesso: {results['success']} ({pct:.1f}%)")
print(f"Falhas: {results['failed']}")

if results["errors"]:
    print("\n❌ ERROS ENCONTRADOS:")
    for i, error in enumerate(results["errors"], 1):
        print(f"   {i}. {error}")

if pct == 100:
    print("\n✅ AGENTES 100% FUNCIONAIS")
elif pct >= 70:
    print("\n⚠️ AGENTES PARCIALMENTE FUNCIONAIS")
else:
    print("\n❌ AGENTES COM PROBLEMAS")

print("="*60)
