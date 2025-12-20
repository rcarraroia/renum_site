"""
Script para testar endpoint de clientes
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Login
login_data = {
    "email": "rcarraro2015@gmail.com",
    "password": "M&151173c@"
}

print("=== Testando Login ===")
login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"Status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Testar endpoint de clientes
    print("\n=== Testando GET /api/clients ===")
    clients_response = requests.get(f"{BASE_URL}/api/clients", headers=headers)
    print(f"Status: {clients_response.status_code}")
    
    if clients_response.status_code == 200:
        clients = clients_response.json()
        print(f"Total de clientes: {len(clients)}")
        for client in clients:
            print(f"  - {client.get('company_name', 'N/A')} (ID: {client.get('id', 'N/A')})")
    else:
        print(f"Erro: {clients_response.text}")
    
    # 3. Testar endpoint de projetos
    print("\n=== Testando GET /api/projects ===")
    projects_response = requests.get(f"{BASE_URL}/api/projects", headers=headers)
    print(f"Status: {projects_response.status_code}")
    
    if projects_response.status_code == 200:
        projects = projects_response.json()
        print(f"Total de projetos: {len(projects)}")
        for project in projects:
            print(f"  - {project.get('name', 'N/A')} (ID: {project.get('id', 'N/A')})")
    else:
        print(f"Erro: {projects_response.text}")
else:
    print(f"Falha no login: {login_response.text}")
