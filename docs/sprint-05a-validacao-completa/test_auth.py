"""
Script para testar autenticação
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_login():
    print("🔍 Testando Login...\n")
    
    # Dados de login
    login_data = {
        "email": "rcarraro2015@gmail.com",
        "password": "Renato@2015"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login bem-sucedido!")
            print(f"\nToken: {data.get('access_token', 'N/A')[:50]}...")
            print(f"Token Type: {data.get('token_type', 'N/A')}")
            
            if 'user' in data:
                print(f"\nUsuário:")
                print(f"  ID: {data['user'].get('id', 'N/A')}")
                print(f"  Email: {data['user'].get('email', 'N/A')}")
                print(f"  Role: {data['user'].get('role', 'N/A')}")
            
            return data.get('access_token')
        else:
            print(f"❌ Erro no login: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return None

def test_me(token):
    print("\n\n🔍 Testando /api/auth/me...\n")
    
    if not token:
        print("❌ Token não disponível")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint /me funcionando!")
            print(f"\nDados do usuário:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False

if __name__ == "__main__":
    token = test_login()
    
    if token:
        test_me(token)
        
        # Salvar token para outros testes
        with open('test_token.txt', 'w') as f:
            f.write(token)
        print("\n💾 Token salvo em test_token.txt")
