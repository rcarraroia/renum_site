"""
Teste simples do WebSocket
"""
import asyncio
import websockets
import json

# Token do admin
with open('test_token.txt', 'r') as f:
    TOKEN = f.read().strip()

WS_URL = f"ws://localhost:8000/ws/00000000-0000-0000-0000-000000000001?token={TOKEN}"

async def test_websocket():
    print("="*70)
    print("TESTE WEBSOCKET")
    print("="*70)
    
    print(f"\n1. Tentando conectar...")
    print(f"   URL: {WS_URL[:50]}...")
    
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("   OK: Conexao estabelecida!")
            
            # Tentar enviar mensagem
            print("\n2. Enviando mensagem...")
            test_message = {
                "type": "SEND_MESSAGE",
                "payload": {
                    "content": "Teste"
                }
            }
            
            await websocket.send(json.dumps(test_message))
            print("   OK: Mensagem enviada!")
            
            # Tentar receber resposta
            print("\n3. Aguardando resposta...")
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"   OK: Resposta recebida!")
                print(f"   {response[:100]}")
            except asyncio.TimeoutError:
                print("   TIMEOUT: Sem resposta em 5s")
            
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"   ERRO: Status {e.status_code}")
        print(f"   Mensagem: {e}")
    except Exception as e:
        print(f"   ERRO: {type(e).__name__}")
        print(f"   Mensagem: {str(e)[:200]}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    asyncio.run(test_websocket())
