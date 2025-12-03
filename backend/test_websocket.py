"""
Teste do WebSocket
"""
import asyncio
import websockets
import json

# Token do admin
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

WS_URL = f"ws://localhost:8000/ws/test-conversation-id?token={TOKEN}"

async def test_websocket():
    print("\n" + "="*70)
    print("🔌 VALIDAÇÃO DO WEBSOCKET")
    print("="*70 + "\n")
    
    results = {
        "Conecta com token": False,
        "Envia mensagem": False,
        "Recebe mensagem": False,
        "Rejeita sem token": False
    }
    
    # Teste 1: Conectar com token válido
    print("1️⃣ Teste: Conectar com token válido")
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("   ✅ Conexão estabelecida")
            results["Conecta com token"] = True
            
            # Teste 2: Enviar mensagem
            print("\n2️⃣ Teste: Enviar mensagem")
            test_message = {
                "type": "message",
                "content": "Teste de mensagem via WebSocket"
            }
            
            await websocket.send(json.dumps(test_message))
            print("   ✅ Mensagem enviada")
            results["Envia mensagem"] = True
            
            # Teste 3: Receber resposta
            print("\n3️⃣ Teste: Receber resposta")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"   ✅ Resposta recebida: {response[:100]}...")
                results["Recebe mensagem"] = True
            except asyncio.TimeoutError:
                print("   ⚠️ Timeout - servidor não respondeu em 5s")
                results["Recebe mensagem"] = False
            
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"   ❌ Erro de conexão: {e}")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:100]}")
    
    # Teste 4: Rejeitar conexão sem token
    print("\n4️⃣ Teste: Rejeitar conexão sem token")
    try:
        ws_url_no_token = "ws://localhost:8000/ws/test-conversation-id"
        async with websockets.connect(ws_url_no_token) as websocket:
            print("   ❌ Conexão aceita sem token (FALHA DE SEGURANÇA!)")
            results["Rejeita sem token"] = False
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code in [401, 403]:
            print(f"   ✅ Conexão rejeitada corretamente ({e.status_code})")
            results["Rejeita sem token"] = True
        else:
            print(f"   ⚠️ Erro inesperado: {e.status_code}")
    except Exception as e:
        print(f"   ⚠️ Erro: {str(e)[:100]}")
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO - WEBSOCKET")
    print("="*70 + "\n")
    
    for test, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {test}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n{passed}/{total} testes passaram ({passed/total*100:.0f}%)")
    
    print("\n" + "="*70)
    print("CONCLUSÃO")
    print("="*70)
    
    if passed == total:
        print("✅ WebSocket 100% funcional")
    elif passed >= 2:
        print("⚠️ WebSocket funciona mas com ressalvas")
    else:
        print("❌ WebSocket com problemas graves")

if __name__ == "__main__":
    asyncio.run(test_websocket())
