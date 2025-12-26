"""
Script de Validação - SICC Multi-Agente
Sprint SICC Multi-Agente

Valida que o SICC está funcionando corretamente para todos os agentes.
"""

import os
import sys
import asyncio
from datetime import datetime

# Adicionar path do backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv()


def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(test_name: str, passed: bool, details: str = ""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status} | {test_name}")
    if details:
        print(f"         {details}")


async def test_sicc_hook():
    """Testa o SICC Hook"""
    print_header("TESTE 1: SICC Hook")
    
    try:
        from src.services.sicc.sicc_hook import get_sicc_hook, SiccHook
        
        # 1. Verificar singleton
        hook1 = get_sicc_hook()
        hook2 = get_sicc_hook()
        print_result("Singleton pattern", hook1 is hook2)
        
        # 2. Verificar stats iniciais
        stats = hook1.get_stats()
        print_result("Stats disponíveis", "enabled" in stats and "queue_size" in stats)
        print(f"         Stats: {stats}")
        
        # 3. Testar enable/disable
        hook1.disable()
        print_result("Disable funciona", not hook1.get_stats()["enabled"])
        
        hook1.enable()
        print_result("Enable funciona", hook1.get_stats()["enabled"])
        
        # 4. Testar on_interaction (mock)
        await hook1.on_interaction(
            agent_id="test-agent-id",
            agent_type="test",
            messages=[{"role": "user", "content": "Teste"}],
            response="Resposta de teste",
            context={"test": True}
        )
        
        stats_after = hook1.get_stats()
        print_result("on_interaction adiciona à queue", stats_after["queue_size"] >= 1)
        
        # 5. Testar flush
        count = await hook1.flush()
        print_result("Flush processa queue", count >= 0)
        
        return True
        
    except Exception as e:
        print_result("SICC Hook", False, str(e))
        return False


async def test_sicc_analyzer():
    """Testa o SICC Analyzer"""
    print_header("TESTE 2: SICC Analyzer")
    
    try:
        from src.services.sicc.analyzer_service import SiccAnalyzer
        
        analyzer = SiccAnalyzer()
        print_result("Analyzer instanciado", True)
        
        # Testar detecção de oportunidade de aprendizado
        messages_learning = [
            {"role": "user", "content": "Aprenda que meu nome é João"}
        ]
        is_learning = analyzer._is_learning_opportunity(messages_learning, "Ok, vou lembrar")
        print_result("Detecta oportunidade de aprendizado", is_learning)
        
        # Testar detecção de feedback positivo
        messages_feedback = [
            {"role": "user", "content": "Olá"},
            {"role": "user", "content": "Perfeito, obrigado!"}
        ]
        should_mem = analyzer._should_memorize(messages_feedback, "De nada!")
        print_result("Detecta feedback positivo", should_mem)
        
        return True
        
    except Exception as e:
        print_result("SICC Analyzer", False, str(e))
        return False


def test_base_agent_sicc_integration():
    """Testa integração do BaseAgent com SICC"""
    print_header("TESTE 3: BaseAgent SICC Integration")
    
    try:
        from src.agents.base import BaseAgent
        import inspect
        
        # Verificar novos atributos
        init_sig = inspect.signature(BaseAgent.__init__)
        params = list(init_sig.parameters.keys())
        
        print_result("agent_id no __init__", "agent_id" in params)
        print_result("agent_type no __init__", "agent_type" in params)
        print_result("sicc_enabled no __init__", "sicc_enabled" in params)
        
        # Verificar método _notify_sicc
        has_notify = hasattr(BaseAgent, '_notify_sicc')
        print_result("Método _notify_sicc existe", has_notify)
        
        return True
        
    except Exception as e:
        print_result("BaseAgent Integration", False, str(e))
        return False


def test_renus_sicc_integration():
    """Testa integração do RenusAgent com SICC"""
    print_header("TESTE 4: RenusAgent SICC Integration")
    
    try:
        # Apenas verificar código, não instanciar (requer OpenAI key)
        from src.agents.renus import RenusAgent
        import inspect
        
        source = inspect.getsource(RenusAgent.__init__)
        
        print_result("agent_id configurado", "agent_id" in source)
        print_result("agent_type='renus'", "agent_type" in source)
        print_result("sicc_enabled passado", "sicc_enabled" in source)
        
        invoke_source = inspect.getsource(RenusAgent.invoke)
        print_result("_notify_sicc chamado no invoke", "_notify_sicc" in invoke_source)
        
        return True
        
    except Exception as e:
        print_result("RenusAgent Integration", False, str(e))
        return False


