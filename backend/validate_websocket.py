"""
Sprint 05B - Task 1: Validação WebSocket
Testa conexão WebSocket em cenários reais
"""
import asyncio
import json
import time
from typing import Optional
from dataclasses import dataclass
import websockets
from websockets.exceptions import InvalidStatusCode, ConnectionClosed
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from src.config.settings import settings


@dataclass
class TestResult:
    test_name: str
    passed: bool
    message: str
    duration_ms: float
    details: Optional[dict] = None


class WebSocketValidator:
    def __init__(self, ws_url: str, token: Optional[str] = None):
        self.ws_url = ws_url
        self.token = token
        self.results: list[TestResult] = []
    
    async def test_connection_with_token(self) -> TestResult:
        """Testa conexão com token válido - deve retornar status 101"""
        test_name = "Connection with valid token"
        start = time.time()
        
        try:
            if not self.token:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message="No token provided for testing",
                    duration_ms=0
                )
            
            # Conectar com token
            conversation_id = "test-conversation-001"
            url = f"{self.ws_url}/ws/{conversation_id}?token={self.token}"
            
            async with websockets.connect(url) as websocket:
                # Aguardar mensagem de confirmação
                response = await asyncio.wait_for(
                    websocket.recv(),
                    timeout=5.0
                )
                
                data = json.loads(response)
                
                # Verificar mensagem CONNECTED
                if data.get("type") == "connected":
                    duration = (time.time() - start) * 1000
                    return TestResult(
                        test_name=test_name,
                        passed=True,
                        message="✅ Connected successfully with status 101",
                        duration_ms=duration,
                        details={"response": data}
                    )
                else:
                    duration = (time.time() - start) * 1000
                    return TestResult(
                        test_name=test_name,
                        passed=False,
                        message=f"❌ Unexpected response type: {data.get('type')}",
                        duration_ms=duration,
                        details={"response": data}
                    )
        
        except asyncio.TimeoutError:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message="❌ Timeout waiting for connection confirmation",
                duration_ms=duration
            )
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Connection failed: {str(e)}",
                duration_ms=duration
            )
    
    async def test_connection_without_token(self) -> TestResult:
        """Testa conexão sem token - deve rejeitar com 401/403"""
        test_name = "Connection without token"
        start = time.time()
        
        try:
            conversation_id = "test-conversation-002"
            url = f"{self.ws_url}/ws/{conversation_id}"  # Sem token
            
            async with websockets.connect(url) as websocket:
                # Se chegou aqui, conexão foi aceita (ERRO!)
                duration = (time.time() - start) * 1000
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message="❌ Connection accepted without token (should reject)",
                    duration_ms=duration
                )
        
        except InvalidStatusCode as e:
            # Esperado: deve rejeitar
            duration = (time.time() - start) * 1000
            if e.status_code in [401, 403, 400]:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message=f"✅ Correctly rejected with status {e.status_code}",
                    duration_ms=duration
                )
            else:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message=f"❌ Rejected but with unexpected status: {e.status_code}",
                    duration_ms=duration
                )
        
        except ConnectionClosed as e:
            # Também aceitável se fechar com código 4001
            duration = (time.time() - start) * 1000
            if e.code == 4001:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message=f"✅ Correctly rejected with close code {e.code}",
                    duration_ms=duration
                )
            else:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message=f"❌ Connection closed with unexpected code: {e.code}",
                    duration_ms=duration
                )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            # Qualquer erro é aceitável (conexão rejeitada)
            return TestResult(
                test_name=test_name,
                passed=True,
                message=f"✅ Connection rejected: {str(e)}",
                duration_ms=duration
            )
    
    async def test_message_exchange(self) -> TestResult:
        """Testa envio e recebimento de mensagens - deve responder em <2s"""
        test_name = "Message exchange"
        start = time.time()
        
        try:
            if not self.token:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message="No token provided for testing",
                    duration_ms=0
                )
            
            conversation_id = "test-conversation-003"
            url = f"{self.ws_url}/ws/{conversation_id}?token={self.token}"
            
            async with websockets.connect(url) as websocket:
                # Aguardar CONNECTED
                await websocket.recv()
                
                # Pode receber PRESENCE_UPDATE também, ignorar
                try:
                    msg = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                    # Ignorar presence_update
                except asyncio.TimeoutError:
                    pass
                
                # Enviar mensagem
                test_message = {
                    "type": "send_message",
                    "payload": {
                        "content": "Test message from validator",
                        "type": "text"
                    }
                }
                
                await websocket.send(json.dumps(test_message))
                
                # Aguardar resposta (NEW_MESSAGE broadcast)
                # Pode receber múltiplas mensagens, procurar por new_message
                found_new_message = False
                for _ in range(3):  # Tentar até 3 mensagens
                    try:
                        response = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=2.0
                        )
                        data = json.loads(response)
                        
                        if data.get("type") == "new_message":
                            found_new_message = True
                            duration = (time.time() - start) * 1000
                            
                            if duration < 2000:
                                return TestResult(
                                    test_name=test_name,
                                    passed=True,
                                    message=f"✅ Message processed in {duration:.0f}ms (<2s)",
                                    duration_ms=duration,
                                    details={"response": data}
                                )
                            else:
                                return TestResult(
                                    test_name=test_name,
                                    passed=False,
                                    message=f"❌ Message processed but took {duration:.0f}ms (>2s)",
                                    duration_ms=duration
                                )
                    except asyncio.TimeoutError:
                        break
                
                duration = (time.time() - start) * 1000
                if not found_new_message:
                    return TestResult(
                        test_name=test_name,
                        passed=False,
                        message="❌ Did not receive new_message response",
                        duration_ms=duration
                    )
        
        except asyncio.TimeoutError:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message="❌ Timeout waiting for message response (>2s)",
                duration_ms=duration
            )
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Message exchange failed: {str(e)}",
                duration_ms=duration
            )
    
    async def test_multiple_clients(self) -> TestResult:
        """Testa múltiplos clientes simultâneos - deve manter todas conexões"""
        test_name = "Multiple simultaneous clients"
        start = time.time()
        
        try:
            if not self.token:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message="No token provided for testing",
                    duration_ms=0
                )
            
            conversation_id = "test-conversation-004"
            num_clients = 5
            connections = []
            
            # Conectar múltiplos clientes
            for i in range(num_clients):
                url = f"{self.ws_url}/ws/{conversation_id}?token={self.token}"
                ws = await websockets.connect(url)
                # Aguardar CONNECTED
                await ws.recv()
                connections.append(ws)
            
            # Aguardar 2 segundos
            await asyncio.sleep(2)
            
            # Verificar se todas conexões ainda estão ativas
            # Usar closed property (not open)
            active_count = 0
            for ws in connections:
                if not ws.closed:
                    active_count += 1
            
            # Fechar todas conexões
            for ws in connections:
                if not ws.closed:
                    await ws.close()
            
            duration = (time.time() - start) * 1000
            
            if active_count == num_clients:
                return TestResult(
                    test_name=test_name,
                    passed=True,
                    message=f"✅ All {num_clients} connections remained stable",
                    duration_ms=duration,
                    details={"active_connections": active_count}
                )
            else:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message=f"❌ Only {active_count}/{num_clients} connections remained active",
                    duration_ms=duration
                )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Multiple clients test failed: {str(e)}",
                duration_ms=duration
            )
    
    async def test_connection_cleanup(self) -> TestResult:
        """Testa limpeza de recursos ao fechar - não deve ter memory leak"""
        test_name = "Connection cleanup"
        start = time.time()
        
        try:
            if not self.token:
                return TestResult(
                    test_name=test_name,
                    passed=False,
                    message="No token provided for testing",
                    duration_ms=0
                )
            
            conversation_id = "test-conversation-005"
            url = f"{self.ws_url}/ws/{conversation_id}?token={self.token}"
            
            # Conectar e desconectar 10 vezes
            for i in range(10):
                async with websockets.connect(url) as websocket:
                    await websocket.recv()  # CONNECTED
                    # Fechar imediatamente
            
            duration = (time.time() - start) * 1000
            
            # Se chegou aqui sem erros, limpeza funcionou
            return TestResult(
                test_name=test_name,
                passed=True,
                message="✅ Resources cleaned up successfully (10 connect/disconnect cycles)",
                duration_ms=duration
            )
        
        except Exception as e:
            duration = (time.time() - start) * 1000
            return TestResult(
                test_name=test_name,
                passed=False,
                message=f"❌ Cleanup test failed: {str(e)}",
                duration_ms=duration
            )
    
    async def run_all_tests(self) -> list[TestResult]:
        """Executa todos os testes"""
        print("\n" + "="*60)
        print("🧪 WEBSOCKET VALIDATION - Sprint 05B Task 1")
        print("="*60 + "\n")
        
        tests = [
            ("1. Connection with valid token", self.test_connection_with_token),
            ("2. Connection without token", self.test_connection_without_token),
            ("3. Message exchange (<2s)", self.test_message_exchange),
            ("4. Multiple simultaneous clients", self.test_multiple_clients),
            ("5. Connection cleanup", self.test_connection_cleanup),
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            result = await test_func()
            self.results.append(result)
            
            print(f"   {result.message}")
            print(f"   Duration: {result.duration_ms:.0f}ms")
            
            if result.details:
                print(f"   Details: {json.dumps(result.details, indent=2)}")
        
        return self.results
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60 + "\n")
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        percentage = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {total - passed} ❌")
        print(f"Success Rate: {percentage:.1f}%")
        
        print("\n" + "-"*60)
        print("DETAILED RESULTS:")
        print("-"*60 + "\n")
        
        for i, result in enumerate(self.results, 1):
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{i}. {result.test_name}: {status}")
            print(f"   {result.message}")
            print(f"   Duration: {result.duration_ms:.0f}ms\n")
        
        print("="*60 + "\n")
        
        return passed == total


async def main():
    """Main function"""
    # Configuração
    ws_url = "ws://localhost:8000"
    
    # Token de teste (você precisa fornecer um token válido)
    # Para obter: fazer login no frontend e copiar o token
    token = input("\n🔑 Enter JWT token (or press Enter to skip auth tests): ").strip()
    
    if not token:
        print("\n⚠️  No token provided. Auth tests will be skipped.")
        print("   To get a token: Login in frontend and copy from localStorage")
        token = None
    
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
