#!/usr/bin/env python3
"""
Validação Rápida do Orquestrador
Testa apenas os componentes essenciais
"""

import sys
import os
import requests
import json
from datetime import datetime

# Adicionar path do backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Carregar variáveis de ambiente do .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        from src.services.orchestrator_service import orchestrator_service
        print("✅ OrchestratorService importado")
    except Exception as e:
        print(f"❌ Erro ao importar OrchestratorService: {e}")
        return False
    
    try:
        from src.utils.openrouter_client import OpenRouterClient
        print("✅ OpenRouterClient importado")
    except Exception as e:
        print(f"❌ Erro ao importar OpenRouterClient: {e}")
        return False
    
    try:
        from src.services.lead_service import lead_service
        print("✅ LeadService importado")
    except Exception as e:
        print(f"❌ Erro ao importar LeadService: {e}")
        return False
    
    return True

def test_backend_running():
    """Testa se backend está rodando"""
    print("\n🔍 Testando se backend está rodando...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está rodando")
            return True
        else:
            print(f"❌ Backend retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando (Connection refused)")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar no backend: {e}")
        return False

def test_orchestrator_endpoints():
    """Testa endpoints do orquestrador"""
    print("\n🔍 Testando endpoints do orquestrador...")
    
    # Teste 1: Analyze
    try:
        data = {
            "message": "Quero saber sobre preços",
            "context": {"test": True}
        }
        response = requests.post(
            "http://localhost:8000/api/orchestrator/analyze",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ /analyze funcionando - Topics: {result.get('topics', [])}")
        else:
            print(f"❌ /analyze falhou - Status: {response.status_code}")
            print(f"   Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro no /analyze: {e}")
        return False
    
    # Teste 2: Route
    try:
        data = {
            "message": "Preciso de suporte técnico",
            "agent_id": "test-agent",
            "context": {"test": True}
        }
        response = requests.post(
            "http://localhost:8000/api/orchestrator/route",
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            should_route = result.get('should_route', False)
            print(f"✅ /route funcionando - Should route: {should_route}")
        else:
            print(f"❌ /route falhou - Status: {response.status_code}")
            print(f"   Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro no /route: {e}")
        return False
    
    return True

def main():
    """Validação rápida"""
    print("⚡ VALIDAÇÃO RÁPIDA DO ORQUESTRADOR")
    print("=" * 40)
    
    success_count = 0
    total_tests = 3
    
    # Teste 1: Imports
    if test_imports():
        success_count += 1
    
    # Teste 2: Backend
    if test_backend_running():
        success_count += 1
    
    # Teste 3: Endpoints
    if test_orchestrator_endpoints():
        success_count += 1
    
    # Resultado
    print("\n" + "=" * 40)
    print("📊 RESULTADO DA VALIDAÇÃO")
    print("=" * 40)
    print(f"✅ Sucessos: {success_count}/{total_tests}")
    print(f"❌ Falhas: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("\n🎉 VALIDAÇÃO PASSOU - ORQUESTRADOR FUNCIONANDO!")
        return True
    elif success_count >= 2:
        print("\n⚠️  VALIDAÇÃO PARCIAL - ALGUNS PROBLEMAS ENCONTRADOS")
        return False
    else:
        print("\n🚨 VALIDAÇÃO FALHOU - MUITOS PROBLEMAS")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)