"""
Script para verificar status do usuário no Supabase Auth
"""
from src.config.supabase import supabase_admin

def check_auth_users():
    print("🔍 Verificando usuários no Supabase Auth...\n")
    
    try:
        # Listar usuários (requer admin)
        # Nota: Isso pode não funcionar dependendo das permissões
        response = supabase_admin.auth.admin.list_users()
        
        if hasattr(response, 'users') and response.users:
            print(f"✅ Encontrados {len(response.users)} usuário(s) no Auth:\n")
            
            for user in response.users:
                print(f"ID: {user.id}")
                print(f"Email: {user.email}")
                print(f"Email Confirmed: {user.email_confirmed_at is not None}")
                print(f"Created: {user.created_at}")
                print(f"Last Sign In: {user.last_sign_in_at}")
                print("-" * 50)
        else:
            print("⚠️ Não foi possível listar usuários ou nenhum usuário encontrado")
            print("Isso pode ser uma limitação de permissões")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\n📝 NOTA:")
        print("A listagem de usuários do Auth requer permissões especiais.")
        print("Verifique manualmente no Supabase Dashboard → Authentication → Users")

if __name__ == "__main__":
    check_auth_users()
