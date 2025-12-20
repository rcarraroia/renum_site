import requests
import json
import sys

BASE_URL = "http://localhost:8000"
LOGIN_DATA = {
    "email": "rcarraro2015@gmail.com",
    "password": "M&151173c@"
}

REF_AGENTS = {
    "RENUS": "00000000-0000-0000-0000-000000000001",
    "ISA": "00000000-0000-0000-0000-000000000002"
}

def test_api():
    results = {}
    
    # 1. Health Check
    try:
        r = requests.get(f"{BASE_URL}/health")
        results["health"] = r.status_code == 200
        print(f"Health Check: {r.status_code}")
    except Exception as e:
        results["health"] = False
        print(f"Health Check Failed: {e}")

    # 2. Login
    token = None
    try:
        # Tentar login via form-data (comum em FastAPI OAuth2)
        r = requests.post(f"{BASE_URL}/auth/login", data=LOGIN_DATA)
        if r.status_code != 200:
             # Tentar via JSON caso não seja form-data
             r = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA)
        
        print(f"Login Response: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            token = data.get("access_token")
            results["login"] = True
        else:
            results["login"] = False
            print(f"Login Data: {r.text}")
    except Exception as e:
        results["login"] = False
        print(f"Login Failed: {e}")

    if not token:
        print("Testes interrompidos: Token não obtido")
        return results

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Validar RENUS e ISA exist
    for name, agent_id in REF_AGENTS.items():
        try:
            r = requests.get(f"{BASE_URL}/api/agents/{agent_id}", headers=headers)
            results[f"agent_{name}"] = r.status_code == 200
            print(f"Validar {name} ({agent_id}): {r.status_code}")
        except Exception as e:
            results[f"agent_{name}"] = False

    # 4. Testar ISA Chat (Real)
    try:
        chat_data = {
            "agent_id": REF_AGENTS["ISA"],
            "message": "Olá ISA, você está funcionando?",
            "stream": False
        }
        # Ajustar endpoint com base no que vimos no router (/api/isa ou similar)
        r = requests.post(f"{BASE_URL}/api/isa/chat", json=chat_data, headers=headers)
        if r.status_code != 200:
             # Tentar endpoint alternativo se falhar
             r = requests.post(f"{BASE_URL}/api/conversations/messages", json=chat_data, headers=headers)
        
        results["isa_chat"] = r.status_code == 200
        print(f"ISA Chat Test: {r.status_code}")
        if r.status_code == 200:
            print(f"ISA Response Sample: {r.json().get('response', 'N/A')[:50]}...")
    except Exception as e:
        results["isa_chat"] = False

    # 5. Listar Agentes
    try:
        r = requests.get(f"{BASE_URL}/api/agents", headers=headers)
        results["list_agents"] = r.status_code == 200
        print(f"List Agents: {r.status_code}")
        if r.status_code == 200:
            print(f"Total Agentes Encontrados: {len(r.json())}")
    except Exception as e:
        results["list_agents"] = False

    return results

if __name__ == "__main__":
    test_results = test_api()
    with open("api_test_results.json", "w") as f:
        json.dump(test_results, f, indent=4)
