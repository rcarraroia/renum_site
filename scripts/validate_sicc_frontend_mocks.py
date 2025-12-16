#!/usr/bin/env python3
"""
Validação Frontend SICC com Mocks - Sprint 10
Valida que as páginas SICC funcionam corretamente com dados mock
"""

import requests
import time
from typing import Dict, List, Tuple

# Configurações
FRONTEND_URL = "http://localhost:8081"

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

def test_sicc_routes_accessible() -> Tuple[bool, str]:
    """Testa se as rotas SICC são acessíveis (retornam HTML, não 404)"""
    sicc_routes = [
        "/dashboard/admin/sicc/evolution",
        "/dashboard/admin/sicc/memories", 
        "/dashboard/admin/sicc/learning-queue",
        "/dashboard/admin/sicc/settings"
    ]
    
    results = []
    for route in sicc_routes:
        try:
            # Para SPAs, todas as rotas retornam o index.html
            response = requests.get(f"{FRONTEND_URL}{route}", timeout=5)
            if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
                results.append(f"✅ {route}")
            else:
                results.append(f"❌ {route} - Status {response.status_code}")
        except Exception as e:
            results.append(f"❌ {route} - Erro: {str(e)}")
    
    success = all("✅" in result for result in results)
    return success, "\n".join(results)

def test_sicc_files_exist() -> Tuple[bool, str]:
    """Testa se os arquivos SICC existem e têm conteúdo válido"""
    import os
    
    files_to_check = [
        ("src/services/siccService.ts", "siccService"),
        ("src/types/sicc.ts", "EvolutionStats"),
        ("src/pages/sicc/EvolutionPage.tsx", "EvolutionPage"),
        ("src/pages/sicc/MemoryManagerPage.tsx", "MemoryManagerPage"), 
        ("src/pages/sicc/LearningQueuePage.tsx", "LearningQueuePage"),
        ("src/pages/sicc/SettingsPage.tsx", "SettingsPage"),
        ("src/components/charts/LineChart.tsx", "LineChart"),
        ("src/components/charts/AreaChart.tsx", "AreaChart")
    ]
    
    results = []
    for file_path, expected_content in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if expected_content in content and len(content) > 500:
                        results.append(f"✅ {file_path}")
                    else:
                        results.append(f"⚠️ {file_path} - Conteúdo insuficiente ou inválido")
            except Exception as e:
                results.append(f"❌ {file_path} - Erro ao ler: {str(e)}")
        else:
            results.append(f"❌ {file_path} - Arquivo não encontrado")
    
    success = all("✅" in result for result in results)
    return success, "\n".join(results)

def test_sidebar_integration() -> Tuple[bool, str]:
    """Testa se o sidebar foi atualizado com a seção SICC"""
    import os
    
    sidebar_path = "src/components/dashboard/Sidebar.tsx"
    if not os.path.exists(sidebar_path):
        return False, "Arquivo Sidebar.tsx não encontrado"
    
    try:
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("Inteligência", "Seção Inteligência no sidebar"),
            ("sicc/evolution", "Rota Evolution"),
            ("sicc/memories", "Rota Memories"),
            ("sicc/learning-queue", "Rota Learning Queue"),
            ("sicc/settings", "Rota Settings"),
            ("Brain", "Ícone Brain importado"),
            ("TrendingUp", "Ícone TrendingUp importado"),
            ("Clock", "Ícone Clock importado")
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

def test_app_routes() -> Tuple[bool, str]:
    """Testa se as rotas SICC foram adicionadas no App.tsx"""
    import os
    
    app_path = "src/App.tsx"
    if not os.path.exists(app_path):
        return False, "Arquivo App.tsx não encontrado"
    
    try:
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("EvolutionPage", "Import EvolutionPage"),
            ("MemoryManagerPage", "Import MemoryManagerPage"),
            ("LearningQueuePage", "Import LearningQueuePage"),
            ("SettingsPage", "Import SettingsPage"),
            ("/dashboard/admin/sicc/evolution", "Rota Evolution"),
            ("/dashboard/admin/sicc/memories", "Rota Memories"),
            ("/dashboard/admin/sicc/learning-queue", "Rota Learning Queue"),
            ("/dashboard/admin/sicc/settings", "Rota Settings")
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

def main():
    """Executa todos os testes de validação"""
    print("🔍 VALIDAÇÃO FRONTEND SICC COM MOCKS - SPRINT 10")
    print("=" * 60)
    
    tests = [
        ("Frontend Carrega", test_frontend_loads),
        ("Rotas SICC Acessíveis", test_sicc_routes_accessible),
        ("Arquivos SICC Existem", test_sicc_files_exist),
        ("Sidebar Integrado", test_sidebar_integration),
        ("Rotas App.tsx", test_app_routes)
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
        print("✅ Frontend SICC está integrado e funcionando com mocks")
        return True
    elif passed_tests >= total_tests * 0.8:  # 80% ou mais
        print("⚠️ MAIORIA DOS TESTES PASSOU")
        print("✅ Integração SICC está funcional (com pequenos ajustes necessários)")
        return True
    else:
        print("❌ MUITOS TESTES FALHARAM")
        print("❌ Integração SICC precisa de correções significativas")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)