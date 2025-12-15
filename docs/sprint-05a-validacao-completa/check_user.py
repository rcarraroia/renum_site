"""
Script para verificar usuários no banco
"""
from src.utils.supabase_client import get_client

def check_users():
    supabase = get_client()
    
    print("🔍 Verificando usuários no banco...\n")
    
    try:
        # Buscar todos os profiles
        result = supabase.table('profiles').select('*').execute()
        
        if result.data:
            print(f"✅ Encontrados {len(result.data)} usuário(s):\n")
            
            for user in result.data:
                print(f"ID: {user.get('id')}")
                print(f"Email: {user.get('email')}")
                print(f"Nome: {user.get('first_name')} {user.get('last_name')}")
                print(f"Role: {user.get('role')}")
                print(f"Criado em: {user.get('created_at')}")
                print("-" * 50)
        else:
            print("⚠️ Nenhum usuário encontrado no banco!")
            
    except Exception as e:
        print(f"❌ Erro ao buscar usuários: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_users()
