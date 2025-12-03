"""
Script final para corrigir usuário admin
"""
from src.config.supabase import supabase_admin

def fix_admin_final():
    print("🔧 Corrigindo usuário admin (abordagem alternativa)...\n")
    
    admin_email = "rcarraro2015@gmail.com"
    
    try:
        # Buscar profile existente
        print(f"1️⃣ Buscando profile: {admin_email}")
        
        profile = supabase_admin.table("profiles").select("*").eq(
            "email", admin_email
        ).execute()
        
        if not profile.data:
            print(f"❌ Profile não encontrado!")
            return False
        
        user_id = profile.data[0]['id']
        print(f"✅ Profile encontrado!")
        print(f"   ID: {user_id}")
        print(f"   Role: {profile.data[0].get('role')}")
        
        # Tentar atualizar senha usando o ID
        print(f"\n2️⃣ Atualizando senha do usuário...")
        
        try:
            update_response = supabase_admin.auth.admin.update_user_by_id(
                user_id,
                {
                    "password": "Renato@2015",
                    "email_confirm": True
                }
            )
            
            print(f"✅ Senha atualizada com sucesso!")
            print(f"   Email confirmado: {update_response.user.email_confirmed_at}")
            
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                print(f"❌ Usuário não existe no Auth!")
                print(f"\n📝 PROBLEMA IDENTIFICADO:")
                print(f"   - Profile existe na tabela 'profiles'")
                print(f"   - Mas usuário NÃO existe no Supabase Auth")
                print(f"\n🔧 SOLUÇÃO:")
                print(f"   Precisamos criar o usuário no Auth com o mesmo ID do profile")
                print(f"\n⚠️ Isso requer acesso ao Dashboard do Supabase:")
                print(f"   1. Acesse: https://supabase.com/dashboard/project/vhixvzaxswphwoymdhgg")
                print(f"   2. Vá em Authentication → Users")
                print(f"   3. Clique em 'Add user'")
                print(f"   4. Email: {admin_email}")
                print(f"   5. Senha: Renato@2015")
                print(f"   6. Confirme o email automaticamente")
                print(f"\n   OU use o usuário de teste já criado:")
                print(f"   Email: kiro.auditoria@renum.com")
                print(f"   Senha: Auditoria@2025!")
                
                return False
            else:
                raise
        
        # Garantir que role é admin
        print(f"\n3️⃣ Verificando role...")
        
        if profile.data[0].get('role') != 'admin':
            supabase_admin.table("profiles").update({
                "role": "admin"
            }).eq("id", user_id).execute()
            print(f"✅ Role atualizado para admin!")
        else:
            print(f"✅ Role já é admin!")
        
        print("\n" + "="*70)
        print("✅ USUÁRIO ADMIN CORRIGIDO!")
        print("="*70)
        print(f"\nCredenciais:")
        print(f"  Email: {admin_email}")
        print(f"  Senha: Renato@2015")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_admin_final()
    exit(0 if success else 1)
