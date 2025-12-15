"""
BUG #10 - Teste de Stress para Reproduzir Crash do Servidor

Objetivo: Fazer 50 requests seguidos e identificar quando servidor trava
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_stress():
    """Faz 50 requests seguidos ao endpoint /health"""
    
    print("=" * 80)
    print("BUG #10 - TESTE DE STRESS")
    print("=" * 80)
    print(f"Início: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Endpoint: {BASE_URL}/health")
    print(f"Total de requests: 50")
    print("=" * 80)
    print()
    
    success_count = 0
    fail_count = 0
    crash_at = None
    
    for i in range(1, 51):
        try:
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                success_count += 1
                status = "✅ OK"
            else:
                fail_count += 1
                status = f"⚠️ Status {response.status_code}"
            
            print(f"Request {i:2d}/50: {status} ({elapsed:.2f}s)")
            
            # Pequeno delay entre requests
            time.sleep(0.1)
            
        except requests.exceptions.Timeout:
            fail_count += 1
            crash_at = i
            print(f"Request {i:2d}/50: ❌ TIMEOUT (servidor travou)")
            print()
            print("=" * 80)
            print(f"🚨 SERVIDOR TRAVOU NO REQUEST #{i}")
            print("=" * 80)
            break
            
        except requests.exceptions.ConnectionError:
            fail_count += 1
            crash_at = i
            print(f"Request {i:2d}/50: ❌ CONNECTION ERROR (servidor caiu)")
            print()
            print("=" * 80)
            print(f"🚨 SERVIDOR CAIU NO REQUEST #{i}")
            print("=" * 80)
            break
            
        except Exception as e:
            fail_count += 1
            print(f"Request {i:2d}/50: ❌ ERRO: {str(e)}")
    
    print()
    print("=" * 80)
    print("RESULTADO DO TESTE")
    print("=" * 80)
    print(f"✅ Sucesso: {success_count}/50")
    print(f"❌ Falhas: {fail_count}/50")
    
    if crash_at:
        print(f"🚨 Servidor travou no request #{crash_at}")
        print()
        print("PRÓXIMOS PASSOS:")
        print("1. Verificar logs do servidor no momento do crash")
        print("2. Analisar código de conexão Supabase")
        print("3. Procurar por conexões não fechadas")
    else:
        print("✅ Servidor aguentou todos os 50 requests!")
        print()
        print("CONCLUSÃO:")
        print("- BUG #10 pode não ser reproduzível com /health")
        print("- Testar com endpoints que usam Supabase")
    
    print("=" * 80)
    print(f"Fim: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    test_stress()
