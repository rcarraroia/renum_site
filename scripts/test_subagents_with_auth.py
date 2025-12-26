#!/usr/bin/env python3
"""
Script para testar o endpoint de sub-agentes com autenticação
"""

import sys
import os
import requests
import json
from datetime import datetime

def test_login_and_subagents():
    """Testa login e depois acessa sub-agentes"""
    print("🔐 Testando endpoint de sub-agentes com autenticação...")
    print("=" * 60)
    
    # Primeiro, fazer login para obter token
    login_url = "http://localhost:8000/auth/login"
    login_data = {
        "email": "admin@renum.com",
        "password": "admin123"
    }
    
    try:
        print("🔑 Fazendo login...")
        login_response = requests.post(login_url, json=login_data)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('access_token')
            print(f"✅ Login realizado com sucesso!")
            print(f"🎫 Token obtido: {token[:50]}...")
            
            # Agora testar endpoint de sub-agentes com token
            agent_id = "00000000-0000-0000-0000-000000000001"
            subagents_url = f"http://localhost:8000/api/agents/{agent_id}/sub-agents"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print(f"\n📡 Testando endpoint de sub-agentes...")
            print(f"🔗 URL: {subagents_url}")
            
            subagents_response = requests.get(subagents_url, headers=headers)
            
            print(f"📊 Status Code: {subagents_response.status_code}")
            
            if subagents_response.status_code == 200:
                data = subagents_response.json()
                print(f"✅ Endpoint funcionando com autenticação!")
                print(f"📊 Retornou {len(data)} sub-agentes")
                
                if data:
                    print("\n📋 Primeiro sub-agente:")
                    print(json.dumps(data[0], indent=2, default=str))
                
                return True
                
            else:
                print(f"❌ Erro no endpoint de sub-agentes: {subagents_response.status_code}")
                print(f"📄 Resposta: {subagents_response.text}")
                return False
                
        else:
            print(f"❌ Erro no login: {login_response.status_code}")
            print(f"📄 Resposta: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 Teste do Endpoint de Sub-Agentes com Autenticação")
    print("=" * 60)
    
    success = test_login_and_subagents()
    
    if success:
        print("\n✅ RESULTADO: Endpoint de sub-agentes funciona com autenticação!")
        return 0
    else:
        print("\n❌ RESULTADO: Endpoint de sub-agentes tem problemas com autenticação!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)