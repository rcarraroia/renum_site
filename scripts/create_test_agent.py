#!/usr/bin/env python3
"""
Script para criar agente de teste no banco
"""
import requests
import json

# Token válido
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjgxNzczLCJpYXQiOjE3NjU1OTUzNzMsInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Hhlrodg5Ks31ji9H7t80Z8EVEDopF0djbXV-J2wRfqE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def create_agent():
    """Cria agente via API"""
    print("=== CRIANDO AGENTE VIA API ===")
    
    agent_data = {
        "name": "Agente de Vendas Slim",
        "slug": "agente-vendas-slim",
        "description": "Agente especializado em vendas e atendimento ao cliente",
        "status": "active",
        "is_public": True,
        "system_prompt": "Você é um agente de vendas especializado. Seja profissional, prestativo e focado em ajudar o cliente.",
        "model": "gpt-4o-mini",
        "channel": "web",
        "template_type": "custom",
        "client_id": "876be331-9553-4e9a-9f29-63cfa711e056",
        "public_url": "https://agente-vendas-slim.renum.com.br",
        "config": {
            "temperature": 0.7,
            "max_tokens": 500,
            "tools": ["web_search", "calculator"]
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/agents/",
            headers=headers,
            json=agent_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            agent = response.json()
            print("✅ Agente criado com sucesso!")
            print(f"ID: {agent.get('id')}")
            print(f"Nome: {agent.get('name')}")
            print(f"Slug: {agent.get('slug')}")
            print(f"Status: {agent.get('status')}")
            return agent
        else:
            print(f"❌ Erro ao criar agente: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def create_second_agent():
    """Cria segundo agente para testes"""
    print("\n=== CRIANDO SEGUNDO AGENTE ===")
    
    agent_data = {
        "name": "Agente de Suporte",
        "slug": "agente-suporte",
        "description": "Agente especializado em suporte técnico e atendimento",
        "status": "active",
        "is_public": True,
        "system_prompt": "Você é um agente de suporte técnico. Seja paciente, detalhista e focado em resolver problemas.",
        "model": "gpt-4o-mini",
        "template_type": "support",
        "client_id": "876be331-9553-4e9a-9f29-63cfa711e056",
        "public_url": "https://agente-suporte.renum.com.br",
        "config": {
            "temperature": 0.5,
            "max_tokens": 800,
            "tools": ["knowledge_base", "ticket_system"]
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/agents/",
            headers=headers,
            json=agent_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            agent = response.json()
            print("✅ Segundo agente criado!")
            print(f"ID: {agent.get('id')}")
            print(f"Nome: {agent.get('name')}")
            print(f"Slug: {agent.get('slug')}")
            return agent
        else:
            print(f"❌ Erro: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def test_agents_list():
    """Testa listagem após criação"""
    print("\n=== VERIFICANDO AGENTES CRIADOS ===")
    
    try:
        response = requests.get("http://localhost:8000/api/agents/", headers=headers)
        
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ Total de agentes: {len(agents)}")
            
            for agent in agents:
                print(f"- {agent.get('name')} ({agent.get('slug')})")
                
            return agents
        else:
            print(f"❌ Erro: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

if __name__ == "__main__":
    # Criar agentes
    agent1 = create_agent()
    agent2 = create_second_agent()
    
    # Verificar resultado
    agents = test_agents_list()
    
    if agents:
        print(f"\n🎉 SUCESSO! {len(agents)} agente(s) criado(s) e pronto(s) para teste!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Atualizar token no frontend")
        print("2. Testar chat de teste com agentes reais")
        print("3. Validar integração completa")
    else:
        print("\n❌ FALHA! Nenhum agente foi criado.")