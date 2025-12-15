"""
Teste do Health Check - Validar tempo de resposta
"""
import requests
import time

BASE_URL = "http://localhost:8000"

print("="*70)
print("TESTE HEALTH CHECK")
print("="*70)

times = []
for i in range(5):
    start = time.time()
    r = requests.get(f"{BASE_URL}/health", timeout=3)
    elapsed = time.time() - start
    times.append(elapsed)
    print(f"Teste {i+1}: {elapsed:.3f}s - Status {r.status_code}")

avg = sum(times) / len(times)
print(f"\nMédia: {avg:.3f}s")
print(f"Critério: < 2.0s")

if avg < 2.0:
    print("✅ PASSOU - Health check responde em < 2s")
else:
    print(f"❌ FALHOU - Health check demora {avg:.3f}s (acima de 2s)")

print("="*70)
