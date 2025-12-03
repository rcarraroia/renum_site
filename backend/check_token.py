"""
Verificar token
"""
import jwt
from datetime import datetime

token = open('test_token.txt').read().strip()
decoded = jwt.decode(token, options={'verify_signature': False})

exp = decoded['exp']
now = datetime.now().timestamp()

print(f"Token expira em: {datetime.fromtimestamp(exp)}")
print(f"Agora: {datetime.fromtimestamp(now)}")
print(f"Expirado: {exp < now}")
print(f"User ID: {decoded.get('sub')}")
print(f"Issuer: {decoded.get('iss')}")
