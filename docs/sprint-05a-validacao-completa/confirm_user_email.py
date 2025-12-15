"""
Script para confirmar email do usuário manualmente
"""
from src.config.supabase import supabase_admin

def confirm_user_email():
    print("🔍 Confirmando email do usuário...\n")
    
    user_email = "kiro.auditoria@renum.com"
    user_id = "53e08888-c9cd-4cd3-b2d9-856a9ddaf780"
    
    try:
        # Atualizar usuário para confirmar email
        print(f"Confirmando email para: {user_email}")
        
        response = supabase_admin.auth.admin.update_user_by_id(
            user_id,
            {
                "email_confirm": True
            }
        )
        
        print(f"✅ Email confirmado!")
        print(f"User ID: {response.user.id}")
        print(f"Email: {response.user.email}")
        print(f"Email Confirmed: {response.user.email_confirmed_at}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    confirm_user_email()
