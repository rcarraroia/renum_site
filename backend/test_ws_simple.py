"""
Teste WebSocket simples para debug
"""
import asyncio
import websockets
import json
from generate_test_token import generate_test_token


async def test_simple():
    token = generate_test_token()
    print(f"Token: {token[:50]}...")
    
    url = f"ws://localhost:8000/ws/test-conv?token={token}"
    print(f"Connecting to: {url}")
    
    try:
        async with websockets.connect(url) as ws:
            print("✅ Connected!")
            
            # Aguardar mensagem
            print("Waiting for message...")
            msg = await asyncio.wait_for(ws.recv(), timeout=10)
            print(f"Received: {msg}")
            
            data = json.loads(msg)
            print(f"Type: {data.get('type')}")
            print(f"Payload: {data.get('payload')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_simple())
