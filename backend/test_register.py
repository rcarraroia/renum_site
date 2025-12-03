"""
Script para testar registro de novo usuário
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    print("🔍 Testando Registro de Usuário...\n")
    
    # Dados de registro
    register_data = {
        "email": "auditoria@renum.com",
        "password": "Auditoria@2025",
        "first_name": "Auditoria",
        "last_name": "Kiro"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=register_data
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registro bem-sucedido!")
            print(f"\nToken: {data.get('access_token', 'N/A')[:50]}...")
            print(f"Token Type: {data.get('token_type', 'N/A')}")
            
            if 'user' in data:
                print(f"\nUsuário criado:")
                print(f"  ID: {data['user'].get('id', 'N/A')}")
                print(f"  Email: {data['user'].get('email', 'N/A')}")
                print(f"  Nome: {data['user'].get('first_name', 'N/A')} {data['user'].get('last_name', 'N/A')}")
                print(f"  Role: {data['user'].get('role', 'N/A')}")
            
            # Salvar token
            token = data.get('access_token')
            if token:
                with open('test_token.txt', 'w') as f:
                    f.write(token)
                print("\n💾 Token salvo em test_token.txt")
            
            return True
        else:
            print(f"❌ Erro no registro: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exceção: {e}")
        return False

if __name__ == "__main__":
    test_register()
