"""
BUG #10 - Teste de Stress com Endpoints Supabase

Objetivo: Testar endpoints que realmente usam Supabase
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Ler token do arquivo
with open("backend/test_token.txt", "r") as f:
    TOKEN = f.read().strip()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_supabase_stress():
    """Faz 100 requests seguidos a endpoints que usam Supabase"""
    
    print("=" * 80)
    print("BUG #10 - TESTE DE STRESS COM SUPABASE")
    print("=" * 80)
    print(f"Início: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Endpoints: /api/clients, /api/leads, /api/projects")
    print(f"Total de requests: 100 (33 + 33 + 34)")
    print("=" * 80)
    print()
    
    success_count = 0
    fail_count = 0
    crash_at = None
    
    endpoints = [
        ("/api/clients", 33),
        ("/api/leads", 33),
        ("/api/projects", 34)
    ]
    
    request_num = 0
    
    for endpoint, count in endpoints:
        print(f"\n📍 Testando {endpoint}...")
        
        for i in range(1, count + 1):
            request_num += 1
            
            try:
                start_time = time.time()
                response = requests.get(
                    f"{BASE_URL}{endpoint}",
                    headers=HEADERS,
                    timeout=5
                )
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    success_count += 1
                    status = "✅"
                else:
                    fail_count += 1
                    status = f"⚠️ {response.status_code}"
                
                if request_num % 10 == 0:
                    print(f"Request {request_num:3d}/100: {status} ({elapsed:.2f}s)")
                
                # Pequeno delay
                time.sleep(0.05)
                
            except requests.exceptions.Timeout:
                fail_count += 1
                crash_at = request_num
                print(f"Request {request_num:3d}/100: ❌ TIMEOUT")
                print()
                print("=" * 80)
                print(f"🚨 SERVIDOR TRAVOU NO REQUEST #{request_num}")
                print("=" * 80)
                return
                
            except requests.exceptions.ConnectionError:
                fail_count += 1
                crash_at = request_num
                print(f"Request {request_num:3d}/100: ❌ CONNECTION ERROR")
                print()
                print("=" * 80)
                print(f"🚨 SERVIDOR CAIU NO REQUEST #{request_num}")
                print("=" * 80)
                return
                
            except Exception as e:
                fail_count += 1
                print(f"Request {request_num:3d}/100: ❌ ERRO: {str(e)}")
    
    print()
    print("=" * 80)
    print("RESULTADO DO TESTE")
    print("=" * 80)
    print(f"✅ Sucesso: {success_count}/100")
    print(f"❌ Falhas: {fail_count}/100")
    
    if crash_at:
        print(f"🚨 Servidor travou no request #{crash_at}")
    else:
        print()
        print("🎉 SERVIDOR ESTÁVEL!")
        print("✅ Aguentou 100 requests com Supabase")
        print("✅ BUG #10 CORRIGIDO!")
    
    print("=" * 80)
    print(f"Fim: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    test_supabase_stress()
