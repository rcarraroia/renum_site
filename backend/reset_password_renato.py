"""
Reset senha do usuário Renato
"""
from src.config.supabase import supabase_admin

def reset_password():
    print("🔧 Resetando senha do usuário...")
    
    admin_email = "rcarraro2015@gmail.com"
    new_password = "M&151173c@"
    
    try:
        # Buscar profile
        print(f"1️⃣ Buscando profile: {admin_email}")
        profile = supabase_admin.table("profiles").select("*").eq(
            "email", admin_email
        ).execute()
        
        if not profile.data:
            print(f"❌ Profile não encontrado!")
            return False
        
        user_id = profile.data[0]['id']
        print(f"✅ Profile encontrado! ID: {user_id}")
        
        # Atualizar senha
        print(f"\n2️⃣ Atualizando senha...")
        update_response = supabase_admin.auth.admin.update_user_by_id(
            user_id,
            {
                "password": new_password,
                "email_confirm": True
            }
        )
        
        print(f"✅ Senha atualizada com sucesso!")
        print(f"\n📋 CREDENCIAIS:")
        print(f"   Email: {admin_email}")
        print(f"   Senha: {new_password}")
        print(f"\n🎯 Agora você pode fazer login!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    reset_password()
