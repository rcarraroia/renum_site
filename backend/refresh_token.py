"""
Refresh token
"""
import requests

r = requests.post('http://localhost:8000/auth/login', json={
    'email': 'rcarraro2015@gmail.com',
    'password': 'M&151173c@'
})

if r.status_code == 200:
    data = r.json()
    token = data['access_token']
    
    with open('test_token.txt', 'w') as f:
        f.write(token)
    
    print(f"✅ Token atualizado!")
    print(f"   Expira em: {data.get('expires_in', 'N/A')} segundos")
else:
    print(f"❌ Erro: {r.status_code}")
    print(f"   {r.text}")
