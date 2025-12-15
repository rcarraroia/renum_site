"""
Script para testar trigger de auto-criação de profile
"""
from src.config.supabase import supabase_client, supabase_admin
import uuid

def test_trigger():
    print("🧪 Testando trigger de auto-criação de profile...\n")
    
    # Gerar email único
    test_email = f"teste.trigger.{uuid.uuid4().hex[:8]}@renum.com"
    
    test_user = {
        "email": test_email,
        "password": "Teste@123456",
        "first_name": "Teste",
        "last_name": "Trigger"
    }
    
    try:
        # Criar usuário
        print(f"1️⃣ Criando usuário: {test_email}")
        
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
        
        if not response.user:
            print("❌ Falha ao criar usuário")
            return False
        
        user_id = response.user.id
        print(f"✅ Usuário criado!")
        print(f"   ID: {user_id}")
        print(f"   Email: {response.user.email}")
        
        # Verificar se profile foi criado automaticamente
        print(f"\n2️⃣ Verificando se profile foi criado automaticamente...")
        
        import time
        time.sleep(1)  # Aguardar trigger executar
        
        profile = supabase_admin.table("profiles").select("*").eq(
            "id", user_id
        ).execute()
        
        if profile.data:
            print(f"✅ PROFILE CRIADO AUTOMATICAMENTE!")
            print(f"\n   Dados do profile:")
            print(f"   ID: {profile.data[0]['id']}")
            print(f"   Email: {profile.data[0]['email']}")
            print(f"   Nome: {profile.data[0]['first_name']} {profile.data[0]['last_name']}")
            print(f"   Role: {profile.data[0]['role']}")
            
            # Limpar teste
            print(f"\n3️⃣ Limpando dados de teste...")
            
            # Deletar profile
            supabase_admin.table("profiles").delete().eq("id", user_id).execute()
            
            # Deletar usuário do Auth
            supabase_admin.auth.admin.delete_user(user_id)
            
            print(f"✅ Dados de teste removidos")
            
            print("\n" + "="*70)
            print("✅ TRIGGER FUNCIONANDO PERFEITAMENTE!")
            print("="*70)
            
            return True
        else:
            print(f"❌ PROFILE NÃO FOI CRIADO!")
            print(f"\n⚠️ O trigger pode não estar funcionando")
            
            # Limpar usuário de teste
            supabase_admin.auth.admin.delete_user(user_id)
            
            return False
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_trigger()
    exit(0 if success else 1)
