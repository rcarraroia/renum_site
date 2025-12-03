"""
Testar decodificação do token com diferentes chaves
"""
import jwt
from src.config.settings import settings

token = open('test_token.txt').read().strip()

print("="*70)
print("TESTE DE DECODIFICAÇÃO JWT")
print("="*70)

# Teste 1: Com SECRET_KEY
print("\n1. Tentando com SECRET_KEY...")
try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    print("   ✅ SUCESSO!")
    print(f"   User ID: {payload.get('sub')}")
except Exception as e:
    print(f"   ❌ FALHOU: {str(e)[:100]}")

# Teste 2: Com SUPABASE_JWT_SECRET
print("\n2. Tentando com SUPABASE_JWT_SECRET...")
try:
    payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=["HS256"])
    print("   ✅ SUCESSO!")
    print(f"   User ID: {payload.get('sub')}")
except Exception as e:
    print(f"   ❌ FALHOU: {str(e)[:100]}")

# Teste 2b: Com SUPABASE_JWT_SECRET (sem verificar audience)
print("\n2b. Tentando com SUPABASE_JWT_SECRET (sem verificar audience)...")
try:
    payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
    print("   ✅ SUCESSO!")
    print(f"   User ID: {payload.get('sub')}")
except Exception as e:
    print(f"   ❌ FALHOU: {str(e)[:100]}")

# Teste 3: Sem verificação (para ver o payload)
print("\n3. Decodificando sem verificação...")
payload = jwt.decode(token, options={'verify_signature': False})
print(f"   Issuer: {payload.get('iss')}")
print(f"   User ID: {payload.get('sub')}")
print(f"   Role: {payload.get('role')}")

print("\n" + "="*70)
