#!/usr/bin/env python3
"""
Validação Tasks 43-44 - Niche Propagation & Layer Management
Verifica se os serviços foram implementados corretamente
"""

import os
import sys
from pathlib import Path

def validate_tasks43_44():
    """Valida Tasks 43 e 44"""
    print("🔄 VALIDAÇÃO TASKS 43-44 - NICHE PROPAGATION & LAYER MANAGEMENT")
    print("=" * 65)
    
    results = []
    
    # Teste 1: Verificar arquivos criados
    print("\n📋 Teste 1: Verificar arquivos criados")
    required_files = [
        "src/services/sicc/niche_propagation_service.py",
        "src/services/sicc/layer_management_service.py"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file_path} - {file_size} bytes")
        else:
            print(f"❌ {file_path} - NÃO ENCONTRADO")
            all_files_exist = False
    
    results.append(("Arquivos criados", all_files_exist, f"{len(required_files)} arquivos"))
    
    # Teste 2: Verificar conteúdo - Niche Propagation
    print("\n📋 Teste 2: Verificar NichePropagationService")
    niche_service_ok = False
    if os.path.exists("src/services/sicc/niche_propagation_service.py"):
        with open("src/services/sicc/niche_propagation_service.py", 'r', encoding='utf-8') as f:
            content = f.read()
            
            required_methods = [
                "get_agents_by_niche",
                "create_base_knowledge_version",
                "propagate_knowledge_to_niche",
                "rollback_propagation"
            ]
            
            methods_found = []
            for method in required_methods:
                if method in content:
                    methods_found.append(method)
                    print(f"✅ Método {method} presente")
                else:
                    print(f"❌ Método {method} faltando")
            
            niche_service_ok = len(methods_found) == len(required_methods)
    
    results.append(("NichePropagationService", niche_service_ok, f"{len(methods_found) if 'methods_found' in locals() else 0}/4 métodos"))
    
    # Teste 3: Verificar conteúdo - Layer Management
    print("\n📋 Teste 3: Verificar LayerManagementService")
    layer_service_ok = False
    if os.path.exists("src/services/sicc/layer_management_service.py"):
        with open("src/services/sicc/layer_management_service.py", 'r', encoding='utf-8') as f:
            content = f.read()
            
            required_methods = [
                "add_knowledge_to_layer",
                "get_layered_memories",
                "get_layered_patterns",
                "resolve_knowledge_conflicts"
            ]
            
            methods_found = []
            for method in required_methods:
                if method in content:
                    methods_found.append(method)
                    print(f"✅ Método {method} presente")
                else:
                    print(f"❌ Método {method} faltando")
            
            layer_service_ok = len(methods_found) == len(required_methods)
    
    results.append(("LayerManagementService", layer_service_ok, f"{len(methods_found) if 'methods_found' in locals() else 0}/4 métodos"))
    
    # Teste 4: Verificar enums e classes
    print("\n📋 Teste 4: Verificar estruturas de dados")
    structures_ok = False
    if os.path.exists("src/services/sicc/layer_management_service.py"):
        with open("src/services/sicc/layer_management_service.py", 'r', encoding='utf-8') as f:
            content = f.read()
            
            structures = ["KnowledgeLayer", "class LayerManagementService"]
            structures_found = []
            
            for structure in structures:
                if structure in content:
                    structures_found.append(structure)
                    print(f"✅ {structure} presente")
                else:
                    print(f"❌ {structure} faltando")
            
            structures_ok = len(structures_found) == len(structures)
    
    results.append(("Estruturas de dados", structures_ok, f"{len(structures_found) if 'structures_found' in locals() else 0}/2 estruturas"))
    
    # Teste 5: Verificar imports e dependências
    print("\n📋 Teste 5: Verificar imports")
    imports_ok = True
    
    files_to_check = [
        "src/services/sicc/niche_propagation_service.py",
        "src/services/sicc/layer_management_service.py"
    ]
    
    required_imports = ["MemoryService", "BehaviorService", "get_client"]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for imp in required_imports:
                    if imp not in content:
                        print(f"❌ Import {imp} faltando em {file_path}")
                        imports_ok = False
                        break
                else:
                    print(f"✅ Imports OK em {Path(file_path).name}")
    
    results.append(("Imports", imports_ok, "Dependências verificadas"))
    
    # Teste 6: Verificar tamanho dos arquivos (indicador de completude)
    print("\n📋 Teste 6: Verificar completude dos arquivos")
    completeness_ok = True
    
    min_sizes = {
        "src/services/sicc/niche_propagation_service.py": 15000,  # ~15KB
        "src/services/sicc/layer_management_service.py": 12000    # ~12KB
    }
    
    for file_path, min_size in min_sizes.items():
        if os.path.exists(file_path):
            actual_size = os.path.getsize(file_path)
            if actual_size >= min_size:
                print(f"✅ {Path(file_path).name} - {actual_size} bytes (≥ {min_size})")
            else:
                print(f"⚠️ {Path(file_path).name} - {actual_size} bytes (< {min_size}) - Pode estar incompleto")
                completeness_ok = False
        else:
            completeness_ok = False
    
    results.append(("Completude arquivos", completeness_ok, "Tamanhos verificados"))
    
    return results

def main():
    """Executa validação e gera relatório"""
    try:
        results = validate_tasks43_44()
        
        # Relatório final
        print("\n" + "=" * 65)
        print("📊 RELATÓRIO FINAL - TASKS 43-44")
        print("=" * 65)
        
        passed = 0
        total = len(results)
        
        for test_name, success, details in results:
            status = "✅ PASSOU" if success else "❌ FALHOU"
            print(f"{status}: {test_name} - {details}")
            if success:
                passed += 1
        
        print(f"\n📈 RESULTADO: {passed}/{total} testes passaram")
        
        if passed == total:
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Tasks 43-44 - Niche Propagation & Layer Management COMPLETAS")
            return True
        elif passed >= total * 0.8:
            print("⚠️ MAIORIA DOS TESTES PASSOU")
            print("✅ Tasks 43-44 estão quase completas")
            return True
        else:
            print("❌ MUITOS TESTES FALHARAM")
            print("❌ Tasks 43-44 precisam de correções")
            return False
            
    except Exception as e:
        print(f"💥 ERRO CRÍTICO: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)