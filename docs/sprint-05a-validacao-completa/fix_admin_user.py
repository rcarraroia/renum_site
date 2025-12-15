"""
Script para cadastrar usuário admin no Supabase Auth
"""
from src.config.supabase import supabase_admin

def fix_admin_user():
    print("🔧 Cadastrando usuário admin no Supabase Auth...\n")
    
    admin_data = {
        "email": "rcarraro2015@gmail.com",
        "password": "Renato@2015",  # Senha padrão - DEVE SER ALTERADA
        "email_confirm": True,  # Confirmar email automaticamente
        "user_metadata": {
            "first_name": "Admin",
            "last_name": "Renum"
        }
    }
    
    try:
        # Criar usuário no Auth
        print(f"Criando usuário: {admin_data['email']}")
        
        response = supabase_admin.auth.admin.create_user({
            "email": admin_data["email"],
            "password": admin_data["password"],
            "email_confirm": admin_data["email_confirm"],
            "user_metadata": admin_data["user_metadata"]
        })
        
        if response.user:
            print(f"✅ Usuário criado no Auth!")
            print(f"   User ID: {response.user.id}")
            print(f"   Email: {response.user.email}")
            print(f"   Email Confirmed: {response.user.email_confirmed_at}")
            
            # Verificar se profile já existe
            print("\nVerificando profile existente...")
            profile_check = supabase_admin.table("profiles").select("*").eq(
                "email", admin_data["email"]
            ).execute()
            
            if profile_check.data:
                print(f"✅ Profile já existe!")
                print(f"   ID: {profile_check.data[0]['id']}")
                
                # Atualizar ID do profile para corresponder ao Auth
                if profile_check.data[0]['id'] != response.user.id:
                    print("\n⚠️ IDs diferentes! Atualizando...")
                    
                    # Deletar profile antigo
                    supabase_admin.table("profiles").delete().eq(
                        "id", profile_check.data[0]['id']
                    ).execute()
                    
                    # Criar novo profile com ID correto
                    supabase_admin.table("profiles").insert({
                        "id": response.user.id,
                        "email": admin_data["email"],
                        "first_name": "Admin",
                        "last_name": "Renum",
                        "role": "admin"
                    }).execute()
                    
                    print("   ✅ Profile atualizado com ID correto")
            else:
                print("⚠️ Profile não existe, criando...")
                
                supabase_admin.table("profiles").insert({
                    "id": response.user.id,
                    "email": admin_data["email"],
                    "first_name": "Admin",
                    "last_name": "Renum",
                    "role": "admin"
                }).execute()
                
                print("   ✅ Profile criado")
            
            print("\n" + "="*70)
            print("✅ USUÁRIO ADMIN CONFIGURADO COM SUCESSO!")
            print("="*70)
            print(f"\nCredenciais:")
            print(f"  Email: {admin_data['email']}")
            print(f"  Senha: {admin_data['password']}")
            print(f"\n⚠️ IMPORTANTE: Altere a senha no primeiro login!")
            
            return True
        else:
            print("❌ Falha ao criar usuário")
            return False
            
    except Exception as e:
        error_msg = str(e)
        
        if "already been registered" in error_msg or "already exists" in error_msg:
            print(f"⚠️ Usuário já existe no Auth!")
            print(f"\n📝 SOLUÇÃO:")
            print(f"1. Acesse: https://supabase.com/dashboard/project/vhixvzaxswphwoymdhgg")
            print(f"2. Vá em Authentication → Users")
            print(f"3. Encontre {admin_data['email']}")
            print(f"4. Clique em 'Send password reset email'")
            print(f"5. OU delete o usuário e execute este script novamente")
            return False
        else:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = fix_admin_user()
    exit(0 if success else 1)
