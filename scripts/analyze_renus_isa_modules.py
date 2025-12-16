#!/usr/bin/env python3
"""
Análise Completa dos Módulos RENUS e ISA
Verifica implementação, rotas, componentes, banco de dados e funcionalidades
"""
import os
import json
import requests
from pathlib import Path

# Token válido para testes
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjgxNzczLCJpYXQiOjE3NjU1OTUzNzMsInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Hhlrodg5Ks31ji9H7t80Z8EVEDopF0djbXV-J2wRfqE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def analyze_frontend_routes():
    """Analisa rotas do frontend"""
    print("=== 🌐 ANÁLISE DE ROTAS FRONTEND ===")
    
    # Verificar App.tsx para rotas principais
    app_file = "src/App.tsx"
    if os.path.exists(app_file):
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📍 ROTAS ENCONTRADAS NO APP.TSX:")
        
        # Procurar por rotas específicas
        routes_to_check = [
            "/dashboard/admin/renus-config",
            "/dashboard/admin/assistente-isa",
            "/renus-config",
            "/assistente-isa",
            "/isa"
        ]
        
        for route in routes_to_check:
            if route in content:
                print(f"  ✅ {route} - ENCONTRADA")
            else:
                print(f"  ❌ {route} - NÃO ENCONTRADA")
    else:
        print("❌ App.tsx não encontrado")

def analyze_frontend_pages():
    """Analisa páginas do frontend"""
    print("\n=== 📄 ANÁLISE DE PÁGINAS FRONTEND ===")
    
    # Estrutura esperada de páginas
    expected_pages = {
        "RENUS Config": [
            "src/pages/admin/renus/RenusConfigPage.tsx",
            "src/pages/renus/RenusConfigPage.tsx",
            "src/pages/admin/RenusConfigPage.tsx",
            "src/components/renus/RenusConfig.tsx"
        ],
        "ISA Assistant": [
            "src/pages/admin/isa/IsaAssistantPage.tsx",
            "src/pages/isa/IsaAssistantPage.tsx", 
            "src/pages/admin/IsaAssistantPage.tsx",
            "src/components/isa/IsaAssistant.tsx"
        ]
    }
    
    for module_name, possible_paths in expected_pages.items():
        print(f"\n🔍 {module_name}:")
        found = False
        for path in possible_paths:
            if os.path.exists(path):
                print(f"  ✅ ENCONTRADO: {path}")
                found = True
                
                # Analisar conteúdo do arquivo
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    print(f"     📊 Linhas: {lines}")
                    
                    # Verificar imports importantes
                    if "useState" in content:
                        print("     🔧 Usa React hooks")
                    if "useEffect" in content:
                        print("     🔄 Usa useEffect")
                    if "axios" in content or "fetch" in content:
                        print("     🌐 Faz chamadas API")
                    if "mock" in content.lower():
                        print("     ⚠️ Contém dados mock")
            else:
                print(f"  ❌ NÃO ENCONTRADO: {path}")
        
        if not found:
            print(f"  🚨 NENHUM ARQUIVO ENCONTRADO PARA {module_name}")

