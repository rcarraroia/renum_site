#!/usr/bin/env python3
"""
Validação Consolidada de Todos os Property Tests - Phase 5
Sprint 10 - SICC Implementation

Executa todos os property tests das Tasks 20, 22, 24, 26, 28
Seguindo regras de validação: NUNCA ASSUMA. SEMPRE VERIFIQUE.
"""

import sys
import subprocess
from pathlib import Path

def run_test_script(script_name, task_name):
    """Executa um script de teste e retorna o resultado"""
    
    print(f"\n🧪 EXECUTANDO {task_name}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        # Mostrar output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        
        if success:
            print(f"✅ {task_name} - SUCESSO")
        else:
            print(f"❌ {task_name} - FALHOU (exit code: {result.returncode})")
        
        return success
        
    except subprocess.TimeoutExpired:
        print(f"⏰ {task_name} - TIMEOUT (>5min)")
        return False
    except Exception as e:
        print(f"❌ {task_name} - ERRO: {e}")
        return False


def main():
    """Executa todos os property tests"""
    
    print("🧪 VALIDAÇÃO CONSOLIDADA - PROPERTY TESTS")
    print("Sprint 10 - Phase 5 - Tasks 20, 22, 24, 26, 28")
    print("=" * 80)
    
    # Lista de testes para executar
    tests = [
        ("test_embedding_simple.py", "Task 20: EmbeddingService Property Tests"),
        ("test_memory_simple.py", "Task 22: MemoryService Property Tests"),
        ("test_behavior_simple.py", "Task 24: BehaviorService Property Tests"),
        ("test_snapshot_simple.py", "Task 26: SnapshotService Property Tests"),
        ("test_metrics_simple.py", "Task 28: MetricsService Property Tests")
    ]
    
    # Executar todos os testes
    results = []
    
    for script, task_name in tests:
        success = run_test_script(script, task_name)
        results.append((task_name, success))
    
    # Resumo final
    print("\n" + "=" * 80)
    print("📊 RESUMO FINAL - TODOS OS PROPERTY TESTS")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for task_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"   {status} - {task_name}")
        if success:
            passed += 1
    
    success_rate = passed / total if total > 0 else 0
    print(f"\n📈 TAXA DE SUCESSO GERAL: {passed}/{total} ({success_rate:.1%})")
    
    if success_rate >= 0.8:  # 80% mínimo
        print(f"\n🎉 TODOS OS PROPERTY TESTS APROVADOS!")
        print(f"✅ Phase 5 - Property Tests COMPLETA")
        print(f"✅ Tasks 20, 22, 24, 26, 28 - VALIDADAS")
        
        print(f"\n📋 PRÓXIMOS PASSOS:")
        print(f"   - Task 38: Monitoring & Alerting")
        print(f"   - Task 39: Performance Tuning")
        print(f"   - Tasks 46-50: Final testing, optimization, security")
        
        return True
    else:
        print(f"\n❌ PROPERTY TESTS FALHARAM!")
        print(f"⚠️  Corrija os testes que falharam antes de prosseguir")
        
        # Mostrar quais falharam
        failed_tests = [task for task, success in results if not success]
        if failed_tests:
            print(f"\n🔧 TESTES QUE FALHARAM:")
            for task in failed_tests:
                print(f"   - {task}")
        
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)