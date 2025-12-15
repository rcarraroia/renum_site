#!/usr/bin/env python3
"""
Script para testar conexão com o backend - versão corrigida
"""
import requests
import json

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🔍 Testando conexão com backend...")
    print(f"URL: {base_url}")
    
    # Teste 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint falhou: {e}")
        return False
    
    # Teste 2: Health check correto
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Health check falhou: {e}")
    
    # Teste 3: Database health
    try:
        response = requests.get(f"{base_url}/health/db", timeout=5)
        print(f"✅ Database health: {response.status_code}")
        if response.status_code == 200:
            print(f"   Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Database health falhou: {e}")
    
    print("\n🔍 Testando endpoints que precisam de auth...")
    
    # Teste 4: Dashboard stats (sem auth)
    try:
        response = requests.get(f"{base_url}/api/dashboard/stats", timeout=5)
        print(f"⚠️  Dashboard stats (sem auth): {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Corretamente protegido por autenticação")
    except Exception as e:
        print(f"❌ Dashboard stats falhou: {e}")
    
    return True

if __name__ == "__main__":
    test_backend()