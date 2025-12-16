#!/usr/bin/env python3
"""
Validação Frontend SICC - Sprint 10
Valida que as páginas SICC foram integradas corretamente no frontend
"""

import requests
import time
from typing import Dict, List, Tuple

# Configurações
FRONTEND_URL = "http://localhost:8081"
BACKEND_URL = "http://localhost:8000"

def test_frontend_loads() -> Tuple[bool, str]:
    """Testa se o frontend carrega sem erros"""
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            return True, "Frontend carregou com sucesso"
        else:
            return False, f"Frontend retornou status {response.status_code}"
    except Exception as e:
        return False, f"Erro ao acessar frontend: {str(e)}"

def test_sicc_routes_exist() -> Tuple[bool, str]:
    """Testa se as rotas SICC existem (não retornam 404)"""
    sicc_routes = [
        "/dashboard/admin/sicc/evolution",
        "/dashboard/admin/sicc/memories", 
        "/dashboard/admin/sicc/learning-queue",
        "/dashboard/admin/sicc/settings"
    ]
    
    results = []
    for route in sicc_routes:
        try:
            # Nota: Como são rotas SPA, vamos testar se o index.html carrega
            response = requests.get(f"{FRONTEND_URL}{route}", timeout=5)
            if response.status_code == 200:
                results.append(f"✅ {route}")
            else:
                results.append(f"❌ {route} - Status {response.status_code}")
        except Exception as e:
            results.append(f"❌ {route} - Erro: {str(e)}")
    
    success = all("✅" in result for result in results)
    return success, "\n".join(results)

def test_backend_sicc_endpoints() -> Tuple[bool, str]:
    """Testa se os endpoints SICC do backend respondem"""
    endpoints = [
        "/api/sicc/memory/",
        "/api/sicc/learning/",
        "/api/sicc/patterns/",
        "/api/sicc/stats/agent/37ae9902-24bf-42b1-9d01-88c201ee0a6c/dashboard"
    ]
    
    results = []
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
            if response.status_code in [200, 401]:  # 401 é esperado sem auth
                results.append(f"✅ {endpoint}")
            else:
                results.append(f"❌ {endpoint} - Status {response.status_code}")
        except Exception as e:
            results.append(f"❌ {endpoint} - Erro: {str(e)}")
    
    success = all("✅" in result for result in results)
    return success, "\n".join(results)

def test_sicc_service_imports() -> Tuple[bool, str]:
    """Testa se os arquivos SICC existem e têm conteúdo válido"""
    import os
    
    files_to_check = [
        "src/services/siccService.ts",
        "src/types/sicc.ts",
        "src/pages/sicc/EvolutionPage.tsx",
        "src/pages/sicc/MemoryManagerPage.tsx", 
        "src/pages/sicc/LearningQueuePage.tsx",
        "src/pages/sicc/SettingsPage.tsx"
    ]
    
    results = []
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 100:  # Arquivo tem conteúdo substancial
                        results.append(f"✅ {file_path}")
                    else:
                        results.append(f"⚠️ {file_path} - Arquivo muito pequeno")
            except Exception as e:
                results.append(f"❌ {file_path} - Erro ao ler: {str(e)}")
        else:
            results.append(f"❌ {file_path} - Arquivo não encontrado")
    
    success = all("✅" in result for result in results)
    return success, "\n".join(results)

def main():
    """Executa todos os testes de validação"""
    print("🔍 VALIDAÇÃO FRONTEND SICC - SPRINT 10")
    print("=" * 50)
    
    tests = [
        ("Frontend Carrega", test_frontend_loads),
        ("Rotas SICC Existem", test_sicc_routes_exist),
        ("Endpoints Backend SICC", test_backend_sicc_endpoints),
        ("Arquivos SICC Existem", test_sicc_service_imports)
    ]
    
    results = {}
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Testando: {test_name}")
        print("-" * 30)
        
        try:
            success, message = test_func()
            results[test_name] = success
            
            if success:
                print(f"✅ PASSOU: {message}")
                passed_tests += 1
            else:
                print(f"❌ FALHOU: {message}")
                
        except Exception as e:
            print(f"💥 ERRO: {str(e)}")
            results[test_name] = False
    
    # Relatório Final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print(f"\n📈 RESULTADO: {passed_tests}/{total_tests} testes passaram")
    
    if passed_tests == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Frontend SICC está integrado corretamente")
        return True
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("❌ Integração SICC precisa de correções")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)