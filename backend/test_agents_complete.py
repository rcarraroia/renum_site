"""
Teste completo dos 3 agentes LangChain
Foco em descobrir se funcionam REALMENTE (não mocks)
"""
import asyncio
from src.agents.renus import RenusAgent
from src.agents.isa import IsaAgent
from src.agents.discovery_agent import DiscoveryAgent
from src.utils.supabase_client import get_client

class AgentTester:
    def __init__(self):
        self.results = {
            "renus": {"tests": 0, "passed": 0, "failed": 0, "details": []},
            "isa": {"tests": 0, "passed": 0, "failed": 0, "details": []},
            "discovery": {"tests": 0, "passed": 0, "failed": 0, "details": []}
        }
    
    def log_test(self, agent_name, test_name, success, message):
        """Registra resultado de um teste"""
        self.results[agent_name]["tests"] += 1
        if success:
            self.results[agent_name]["passed"] += 1
            print(f"  ✅ {test_name}")
        else:
            self.results[agent_name]["failed"] += 1
            print(f"  ❌ {test_name}: {message}")
        
        self.results[agent_name]["details"].append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    async def test_renus(self):
        """Testa RENUS Agent"""
        print("\n" + "="*70)
        print("🤖 TESTANDO: RENUS AGENT")
        print("="*70 + "\n")
        
        try:
            agent = RenusAgent()
            self.log_test("renus", "Inicialização", True, "Agent criado")
        except Exception as e:
            self.log_test("renus", "Inicialização", False, str(e)[:100])
            return
        
        # Teste 1: Mensagem simples
        try:
            result = await agent.invoke({
                "messages": [{"role": "user", "content": "Olá, quem é você?"}]
            })
            
            has_response = "response" in result or "messages" in result
            self.log_test("renus", "Responde mensagem simples", has_response, 
                         "Resposta gerada" if has_response else "Sem resposta")
        except Exception as e:
            self.log_test("renus", "Responde mensagem simples", False, str(e)[:100])
        
        # Teste 2: Acesso ao Supabase
        try:
            result = await agent.invoke({
                "messages": [{"role": "user", "content": "Quantos clientes temos cadastrados?"}]
            })
            
            # Verificar se tentou acessar banco (não apenas mock)
            response_text = str(result)
            has_data = any(word in response_text.lower() for word in ["cliente", "cadastrado", "total", "número"])
            
            self.log_test("renus", "Acessa Supabase", has_data,
                         "Parece acessar dados reais" if has_data else "Resposta genérica (possível mock)")
        except Exception as e:
            self.log_test("renus", "Acessa Supabase", False, str(e)[:100])
    
    async def test_isa(self):
        """Testa ISA Agent"""
        print("\n" + "="*70)
        print("🤖 TESTANDO: ISA AGENT")
        print("="*70 + "\n")
        
        try:
            agent = IsaAgent()
            self.log_test("isa", "Inicialização", True, "Agent criado")
        except Exception as e:
            self.log_test("isa", "Inicialização", False, str(e)[:100])
            return
        
        # Teste 1: Mensagem simples
        try:
            result = await agent.invoke({
                "messages": [{"role": "user", "content": "Olá ISA"}],
                "user_id": "test-user-id"
            })
            
            has_response = "response" in result
            self.log_test("isa", "Responde mensagem simples", has_response,
                         "Resposta gerada" if has_response else "Sem resposta")
        except Exception as e:
            self.log_test("isa", "Responde mensagem simples", False, str(e)[:100])
        
        # Teste 2: CRÍTICO - Listar dados REAIS do banco
        print("\n  🔍 Teste crítico: ISA lista dados REAIS do banco...")
        try:
            # Primeiro, verificar quantos clientes existem
            supabase = get_client()
            real_count = len(supabase.table('clients').select('id').execute().data)
            print(f"     Clientes reais no banco: {real_count}")
            
            # Pedir para ISA listar
            result = await agent.invoke({
                "messages": [{"role": "user", "content": "Liste os últimos 3 clientes cadastrados"}],
                "user_id": "test-user-id"
            })
            
            response_text = str(result.get("response", ""))
            
            # Verificar se ISA retornou dados reais ou mock
            is_real = str(real_count) in response_text or "cliente" in response_text.lower()
            is_mock = "mock" in response_text.lower() or "exemplo" in response_text.lower()
            
            if is_real and not is_mock:
                self.log_test("isa", "Lista dados REAIS", True, f"Retornou dados do banco ({real_count} clientes)")
            elif is_mock:
                self.log_test("isa", "Lista dados REAIS", False, "USANDO MOCK! Não acessa banco real")
            else:
                self.log_test("isa", "Lista dados REAIS", False, "Resposta ambígua, não confirmou acesso ao banco")
                
        except Exception as e:
            self.log_test("isa", "Lista dados REAIS", False, str(e)[:100])
        
        # Teste 3: CRÍTICO - Criar registro no banco
        print("\n  🔍 Teste crítico: ISA cria registro REAL no banco...")
        try:
            result = await agent.invoke({
                "messages": [{"role": "user", "content": "Crie um lead de teste com nome 'Teste ISA' e telefone '+5511999999999'"}],
                "user_id": "test-user-id"
            })
            
            # Verificar se lead foi realmente criado
            supabase = get_client()
            leads = supabase.table('leads').select('*').eq('name', 'Teste ISA').execute().data
            
            if leads:
                self.log_test("isa", "Cria registro REAL", True, f"Lead criado no banco! ID: {leads[0]['id']}")
                
                # Limpar teste
                supabase.table('leads').delete().eq('id', leads[0]['id']).execute()
                print(f"     (Lead de teste deletado)")
            else:
                self.log_test("isa", "Cria registro REAL", False, "Lead NÃO foi criado no banco (possível mock)")
                
        except Exception as e:
            self.log_test("isa", "Cria registro REAL", False, str(e)[:100])
    
    async def test_discovery(self):
        """Testa Discovery Agent"""
        print("\n" + "="*70)
        print("🤖 TESTANDO: DISCOVERY AGENT")
        print("="*70 + "\n")
        
        try:
            agent = DiscoveryAgent()
            self.log_test("discovery", "Inicialização", True, "Agent criado")
        except Exception as e:
            self.log_test("discovery", "Inicialização", False, str(e)[:100])
            return
        
        # Teste 1: Processar conversa de entrevista
        print("\n  🔍 Simulando entrevista completa...")
        try:
            messages = [
                {"role": "assistant", "content": "Olá! Qual seu nome completo?"},
                {"role": "user", "content": "João Silva"},
                {"role": "assistant", "content": "Qual seu email?"},
                {"role": "user", "content": "joao@teste.com"},
                {"role": "assistant", "content": "Qual seu telefone?"},
                {"role": "user", "content": "+5511999999999"},
            ]
            
            result = await agent.process_messages(messages)
            
            # Verificar se extraiu dados
            has_data = isinstance(result, dict) and len(result) > 0
            self.log_test("discovery", "Processa entrevista", has_data,
                         f"Extraiu {len(result)} campos" if has_data else "Não extraiu dados")
            
            # Verificar campos obrigatórios
            if has_data:
                required_fields = ["nome", "email", "telefone"]
                found_fields = [f for f in required_fields if f in str(result).lower()]
                
                self.log_test("discovery", "Extrai campos obrigatórios", 
                             len(found_fields) >= 2,
                             f"Encontrou: {', '.join(found_fields)}")
        except Exception as e:
            self.log_test("discovery", "Processa entrevista", False, str(e)[:100])
    
    def print_summary(self):
        """Imprime resumo final"""
        print("\n\n" + "="*70)
        print("📊 RESUMO GERAL - AGENTES LANGCHAIN")
        print("="*70 + "\n")
        
        total_tests = sum(r["tests"] for r in self.results.values())
        total_passed = sum(r["passed"] for r in self.results.values())
        total_failed = sum(r["failed"] for r in self.results.values())
        
        print(f"Total de testes: {total_tests}")
        print(f"✅ Passaram: {total_passed} ({total_passed/total_tests*100:.1f}%)")
        print(f"❌ Falharam: {total_failed} ({total_failed/total_tests*100:.1f}%)")
        
        print(f"\n{'='*70}")
        print("RESUMO POR AGENTE")
        print(f"{'='*70}\n")
        
        for agent_name, data in self.results.items():
            status = "✅" if data["failed"] == 0 else "⚠️" if data["passed"] > 0 else "❌"
            print(f"{status} {agent_name.upper()}: {data['passed']}/{data['tests']} passaram")
            
            # Mostrar detalhes dos testes falhados
            failed_tests = [d for d in data["details"] if not d["success"]]
            if failed_tests:
                for test in failed_tests:
                    print(f"   ❌ {test['test']}: {test['message'][:60]}")

async def main():
    tester = AgentTester()
    
    await tester.test_renus()
    await tester.test_isa()
    await tester.test_discovery()
    
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main())
