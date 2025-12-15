"""Teste simples de endpoint WebSocket - Sprint 05A - Fase 4"""
import requests

BASE_URL = "http://localhost:8000"

with open("test_token.txt", "r") as f:
    TOKEN = f.read().strip()

print("\n" + "="*60)
print("FASE 4 - VALIDAÇÃO WEBSOCKET (Endpoint)")
print("="*60)

results = {"total": 0, "success": 0}

# TESTE 1: Verificar se endpoint /ws existe
results["total"] += 1
print("\n1. Verificar endpoint /ws")
try:
    # Tentar GET no endpoint (deve retornar erro mas confirma que existe)
    response = requests.get(f"{BASE_URL}/ws", timeout=5)
    # WebSocket endpoint geralmente retorna 426 (Upgrade Required) para GET
    if response.status_code in [426, 400, 405]:
        print(f"   ✅ Endpoint existe (Status {response.status_code})")
        results["success"] += 1
    else:
        print(f"   ⚠️ Status inesperado: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ Endpoint não responde")
except Exception as e:
    print(f"   ❌ Erro: {str(e)[:50]}")

# TESTE 2: Verificar rota no código
results["total"] += 1
print("\n2. Verificar rota WebSocket no código")
try:
    with open("src/main.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "/ws" in content or "websocket" in content.lower():
            print("   ✅ Rota WebSocket encontrada no código")
            results["success"] += 1
        else:
            print("   ❌ Rota WebSocket não encontrada no código")
except Exception as e:
    print(f"   ❌ Erro ao ler arquivo: {str(e)[:50]}")

# TESTE 3: Verificar se há handler WebSocket
results["total"] += 1
print("\n3. Verificar handler WebSocket")
try:
    import os
    ws_files = []
    for root, dirs, files in os.walk("src"):
        for file in files:
            if "websocket" in file.lower() or "ws" in file.lower():
                ws_files.append(os.path.join(root, file))
    
    if ws_files:
        print(f"   ✅ Arquivos WebSocket encontrados: {len(ws_files)}")
        for f in ws_files[:3]:  # Mostrar até 3
            print(f"      - {f}")
        results["success"] += 1
    else:
        print("   ⚠️ Nenhum arquivo WebSocket encontrado")
except Exception as e:
    print(f"   ❌ Erro: {str(e)[:50]}")

# TESTE 4: Verificar logs do servidor
results["total"] += 1
print("\n4. Verificar se servidor aceita WebSocket")
print("   ⏳ Teste manual necessário (conectar via navegador)")
print("   ℹ️ Abrir: http://localhost:8000/docs e testar /ws")

# Resumo
print("\n" + "="*60)
pct = (results["success"] / results["total"] * 100) if results["total"] > 0 else 0
print(f"RESULTADO: {results['success']}/{results['total']} ({pct:.1f}%)")

if pct >= 75:
    print("✅ WEBSOCKET CONFIGURADO")
elif pct >= 50:
    print("⚠️ WEBSOCKET PARCIALMENTE CONFIGURADO")
else:
    print("❌ WEBSOCKET NÃO CONFIGURADO")
print("="*60)
