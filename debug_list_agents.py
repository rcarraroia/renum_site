import asyncio
import sys
import os
import json
from uuid import UUID
from dotenv import load_dotenv

# Carregar ambiente
load_dotenv("backend/.env")
sys.path.append("backend")

from src.config.supabase import supabase_admin
from src.models.agent import AgentListItem

async def test_service_logic():
    print("--- Testing AgentService.list_agents Logic ---")
    try:
        limit = 50
        offset = 0
        query = supabase_admin.table('agents').select('*')
        query = query.order('created_at', desc=True).range(offset, offset + limit - 1)
        response = query.execute()
        
        print(f"DB Result: {len(response.data)} agents.")
        for i, agent in enumerate(response.data):
            try:
                item = AgentListItem(**agent)
                print(f"[{i}] SUCCESS: {agent['name']}")
            except Exception as e:
                print(f"[{i}] SERIALIZATION FAILURE: {agent['name']} - {e}")
    except Exception as e:
        print(f"SERVICE LOGIC ERROR: {e}")

async def test_http_endpoint():
    print("\n--- Testing API REST Endpoint via HTTP ---")
    import requests
    BASE_URL = "http://localhost:8000"
    LOGIN_DATA = {"email": "rcarraro2015@gmail.com", "password": "M&151173c@"}
    
    try:
        # Login
        login_resp = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_DATA)
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.status_code} - {login_resp.text}")
            return
        
        token = login_resp.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Test Get User Profile (AuthService logic)
        user_resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"GET /auth/me Status: {user_resp.status_code}")
        if user_resp.status_code != 200:
            print(f"Auth Me Error: {user_resp.text}")
            
            # Direct DB check for profile
            print("Checking profiles table directly...")
            from src.config.supabase import supabase_admin
            user_id = login_resp.json().get("user", {}).get("id")
            if user_id:
                prof = supabase_admin.table("profiles").select("*").eq("id", user_id).execute()
                if not prof.data:
                    print(f"CRITICAL: Profile for user {user_id} NOT FOUND in DB!")
                else:
                    print(f"Profile found: {prof.data[0]}")
        
        # 3. List agents
        print(f"GET {BASE_URL}/api/agents...")
        r = requests.get(f"{BASE_URL}/api/agents", headers=headers)
        print(f"Status: {r.status_code}")
        if r.status_code != 200:
            print(f"Error Detail: {r.text}")
        else:
            print(f"Success! Found {len(r.json())} agents.")
    except Exception as e:
        print(f"HTTP REQUEST FAILED: {e}")

async def main():
    await test_service_logic()
    await test_http_endpoint()

if __name__ == "__main__":
    asyncio.run(main())
