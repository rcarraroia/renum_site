import requests
import json

BASE_URL = "http://localhost:8000"
LOGIN_DATA = {
    "email": "rcarraro2015@gmail.com",
    "password": "M&151173c@"
}

def debug_list_agents():
    # 1. Login
    r = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA)
    if r.status_code != 200:
        print(f"Login failed: {r.status_code} - {r.text}")
        return
    
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. List agents
    print("Testing /api/agents...")
    r = requests.get(f"{BASE_URL}/api/agents", headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Detail: {r.text}")

    # 3. Test Wizard Start
    print("\nTesting /api/agents/wizard/start...")
    # client_id can be None for system agents or a valid client ID
    r = requests.post(f"{BASE_URL}/api/agents/wizard/start", json={"client_id": None}, headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Detail: {r.text}")

if __name__ == "__main__":
    debug_list_agents()