def analyze_backend_routes():
    """Analisa rotas do backend"""
    print("\n=== 🔧 ANÁLISE DE ROTAS BACKEND ===")
    
    # Verificar main.py para routers registrados
    main_file = "backend/src/main.py"
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📍 ROUTERS REGISTRADOS:")
        routers_to_check = [
            "renus_config.router",
            "isa.router",
            "renus.router",
            "assistente_isa.router"
        ]
        
        for router in routers_to_check:
            if router in content:
                print(f"  ✅ {router} - REGISTRADO")
            else:
                print(f"  ❌ {router} - NÃO REGISTRADO")
    
    # Verificar arquivos de rotas específicos
    route_files = [
        "backend/src/api/routes/renus_config.py",
        "backend/src/api/routes/isa.py",
        "backend/src/api/routes/renus.py",
        "backend/src/api/routes/assistente_isa.py"
    ]
    
    print("\n📁 ARQUIVOS DE ROTAS:")
    for file_path in route_files:
        if os.path.exists(file_path):
            print(f"  ✅ EXISTE: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Contar endpoints
            endpoints = content.count("@router.")
            print(f"     📊 Endpoints: {endpoints}")
            
            # Verificar métodos HTTP
            methods = []
            if "@router.get" in content:
                methods.append("GET")
            if "@router.post" in content:
                methods.append("POST")
            if "@router.put" in content:
                methods.append("PUT")
            if "@router.delete" in content:
                methods.append("DELETE")
            
            if methods:
                print(f"     🔗 Métodos: {', '.join(methods)}")
        else:
            print(f"  ❌ NÃO EXISTE: {file_path}")

def test_backend_endpoints():
    """Testa endpoints do backend"""
    print("\n=== 🧪 TESTE DE ENDPOINTS BACKEND ===")
    
    endpoints_to_test = [
        "/api/renus-config",
        "/api/renus-config/",
        "/api/isa",
        "/api/isa/",
        "/api/assistente-isa",
        "/api/assistente-isa/"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", headers=headers, timeout=5)
            print(f"  📡 {endpoint}")
            print(f"     Status: {response.status_code}")
            
            if response.status_code == 200:
                print("     ✅ FUNCIONANDO")
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"     📊 Retornou {len(data)} itens")
                    elif isinstance(data, dict):
                        print(f"     📊 Retornou objeto com {len(data)} campos")
                except:
                    print("     📄 Retornou texto/HTML")
            elif response.status_code == 404:
                print("     ❌ NÃO ENCONTRADO")
            elif response.status_code == 401:
                print("     🔒 NÃO AUTORIZADO")
            elif response.status_code == 500:
                print("     💥 ERRO INTERNO")
            else:
                print(f"     ⚠️ STATUS INESPERADO: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"  📡 {endpoint}")
            print("     💀 SERVIDOR NÃO RESPONDE")
        except requests.exceptions.Timeout:
            print(f"  📡 {endpoint}")
            print("     ⏰ TIMEOUT")
        except Exception as e:
            print(f"  📡 {endpoint}")
            print(f"     ❌ ERRO: {e}")

def analyze_database_tables():
    """Analisa tabelas do banco de dados"""
    print("\n=== 🗄️ ANÁLISE DE TABELAS DO BANCO ===")
    
    # Tentar via API do backend
    try:
        # Testar endpoint de configuração RENUS
        response = requests.get("http://localhost:8000/api/renus-config", headers=headers, timeout=5)
        print("📊 TABELA RENUS_CONFIG:")
        print(f"  Status API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ {len(data)} configurações encontradas")
            
            if data:
                first_config = data[0]
                print("  📋 Campos disponíveis:")
                for key in first_config.keys():
                    print(f"    - {key}")
        else:
            print(f"  ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Erro ao acessar API: {e}")
    
    # Verificar modelos Pydantic
    model_files = [
        "backend/src/models/renus_config.py",
        "backend/src/models/isa.py",
        "backend/src/models/renus.py"
    ]
    
    print("\n📋 MODELOS DE DADOS:")
    for file_path in model_files:
        if os.path.exists(file_path):
            print(f"  ✅ EXISTE: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Contar classes de modelo
            classes = content.count("class ")
            print(f"     📊 Classes: {classes}")
            
            # Verificar se usa Pydantic
            if "BaseModel" in content:
                print("     🔧 Usa Pydantic")
            if "Field" in content:
                print("     📝 Usa validações Field")
        else:
            print(f"  ❌ NÃO EXISTE: {file_path}")

def analyze_services():
    """Analisa services do backend"""
    print("\n=== ⚙️ ANÁLISE DE SERVICES ===")
    
    service_files = [
        "backend/src/services/renus_service.py",
        "backend/src/services/isa_service.py",
        "backend/src/services/renus_config_service.py",
        "backend/src/services/assistente_isa_service.py"
    ]
    
    for file_path in service_files:
        if os.path.exists(file_path):
            print(f"  ✅ EXISTE: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analisar funcionalidades
            functions = content.count("def ")
            classes = content.count("class ")
            print(f"     📊 Classes: {classes}, Funções: {functions}")
            
            # Verificar integrações
            if "supabase" in content.lower():
                print("     🗄️ Integra com Supabase")
            if "langchain" in content.lower():
                print("     🤖 Usa LangChain")
            if "openai" in content.lower():
                print("     🧠 Usa OpenAI")
        else:
            print(f"  ❌ NÃO EXISTE: {file_path}")

def analyze_components():
    """Analisa componentes React"""
    print("\n=== 🧩 ANÁLISE DE COMPONENTES REACT ===")
    
    # Procurar por componentes relacionados
    component_patterns = [
        "src/components/**/renus*.tsx",
        "src/components/**/isa*.tsx",
        "src/components/**/Renus*.tsx",
        "src/components/**/Isa*.tsx",
        "src/components/**/ISA*.tsx"
    ]
    
    import glob
    
    found_components = []
    for pattern in component_patterns:
        matches = glob.glob(pattern, recursive=True)
        found_components.extend(matches)
    
    if found_components:
        print("📦 COMPONENTES ENCONTRADOS:")
        for component in found_components:
            print(f"  ✅ {component}")
            
            with open(component, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = len(content.split('\n'))
            print(f"     📊 Linhas: {lines}")
            
            # Verificar funcionalidades
            if "useState" in content:
                print("     🔧 Gerencia estado")
            if "useEffect" in content:
                print("     🔄 Tem efeitos")
            if "fetch" in content or "axios" in content:
                print("     🌐 Faz requisições")
    else:
        print("❌ NENHUM COMPONENTE ESPECÍFICO ENCONTRADO")

def generate_summary():
    """Gera resumo da análise"""
    print("\n" + "="*60)
    print("📋 RESUMO DA ANÁLISE")
    print("="*60)
    
    print("\n🎯 MÓDULOS ANALISADOS:")
    print("1. RENUS Config (/dashboard/admin/renus-config)")
    print("2. Assistente ISA (/dashboard/admin/assistente-isa)")
    
    print("\n📊 ÁREAS VERIFICADAS:")
    print("✅ Rotas Frontend (App.tsx)")
    print("✅ Páginas React")
    print("✅ Rotas Backend (main.py)")
    print("✅ Arquivos de API")
    print("✅ Endpoints HTTP")
    print("✅ Tabelas do Banco")
    print("✅ Modelos Pydantic")
    print("✅ Services")
    print("✅ Componentes React")
    
    print("\n⚠️ IMPORTANTE:")
    print("Esta análise é APENAS INVESTIGATIVA")
    print("Nenhum arquivo foi alterado ou modificado")
    print("Relatório completo será gerado em arquivo separado")

if __name__ == "__main__":
    print("🔍 ANÁLISE COMPLETA DOS MÓDULOS RENUS E ISA")
    print("="*60)
    print("📅 Data:", "12/12/2025")
    print("🎯 Objetivo: Verificar implementação dos módulos")
    print("⚠️ Modo: SOMENTE LEITURA - Nenhuma alteração será feita")
    print("="*60)
    
    try:
        analyze_frontend_routes()
        analyze_frontend_pages()
        analyze_backend_routes()
        test_backend_endpoints()
        analyze_database_tables()
        analyze_services()
        analyze_components()
        generate_summary()
        
        print("\n🎉 ANÁLISE CONCLUÍDA!")
        print("📄 Relatório detalhado será gerado...")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE ANÁLISE: {e}")
        print("Análise interrompida, mas dados parciais podem estar disponíveis")