import requests

BASE_URL = "http://localhost:8000"
LOGIN_DATA = {
    "email": "rcarraro2015@gmail.com",
    "password": "M&151173c@"
}

def get_valid_client_id():
    r = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA)
    if r.status_code != 200:
        print("Login failed")
        return None
    
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    r = requests.get(f"{BASE_URL}/api/clients", headers=headers)
    if r.status_code == 200:
        clients = r.json().get("clients", [])
        if clients:
            print(f"VALID_CLIENT_ID={clients[0]['id']}")
            return clients[0]['id']
        else:
            print("No clients found")
    else:
        print(f"Failed to list clients: {r.status_code} - {r.text}")
    return None

if __name__ == "__main__":
    get_valid_client_id()
