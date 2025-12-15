"""
Script para criar usuário de teste no Supabase Auth
"""
from src.config.supabase import supabase_client, supabase_admin
import uuid

def create_test_user():
    print("🔍 Criando usuário de teste...\n")
    
    test_user = {
        "email": "kiro.auditoria@renum.com",
        "password": "Auditoria@2025!",
        "first_name": "Kiro",
        "last_name": "Auditoria"
    }
    
    try:
        # Criar no Supabase Auth
        print(f"Criando usuário: {test_user['email']}")
        
        response = supabase_client.auth.sign_up({
            "email": test_user["email"],
            "password": test_user["password"],
            "options": {
                "data": {
                    "first_name": test_user["first_name"],
                    "last_name": test_user["last_name"]
                }
            }
        })
        
        if response.user:
            print(f"✅ Usuário criado no Auth!")
            print(f"   User ID: {response.user.id}")
            print(f"   Email: {response.user.email}")
            
            # Verificar se profile foi criado
            print("\nVerificando profile...")
            profile = supabase_admin.table("profiles").select("*").eq(
                "id", response.user.id
            ).execute()
            
            if profile.data:
                print(f"✅ Profile criado automaticamente!")
                print(f"   Role: {profile.data[0].get('role', 'N/A')}")
                
                # Atualizar role para admin
                print("\nAtualizando role para admin...")
                supabase_admin.table("profiles").update({
                    "role": "admin"
                }).eq("id", response.user.id).execute()
                
                print("✅ Role atualizado para admin!")
            else:
                print("⚠️ Profile não foi criado automaticamente")
                print("Criando profile manualmente...")
                
                supabase_admin.table("profiles").insert({
                    "id": response.user.id,
                    "email": test_user["email"],
                    "first_name": test_user["first_name"],
                    "last_name": test_user["last_name"],
                    "role": "admin"
                }).execute()
                
                print("✅ Profile criado manualmente!")
            
            print("\n" + "="*50)
            print("✅ USUÁRIO DE TESTE CRIADO COM SUCESSO!")
            print("="*50)
            print(f"Email: {test_user['email']}")
            print(f"Senha: {test_user['password']}")
            print("="*50)
            
            return True
        else:
            print("❌ Falha ao criar usuário")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_test_user()
