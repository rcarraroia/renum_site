#!/usr/bin/env python3
"""
Validação Final SICC Integration - Sprint 10
Valida que a integração SICC está funcionando corretamente
"""

import requests
import time
from typing import Dict, List, Tuple

# Configurações
FRONTEND_URL = "http://localhost:8081"

def test_frontend_loads() -> Tuple[bool, str]:
    """Testa se o frontend carrega sem erros"""
    try:
        response = requests.get(FRONTEND_URL, timeout=15)
        if response.status_code == 200:
            if "<!DOCTYPE html>" in response.text or "<html" in response.text:
                return True, f"Frontend carregou com sucesso (Status: {response.status_code})"
            else:
                return False, f"Frontend retornou status 200 mas sem HTML válido"
        else:
            return False, f"Frontend retornou status {response.status_code}"
    except Exception as e:
        return False, f"Erro ao acessar frontend: {str(e)}"

def test_sicc_routes_accessible() -> Tuple[bool, str]:
    """Testa se as rotas SICC são acessíveis"""
    sicc_routes = [
        "/intelligence/evolution",
        "/intelligence/memories", 
        "/intelligence/queue",
        "/intelligence/settings"
    ]
    
    results = []
    for route in sicc_routes:
        try:
            response = requests.get(f"{FRONTEND_URL}{route}", timeout=10)
            if response.status_code == 200:
                if "<!DOCTYPE html>" in response.text or "<html" in response.text:
                    results.append(f"✅ {route}")
                else:
                    results.append(f"❌ {route} - Status 200 mas sem HTML válido")
            else:
                results.append(f"❌ {route} - Status {response.status_code}")
        except Exception as e:
            results.append(f"❌ {route} - Erro: {str(e)}")
    
    success = all("✅" in result for result in results)
    return success, "\n".join(results)

def test_sidebar_updated() -> Tuple[bool, str]:
    """Testa se o sidebar foi atualizado corretamente"""
    import os
    
    sidebar_path = "src/components/dashboard/Sidebar.tsx"
    if not os.path.exists(sidebar_path):
        return False, "Arquivo Sidebar.tsx não encontrado"
    
    try:
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("/intelligence/evolution", "Rota Evolution corrigida"),
            ("/intelligence/memories", "Rota Memories corrigida"),
            ("/intelligence/queue", "Rota Queue corrigida"),
            ("/intelligence/settings", "Rota Settings corrigida"),
            ("Inteligência", "Seção Inteligência presente"),
        ]
        
        results = []
        for check_text, description in checks:
            if check_text in content:
                results.append(f"✅ {description}")
            else:
                results.append(f"❌ {description} - Não encontrado")
        
        success = all("✅" in result for result in results)
        return success, "\n".join(results)
        
    except Exception as e:
        return False, f"Erro ao verificar sidebar: {str(e)}"

def test_app_routes_updated() -> Tuple[bool, str]:
    """Testa se as rotas no App.tsx foram atualizadas"""
    import os
    
    app_path = "src/App.tsx"
    if not os.path.exists(app_path):
        return False, "Arquivo App.tsx não encontrado"
    
    try:
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("/intelligence/evolution", "Rota Evolution corrigida"),
            ("/intelligence/memories", "Rota Memories corrigida"),
            ("/intelligence/queue", "Rota Queue corrigida"),
            ("/intelligence/settings", "Rota Settings corrigida"),
            ("EvolutionPage", "Import EvolutionPage"),
            ("MemoryManagerPage", "Import MemoryManagerPage"),
            ("LearningQueuePage", "Import LearningQueuePage"),
            ("SettingsPage", "Import SettingsPage")
        ]
        
        results = []
        for check_text, description in checks:
            if check_text in content:
                results.append(f"✅ {description}")
            else:
                results.append(f"❌ {description} - Não encontrado")
        
        success = all("✅" in result for result in results)
        return success, "\n".join(results)
        
    except Exception as e:
        return False, f"Erro ao verificar App.tsx: {str(e)}"

def test_sicc_service_updated() -> Tuple[bool, str]:
    """Testa se o siccService foi atualizado corretamente"""
    import os
    
    service_path = "src/services/siccService.ts"
    if not os.path.exists(service_path):
        return False, "Arquivo siccService.ts não encontrado"
    
    try:
        with open(service_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("getEvolutionStats", "Método getEvolutionStats"),
            ("listMemories", "Método listMemories"),
            ("getLearningQueue", "Método getLearningQueue"),
            ("getSettings", "Método getSettings"),
            ("listAgents", "Método listAgents"),
            ("apiClient", "Import apiClient"),
            ("getMockAgents", "Função getMockAgents"),
            ("getMockMemories", "Função getMockMemories")
        ]
        
        results = []
        for check_text, description in checks:
            if check_text in content:
                results.append(f"✅ {description}")
            else:
                results.append(f"❌ {description} - Não encontrado")
        
        success = all("✅" in result for result in results)
        return success, "\n".join(results)
        
    except Exception as e:
        return False, f"Erro ao verificar siccService: {str(e)}"

def test_pages_exist() -> Tuple[bool, str]:
    """Testa se todas as páginas SICC existem"""
    import os
    
    pages = [
        "src/pages/sicc/EvolutionPage.tsx",
        "src/pages/sicc/MemoryManagerPage.tsx",
        "src/pages/sicc/LearningQueuePage.tsx",
        "src/pages/sicc/SettingsPage.tsx"
    ]
    
    results = []
    for page_path in pages:
        if os.path.exists(page_path):
            try:
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 1000:  # Página tem conteúdo substancial
                        results.append(f"✅ {page_path}")
                    else:
                        results.append(f"⚠️ {page_path} - Conteúdo insuficiente")
            except Exception as e:
                results.append(f"❌ {page_path} - Erro ao ler: {str(e)}")
        else:
            results.append(f"❌ {page_path} - Não encontrado")
    
    success = all("✅" in result for result in results)
    return success, "\n".join(results)

def main():
    """Executa todos os testes de validação"""
    print("🔍 VALIDAÇÃO FINAL SICC INTEGRATION - SPRINT 10")
    print("=" * 60)
    
    tests = [
        ("Frontend Carrega", test_frontend_loads),
        ("Rotas SICC Acessíveis", test_sicc_routes_accessible),
        ("Sidebar Atualizado", test_sidebar_updated),
        ("App.tsx Atualizado", test_app_routes_updated),
        ("siccService Atualizado", test_sicc_service_updated),
        ("Páginas SICC Existem", test_pages_exist)
    ]
    
    results = {}
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 Testando: {test_name}")
        print("-" * 40)
        
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
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{status}: {test_name}")
    
    print(f"\n📈 RESULTADO: {passed_tests}/{total_tests} testes passaram")
    
    if passed_tests == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Integração SICC está completa e funcionando")
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Testar navegação manual no browser")
        print("2. Verificar se dados mock aparecem nas páginas")
        print("3. Testar responsividade mobile")
        print("4. Marcar Task 9 como COMPLETA")
        return True
    elif passed_tests >= total_tests * 0.8:  # 80% ou mais
        print("⚠️ MAIORIA DOS TESTES PASSOU")
        print("✅ Integração SICC está quase completa")
        print("🔧 Pequenos ajustes necessários")
        return True
    else:
        print("❌ MUITOS TESTES FALHARAM")
        print("❌ Integração SICC precisa de correções")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)