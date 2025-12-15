"""Teste rápido de WebSocket - Sprint 05A - Fase 4"""
import asyncio
import websockets
import json

BASE_URL = "ws://localhost:8000"

# Ler token
with open("test_token.txt", "r") as f:
    TOKEN = f.read().strip()

print("\n" + "="*60)
print("FASE 4 - VALIDAÇÃO WEBSOCKET")
print("="*60)

results = {"total": 0, "success": 0, "failed": 0}

async def test_websocket():
    """Testa conexão WebSocket"""
    global results
    
    # TESTE 1: Conectar com token válido
    results["total"] += 1
    print("\n1. Conectar WebSocket com token válido")
    try:
        uri = f"{BASE_URL}/ws?token={TOKEN}"
        async with websockets.connect(uri, timeout=5) as ws:
            print("   ✅ Conexão estabelecida")
            results["success"] += 1
            
            # TESTE 2: Enviar mensagem
            results["total"] += 1
            print("\n2. Enviar mensagem")
            try:
                message = {
                    "type": "message",
                    "content": "Olá, teste",
                    "conversation_id": "test_conv_id"
                }
                await ws.send(json.dumps(message))
                print("   ✅ Mensagem enviada")
                results["success"] += 1
                
                # TESTE 3: Receber resposta
                results["total"] += 1
                print("\n3. Receber resposta")
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=5)
                    data = json.loads(response)
                    print(f"   ✅ Resposta recebida: {data.get('type', 'unknown')}")
                    results["success"] += 1
                except asyncio.TimeoutError:
                    print("   ❌ Timeout aguardando resposta")
                    results["failed"] += 1
                except Exception as e:
                    print(f"   ❌ Erro ao receber: {str(e)[:50]}")
                    results["failed"] += 1
                    
            except Exception as e:
                print(f"   ❌ Erro ao enviar: {str(e)[:50]}")
                results["failed"] += 1
                
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"   ❌ Erro de conexão: Status {e.status_code}")
        results["failed"] += 1
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:50]}")
        results["failed"] += 1
    
    # TESTE 4: Conectar sem token (deve falhar)
    results["total"] += 1
    print("\n4. Conectar sem token (deve rejeitar)")
    try:
        uri = f"{BASE_URL}/ws"
        async with websockets.connect(uri, timeout=5) as ws:
            print("   ❌ Conexão aceita sem token (PROBLEMA!)")
            results["failed"] += 1
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code in [401, 403]:
            print(f"   ✅ Rejeitado corretamente (Status {e.status_code})")
            results["success"] += 1
        else:
            print(f"   ❌ Status inesperado: {e.status_code}")
            results["failed"] += 1
    except Exception as e:
        print(f"   ⚠️ Erro: {str(e)[:50]}")
        results["failed"] += 1

# Executar testes
try:
    asyncio.run(test_websocket())
except Exception as e:
    print(f"\n❌ ERRO FATAL: {str(e)}")

# Resumo
print("\n" + "="*60)
print("RESUMO")
print("="*60)
pct = (results["success"] / results["total"] * 100) if results["total"] > 0 else 0
print(f"Total: {results['total']} testes")
print(f"Sucesso: {results['success']} ({pct:.1f}%)")
print(f"Falhas: {results['failed']}")

if pct == 100:
    print("\n✅ WEBSOCKET 100% FUNCIONAL")
elif pct >= 70:
    print("\n⚠️ WEBSOCKET PARCIALMENTE FUNCIONAL")
else:
    print("\n❌ WEBSOCKET COM PROBLEMAS")
print("="*60)
