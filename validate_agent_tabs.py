#!/usr/bin/env python3
"""
Script de Validação das Abas de Configuração dos Agentes
Testa se as funcionalidades são reais ou mock
"""
import requests
import json
from datetime import datetime

def print_header(title):
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_result(test_name, status, details=""):
    icons = {"real": "✅", "mock": "🟡", "broken": "❌", "unknown": "❓"}
    icon = icons.get(status, "❓")
    print(f"{icon} {test_name}: {status.upper()}")
    if details:
        print(f"   {details}")

def test_agents_endpoints():
    """Testa endpoints relacionados aos agentes"""
    print_header("VALIDAÇÃO DOS ENDPOINTS DE AGENTES")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjczMjM5LCJpYXQiOjE3NjU1ODY4MzksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.HgEqRYi7ijWwaqj1Vkt-ofRIB5dWY4bRyDNGiKMpDsk"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:8083"
    }
    
    base_url = "http://localhost:8000"
    
    # Teste 1: Listar agentes
    try:
        response = requests.get(f"{base_url}/api/agents", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            agents_count = len(data.get('items', []))
            print_result("Endpoint /api/agents", "real", f"Retornou {agents_count} agentes")
            
            # Se há agentes, testar busca por slug
            if agents_count > 0:
                first_agent = data['items'][0]
                agent_slug = first_agent.get('slug')
                if agent_slug:
                    slug_response = requests.get(f"{base_url}/api/agents/slug/{agent_slug}", headers=headers, timeout=5)
                    if slug_response.status_code == 200:
                        print_result("Endpoint /api/agents/slug/{slug}", "real", f"Slug '{agent_slug}' funciona")
                    else:
                        print_result("Endpoint /api/agents/slug/{slug}", "broken", f"Status: {slug_response.status_code}")
                else:
                    print_result("Campo slug nos agentes", "mock", "Agentes não têm slug")
        else:
            print_result("Endpoint /api/agents", "broken", f"Status: {response.status_code}")
    except Exception as e:
        print_result("Endpoint /api/agents", "broken", f"Erro: {e}")
    
    # Teste 2: Ferramentas (Tools)
    try:
        response = requests.get(f"{base_url}/api/tools", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            tools_count = len(data) if isinstance(data, list) else len(data.get('items', []))
            print_result("Endpoint /api/tools", "real", f"Retornou {tools_count} ferramentas")
        else:
            print_result("Endpoint /api/tools", "broken", f"Status: {response.status_code}")
    except Exception as e:
        print_result("Endpoint /api/tools", "broken", f"Erro: {e}")
    
    # Teste 3: Sub-agentes
    try:
        response = requests.get(f"{base_url}/api/sub-agents", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            subagents_count = len(data) if isinstance(data, list) else len(data.get('items', []))
            print_result("Endpoint /api/sub-agents", "real", f"Retornou {subagents_count} sub-agentes")
        else:
            print_result("Endpoint /api/sub-agents", "broken", f"Status: {response.status_code}")
    except Exception as e:
        print_result("Endpoint /api/sub-agents", "broken", f"Erro: {e}")
    
    # Teste 4: Integrações
    try:
        response = requests.get(f"{base_url}/api/integrations", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            integrations_count = len(data) if isinstance(data, list) else len(data.get('items', []))
            print_result("Endpoint /api/integrations", "real", f"Retornou {integrations_count} integrações")
        else:
            print_result("Endpoint /api/integrations", "broken", f"Status: {response.status_code}")
    except Exception as e:
        print_result("Endpoint /api/integrations", "broken", f"Erro: {e}")

def test_frontend_components():
    """Analisa componentes do frontend"""
    print_header("ANÁLISE DOS COMPONENTES FRONTEND")
    
    components_to_check = [
        ("InstructionsTab", "src/components/agents/config/InstructionsTab.tsx"),
        ("ToolsTab", "src/components/agents/config/ToolsTab.tsx"),
        ("IntegrationsTab", "src/components/agents/config/IntegrationsTab.tsx"),
        ("KnowledgeTab", "src/components/agents/config/KnowledgeTab.tsx"),
        ("TriggersTab", "src/components/agents/config/TriggersTab.tsx"),
        ("GuardrailsTab", "src/components/agents/config/GuardrailsTab.tsx"),
        ("SubAgentsTab", "src/components/agents/config/SubAgentsTab.tsx"),
        ("AdvancedTab", "src/components/agents/config/AdvancedTab.tsx"),
        ("ApiWebhooksTab", "src/components/agents/ApiWebhooksTab.tsx"),
        ("PreviewChat", "src/components/agents/PreviewChat.tsx"),
    ]
    
    for component_name, file_path in components_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Análise básica do conteúdo
            has_mock_data = "MOCK" in content.upper() or "mock" in content.lower()
            has_api_calls = "api." in content or "fetch(" in content or "axios." in content
            has_local_storage = "localStorage" in content
            has_real_logic = len(content) > 1000  # Componentes complexos tendem a ser mais reais
            
            if has_api_calls and not has_mock_data:
                status = "real"
                details = "Faz chamadas API reais"
            elif has_mock_data and not has_api_calls:
                status = "mock"
                details = "Usa dados mockados"
            elif has_local_storage:
                status = "mock"
                details = "Salva apenas no localStorage"
            elif has_real_logic:
                status = "unknown"
                details = "Lógica complexa, precisa verificar manualmente"
            else:
                status = "mock"
                details = "Componente simples, provavelmente mock"
            
            print_result(f"Componente {component_name}", status, details)
            
        except FileNotFoundError:
            print_result(f"Componente {component_name}", "broken", "Arquivo não encontrado")
        except Exception as e:
            print_result(f"Componente {component_name}", "unknown", f"Erro ao analisar: {e}")

def generate_summary():
    """Gera resumo da análise"""
    print_header("RESUMO E RECOMENDAÇÕES")
    
    print("📊 ANÁLISE CONCLUÍDA")
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. ✅ Implementar URLs com slug (backend já suporta)")
    print("2. ✅ Adicionar aba 'Chat de Teste' nas abas principais")
    print("3. 🔍 Verificar componentes marcados como 'unknown'")
    print("4. 🛠️ Corrigir componentes marcados como 'broken'")
    print("5. 🔄 Migrar componentes 'mock' para usar dados reais")
    
    print(f"\n📝 RELATÓRIO GERADO EM: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def main():
    """Executa validação completa das abas de agentes"""
    print("🚀 INICIANDO VALIDAÇÃO DAS ABAS DE AGENTES")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Testa endpoints do backend
    test_agents_endpoints()
    
    # Analisa componentes do frontend
    test_frontend_components()
    
    # Gera resumo
    generate_summary()

if __name__ == "__main__":
    main()