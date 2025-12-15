#!/usr/bin/env python3
"""
Gera token de teste para debugging usando service_role
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.supabase import supabase_admin
import jwt
from datetime import datetime, timedelta


def generate_test_token():
    """Gera token JWT para teste"""
    
    print("=== GERADOR DE TOKEN DE TESTE ===")
    
    # 1. Buscar usuário admin
    try:
        profiles = supabase_admin.table("profiles").select("*").eq("role", "admin").execute()
        
        if not profiles.data:
            print("❌ Nenhum admin encontrado")
            return None
            
        admin = profiles.data[0]
        print(f"✅ Admin encontrado: {admin['email']}")
        
        # 2. Gerar JWT token manualmente
        # Usar o mesmo formato que o Supabase usa
        payload = {
            "iss": "supabase",
            "ref": "vhixvzaxswphwoymdhgg",  # Project ref
            "role": "authenticated",
            "aud": "authenticated",
            "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp()),
            "iat": int(datetime.utcnow().timestamp()),
            "sub": admin["id"],
            "email": admin["email"],
            "phone": "",
            "app_metadata": {
                "provider": "email",
                "providers": ["email"]
            },
            "user_metadata": {
                "email": admin["email"],
                "first_name": admin.get("first_name", ""),
                "last_name": admin.get("last_name", "")
            }
        }
        
        # JWT Secret do Supabase
        jwt_secret = "39864Ub2rWjFWbDUvMrbQfu4lmHe9Fiv/auohpenbEx0CTYl+Gb7flinlEIdgc9xLgfhL9BUZqCjRjs7s3yhHg=="
        
        # Gerar token
        token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        
        print(f"\n🎯 TOKEN GERADO:")
        print(f"Bearer {token}")
        
        print(f"\n📋 DADOS DO USUÁRIO:")
        print(f"ID: {admin['id']}")
        print(f"Email: {admin['email']}")
        print(f"Role: {admin['role']}")
        
        return token
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


if __name__ == "__main__":
    token = generate_test_token()
    
    if token:
        print(f"\n✅ Use este token no localStorage do frontend:")
        print(f"localStorage.setItem('renum_token', '{token}');")
        
        print(f"\n✅ Ou teste diretamente no curl:")
        print(f'curl -H "Authorization: Bearer {token}" http://localhost:8000/api/dashboard/stats')
    else:
        print("\n❌ Falha ao gerar token")