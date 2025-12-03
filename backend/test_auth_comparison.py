"""
Comparar login direto Supabase vs auth_service
"""
import asyncio
from src.config.supabase import supabase_client
from src.services.auth_service import auth_service
from src.models.user import UserLogin

async def test_auth():
    print("🔍 Teste 1: Login DIRETO no Supabase")
    print("="*60)
    
    try:
        response = supabase_client.auth.sign_in_with_password({
            "email": "kiro.auditoria@renum.com",
            "password": "kiro123"
        })
        
        if response.user:
            print("✅ Login direto SUCESSO")
            print(f"User ID: {response.user.id}")
            print(f"Email: {response.user.email}")
            print(f"Token: {response.session.access_token[:50]}...")
        else:
            print("❌ Login direto FALHOU")
            
    except Exception as e:
        print(f"❌ ERRO no login direto: {str(e)}")
    
    print()
    print("🔍 Teste 2: Login via AUTH_SERVICE")
    print("="*60)
    
    try:
        credentials = UserLogin(
            email="kiro.auditoria@renum.com",
            password="kiro123"
        )
        
        result = await auth_service.login(credentials)
        
        print("✅ Login via service SUCESSO")
        print(f"Token: {result.get('access_token', 'N/A')[:50]}...")
        print(f"User: {result.get('user', {})}")
        
    except Exception as e:
        print(f"❌ ERRO no login via service: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_auth())
