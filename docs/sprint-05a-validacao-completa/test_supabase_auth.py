"""
Script para testar autenticação direta no Supabase Auth
"""
from src.config.supabase import supabase_client

def test_supabase_auth():
    print("🔍 Testando Supabase Auth diretamente...\n")
    
    # Tentar login com credenciais conhecidas
    credentials = [
        {"email": "rcarraro2015@gmail.com", "password": "Renato@2015"},
        {"email": "rcarraro2015@gmail.com", "password": "renato2015"},
        {"email": "rcarraro2015@gmail.com", "password": "Renum@2025"},
    ]
    
    for cred in credentials:
        print(f"Tentando: {cred['email']} / {cred['password'][:5]}...")
        
        try:
            response = supabase_client.auth.sign_in_with_password({
                "email": cred["email"],
                "password": cred["password"]
            })
            
            if response.user:
                print(f"✅ LOGIN SUCESSO!")
                print(f"   User ID: {response.user.id}")
                print(f"   Email: {response.user.email}")
                print(f"   Token: {response.session.access_token[:50]}...")
                return True
            else:
                print(f"❌ Falhou")
                
        except Exception as e:
            print(f"❌ Erro: {str(e)[:100]}")
    
    print("\n⚠️ Nenhuma credencial funcionou!")
    print("\n📝 RECOMENDAÇÃO:")
    print("1. Acesse o Supabase Dashboard")
    print("2. Vá em Authentication → Users")
    print("3. Encontre o usuário rcarraro2015@gmail.com")
    print("4. Clique em 'Reset Password' ou crie novo usuário")
    
    return False

if __name__ == "__main__":
    test_supabase_auth()
