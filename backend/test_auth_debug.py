#!/usr/bin/env python3
"""
Script para debugar problemas de autenticação
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.supabase import supabase_client, supabase_admin
from src.services.auth_service import auth_service
from src.models.user import UserLogin


async def test_auth():
    """Testa sistema de autenticação"""
    
    print("=== TESTE DE AUTENTICAÇÃO ===")
    
    # 1. Verificar se existe usuário admin
    print("\n1. Verificando usuários existentes...")
    try:
        profiles = supabase_admin.table("profiles").select("*").execute()
        print(f"Usuários encontrados: {len(profiles.data)}")
        
        for profile in profiles.data:
            print(f"  - {profile.get('email', 'N/A')} | Role: {profile.get('role', 'N/A')} | ID: {profile.get('id', 'N/A')}")
            
        # Verificar se existe admin
        admin_profiles = [p for p in profiles.data if p.get('role') == 'admin']
        if not admin_profiles:
            print("❌ PROBLEMA: Nenhum usuário admin encontrado!")
            return False
        else:
            print(f"✅ {len(admin_profiles)} admin(s) encontrado(s)")
            
    except Exception as e:
        print(f"❌ Erro ao buscar profiles: {e}")
        return False
    
    # 2. Testar login com admin
    print("\n2. Testando login...")
    admin_email = admin_profiles[0].get('email')
    
    # Tentar algumas senhas comuns
    test_passwords = ['admin123', 'password', '123456', 'admin', 'renum123']
    
    for password in test_passwords:
        try:
            print(f"  Tentando: {admin_email} / {password}")
            
            login_data = UserLogin(email=admin_email, password=password)
            result = await auth_service.login(login_data)
            
            print(f"✅ LOGIN SUCESSO!")
            print(f"  Token: {result['access_token'][:50]}...")
            print(f"  User: {result['user'].name} ({result['user'].role})")
            
            # 3. Testar token
            print("\n3. Testando token...")
            user = await auth_service.get_current_user(result['access_token'])
            if user:
                print(f"✅ Token válido: {user.name} ({user.role})")
                print(f"\n🎯 TOKEN PARA USAR NO FRONTEND:")
                print(f"Bearer {result['access_token']}")
                return True
            else:
                print("❌ Token inválido")
                
        except Exception as e:
            print(f"  ❌ Falhou: {e}")
            continue
    
    print("❌ Nenhuma senha funcionou")
    return False


if __name__ == "__main__":
    success = asyncio.run(test_auth())
    if not success:
        print("\n🚨 PROBLEMAS ENCONTRADOS:")
        print("1. Verifique se existe usuário admin no Supabase")
        print("2. Verifique se a senha está correta")
        print("3. Verifique configuração do Supabase")