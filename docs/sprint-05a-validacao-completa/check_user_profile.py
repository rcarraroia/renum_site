"""
Script para verificar profile do usuário no Supabase
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.supabase import supabase_admin

# ID do usuário
user_id = "876be331-9553-4e9a-9f29-63cfa711e056"
email = "rcarraro2015@gmail.com"

print(f"\n🔍 Verificando usuário: {email}")
print(f"📋 User ID: {user_id}\n")

# Verificar se profile existe
try:
    response = supabase_admin.table("profiles").select("*").eq("id", user_id).execute()
    
    if response.data:
        print("✅ Profile encontrado:")
        profile = response.data[0]
        print(f"   - ID: {profile.get('id')}")
        print(f"   - Email: {profile.get('email')}")
        print(f"   - First Name: {profile.get('first_name')}")
        print(f"   - Last Name: {profile.get('last_name')}")
        print(f"   - Role: {profile.get('role')}")
        print(f"   - Created: {profile.get('created_at')}")
        print(f"   - Updated: {profile.get('updated_at')}")
    else:
        print("❌ Profile NÃO encontrado!")
        print("\n🔧 Criando profile...")
        
        # Criar profile
        new_profile = {
            "id": user_id,
            "email": email,
            "first_name": "Admin",
            "last_name": "Renum",
            "role": "admin"
        }
        
        create_response = supabase_admin.table("profiles").insert(new_profile).execute()
        
        if create_response.data:
            print("✅ Profile criado com sucesso!")
            print(f"   - Role: admin")
        else:
            print("❌ Erro ao criar profile")
            
except Exception as e:
    print(f"❌ Erro: {str(e)}")

print("\n" + "="*50)
