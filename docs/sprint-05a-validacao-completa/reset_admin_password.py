"""
Script para resetar senha do usuário admin
"""
from src.config.supabase import supabase_admin

def reset_admin_password():
    print("🔧 Resetando senha do usuário admin...\n")
    
    admin_email = "rcarraro2015@gmail.com"
    new_password = "Renato@2015"
    
    try:
        # Buscar usuário pelo email
        print(f"Buscando usuário: {admin_email}")
        
        # Listar usuários para encontrar o ID
        users_response = supabase_admin.auth.admin.list_users()
        
        admin_user = None
        if hasattr(users_response, 'users'):
            for user in users_response.users:
                if user.email == admin_email:
                    admin_user = user
                    break
        
        if not admin_user:
            print(f"❌ Usuário não encontrado no Auth")
            print(f"\n📝 Vou criar o usuário...")
            
            # Criar usuário
            response = supabase_admin.auth.admin.create_user({
                "email": admin_email,
                "password": new_password,
                "email_confirm": True,
                "user_metadata": {
                    "first_name": "Admin",
                    "last_name": "Renum"
                }
            })
            
            if response.user:
                admin_user = response.user
                print(f"✅ Usuário criado!")
            else:
                print(f"❌ Falha ao criar usuário")
                return False
        
        print(f"✅ Usuário encontrado!")
        print(f"   User ID: {admin_user.id}")
        print(f"   Email: {admin_user.email}")
        
        # Atualizar senha
        print(f"\nAtualizando senha...")
        
        update_response = supabase_admin.auth.admin.update_user_by_id(
            admin_user.id,
            {
                "password": new_password,
                "email_confirm": True
            }
        )
        
        print(f"✅ Senha atualizada!")
        
        # Verificar/criar profile
        print(f"\nVerificando profile...")
        
        profile = supabase_admin.table("profiles").select("*").eq(
            "id", admin_user.id
        ).execute()
        
        if not profile.data:
            print(f"⚠️ Profile não existe, criando...")
            
            supabase_admin.table("profiles").insert({
                "id": admin_user.id,
                "email": admin_email,
                "first_name": "Admin",
                "last_name": "Renum",
                "role": "admin"
            }).execute()
            
            print(f"✅ Profile criado!")
        else:
            print(f"✅ Profile já existe!")
            
            # Garantir que é admin
            if profile.data[0].get('role') != 'admin':
                supabase_admin.table("profiles").update({
                    "role": "admin"
                }).eq("id", admin_user.id).execute()
                print(f"✅ Role atualizado para admin!")
        
        print("\n" + "="*70)
        print("✅ USUÁRIO ADMIN CONFIGURADO COM SUCESSO!")
        print("="*70)
        print(f"\nCredenciais:")
        print(f"  Email: {admin_email}")
        print(f"  Senha: {new_password}")
        print(f"\n📝 Teste o login agora!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = reset_admin_password()
    exit(0 if success else 1)