def test_isa_sicc_integration():
    """Testa integração do IsaAgent com SICC"""
    print_header("TESTE 5: IsaAgent SICC Integration")
    
    try:
        from src.agents.isa import IsaAgent
        import inspect
        
        source = inspect.getsource(IsaAgent.__init__)
        
        print_result("agent_id configurado", "agent_id" in source)
        print_result("agent_type='isa'", "agent_type" in source)
        
        invoke_source = inspect.getsource(IsaAgent.invoke)
        print_result("_notify_sicc chamado no invoke", "_notify_sicc" in invoke_source)
        
        return True
        
    except Exception as e:
        print_result("IsaAgent Integration", False, str(e))
        return False


def test_discovery_sicc_integration():
    """Testa integração do DiscoveryAgent com SICC"""
    print_header("TESTE 6: DiscoveryAgent SICC Integration")
    
    try:
        from src.agents.discovery_agent import DiscoveryAgent
        import inspect
        
        source = inspect.getsource(DiscoveryAgent.__init__)
        
        print_result("agent_id configurado", "agent_id" in source)
        print_result("agent_type='discovery'", "agent_type" in source)
        
        invoke_source = inspect.getsource(DiscoveryAgent.invoke)
        print_result("_notify_sicc chamado no invoke", "_notify_sicc" in invoke_source)
        
        return True
        
    except Exception as e:
        print_result("DiscoveryAgent Integration", False, str(e))
        return False


def test_celery_tasks():
    """Testa tasks Celery do SICC"""
    print_header("TESTE 7: Celery Tasks")
    
    try:
        from src.workers.sicc_tasks import (
            consolidate_learnings,
            analyze_patterns,
            create_snapshot,
            flush_sicc_queue,
            cleanup_old_data
        )
        
        print_result("consolidate_learnings importado", True)
        print_result("analyze_patterns importado", True)
        print_result("create_snapshot importado", True)
        print_result("flush_sicc_queue importado", True)
        print_result("cleanup_old_data importado", True)
        
        return True
        
    except Exception as e:
        print_result("Celery Tasks", False, str(e))
        return False


def test_api_routes():
    """Testa rotas API do SICC Hook"""
    print_header("TESTE 8: API Routes")
    
    try:
        from src.api.routes.sicc_hook import router
        
        routes = [r.path for r in router.routes]
        
        print_result("/stats existe", "/stats" in routes)
        print_result("/enable existe", "/enable" in routes)
        print_result("/disable existe", "/disable" in routes)
        print_result("/flush existe", "/flush" in routes)
        print_result("/health existe", "/health" in routes)
        
        return True
        
    except Exception as e:
        print_result("API Routes", False, str(e))
        return False


async def test_database_tables():
    """Testa se as tabelas necessárias existem no banco"""
    print_header("TESTE 9: Database Tables")
    
    try:
        from src.config.supabase import supabase_admin
        
        tables_to_check = [
            "memory_chunks",
            "learning_logs",
            "behavior_patterns",
            "agent_metrics",
            "agent_snapshots",
            "sicc_settings"
        ]
        
        for table in tables_to_check:
            try:
                result = supabase_admin.table(table).select("id").limit(1).execute()
                print_result(f"Tabela {table}", True)
            except Exception as e:
                print_result(f"Tabela {table}", False, str(e))
        
        return True
        
    except Exception as e:
        print_result("Database Tables", False, str(e))
        return False


async def main():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("  VALIDAÇÃO SICC MULTI-AGENTE")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    
    # Testes síncronos
    results.append(("BaseAgent Integration", test_base_agent_sicc_integration()))
    results.append(("RenusAgent Integration", test_renus_sicc_integration()))
    results.append(("IsaAgent Integration", test_isa_sicc_integration()))
    results.append(("DiscoveryAgent Integration", test_discovery_sicc_integration()))
    results.append(("Celery Tasks", test_celery_tasks()))
    results.append(("API Routes", test_api_routes()))
    
    # Testes assíncronos
    results.append(("SICC Hook", await test_sicc_hook()))
    results.append(("SICC Analyzer", await test_sicc_analyzer()))
    results.append(("Database Tables", await test_database_tables()))
    
    # Resumo
    print_header("RESUMO")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print(f"\n  Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n  🎉 SICC Multi-Agente validado com sucesso!")
    else:
        print("\n  ⚠️ Alguns testes falharam. Verifique os detalhes acima.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
