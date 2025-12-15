"""Simple CRUD test to debug"""
import requests
import sys

print("Starting test...", flush=True)

# Read token
try:
    with open("test_token.txt", "r") as f:
        token = f.read().strip()
    print(f"Token loaded: {token[:20]}...", flush=True)
except Exception as e:
    print(f"Error reading token: {e}", flush=True)
    sys.exit(1)

# Test health
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"Health check: {response.status_code}", flush=True)
except Exception as e:
    print(f"Error in health check: {e}", flush=True)
    sys.exit(1)

# Test clients list
try:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:8000/api/clients", headers=headers, timeout=5)
    print(f"Clients list: {response.status_code}", flush=True)
    if response.status_code == 200:
        data = response.json()
        print(f"Clients count: {len(data.get('items', []))}", flush=True)
except Exception as e:
    print(f"Error listing clients: {e}", flush=True)

print("Test complete!", flush=True)
