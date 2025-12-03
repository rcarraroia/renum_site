"""
Script para testar login direto no Supabase
"""
from src.config.supabase import supabase_client

def test_direct_login():
    print("🔍 Testando login direto no Supabase...\n")
    
    credentials = {
        "email": "kiro.auditoria@renum.com",
        "password": "Auditoria@2025!"
    }
    
    print(f"Tentando login com: {credentials['email']}")
    
    try:
        response = supabase_client.auth.sign_in_with_password(credentials)
        
        print(f"\n✅ LOGIN SUCESSO!")
        print(f"User ID: {response.user.id}")
        print(f"Email: {response.user.email}")
        print(f"Email Confirmed: {response.user.email_confirmed_at}")
        print(f"Token: {response.session.access_token[:50]}...")
        
        # Salvar token
        with open('test_token.txt', 'w') as f:
            f.write(response.session.access_token)
        print("\n💾 Token salvo em test_token.txt")
        
        return response.session.access_token
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_direct_login()
