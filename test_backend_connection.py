#!/usr/bin/env python3
"""
Script para testar conexão com o backend
"""
import requests
import json

def test_backend():
    base_url = "http://localhost:8000"
    
    print("🔍 Testando conexão com backend...")
    print(f"URL: {base_url}")
    
    # Teste 1: Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Health check falhou: {e}")
        return False
    
    # Teste 2: Dashboard stats
    try:
        response = requests.get(f"{base_url}/api/dashboard/stats", timeout=5)
        print(f"✅ Dashboard stats: {response.status_code}")
        if response.status_code == 200:
            print(f"   Resposta: {response.json()}")
    except Exception as e:
        print(f"❌ Dashboard stats falhou: {e}")
    
    # Teste 3: Projects
    try:
        response = requests.get(f"{base_url}/api/projects", timeout=5)
        print(f"✅ Projects: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total projetos: {len(data.get('items', []))}")
    except Exception as e:
        print(f"❌ Projects falhou: {e}")
    
    return True

if __name__ == "__main__":
    test_backend()