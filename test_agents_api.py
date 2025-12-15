#!/usr/bin/env python3
"""
Script para testar a API de agentes
"""
import requests
import json

# Token válido
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjgxNzczLCJpYXQiOjE3NjU1OTUzNzMsInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Hhlrodg5Ks31ji9H7t80Z8EVEDopF0djbXV-J2wRfqE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_agents_list():
    """Testa listagem de agentes"""
    print("=== TESTANDO LISTAGEM DE AGENTES ===")
    
    try:
        response = requests.get("http://localhost:8000/api/agents/", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            agents = response.json()
            print(f"Agentes encontrados: {len(agents)}")
            
            for agent in agents:
                print(f"- ID: {agent.get('id')}")
                print(f"  Nome: {agent.get('name')}")
                print(f"  Slug: {agent.get('slug')}")
                print(f"  Status: {agent.get('status')}")
                print()
                
            return agents
        else:
            print(f"Erro: {response.text}")
            return []
            
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return []

def test_chat_endpoint(agent_slug):
    """Testa endpoint de chat público"""
    print(f"=== TESTANDO CHAT COM AGENTE: {agent_slug} ===")
    
    try:
        # Testar informações do agente
        response = requests.get(f"http://localhost:8000/api/chat/{agent_slug}")
        print(f"Status (info): {response.status_code}")
        
        if response.status_code == 200:
            info = response.json()
            print(f"Agente: {info.get('name')}")
            print(f"Descrição: {info.get('description')}")
            print(f"Modelo: {info.get('model')}")
        else:
            print(f"Erro (info): {response.text}")
            
        # Testar envio de mensagem
        message_data = {
            "message": "Olá, como você pode me ajudar?",
            "interview_id": None,
            "context": {}
        }
        
        response = requests.post(
            f"http://localhost:8000/api/chat/{agent_slug}/message",
            headers=headers,
            json=message_data
        )
        
        print(f"Status (message): {response.status_code}")
        
        if response.status_code == 200:
            chat_response = response.json()
            print(f"Resposta: {chat_response.get('message')}")
            print(f"Interview ID: {chat_response.get('interview_id')}")
            print(f"Completo: {chat_response.get('is_complete')}")
        else:
            print(f"Erro (message): {response.text}")
            
    except Exception as e:
        print(f"Erro na requisição: {e}")

if __name__ == "__main__":
    # Listar agentes
    agents = test_agents_list()
    
    # Se houver agentes, testar o primeiro
    if agents:
        first_agent = agents[0]
        agent_slug = first_agent.get('slug')
        if agent_slug:
            test_chat_endpoint(agent_slug)
        else:
            print("Agente não tem slug definido")
    else:
        print("Nenhum agente encontrado para testar")