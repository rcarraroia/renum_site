"""
Executa validação WebSocket automaticamente com token de teste
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from generate_test_token import generate_test_token
from validate_websocket import WebSocketValidator


async def main():
    """Main function"""
    print("\n🔧 Generating test token...")
    token = generate_test_token()
    print(f"✅ Token generated: {token[:50]}...\n")
    
    # Configuração
    ws_url = "ws://localhost:8000"
    
    # Criar validator
    validator = WebSocketValidator(ws_url, token)
    
    # Executar testes
    await validator.run_all_tests()
    
    # Imprimir resumo
    all_passed = validator.print_summary()
    
    # Exit code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    asyncio.run(main())
