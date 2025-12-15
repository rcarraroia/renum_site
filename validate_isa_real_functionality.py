#!/usr/bin/env python3
"""
Validação REAL da funcionalidade ISA
Testa se ISA é agente real ou apenas mock/simulação
"""
import requests
import json

# Token válido
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjgxNzczLCJpYXQiOjE3NjU1OTUzNzMsInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.Hhlrodg5Ks31ji9H7t80Z8EVEDopF0djbXV-J2wRfqE"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_isa_chat_endpoint():
    """Testa se endpoint de chat ISA funciona REALMENTE"""
    print("=== 🧪 TESTE REAL: ISA CHAT ENDPOINT ===")
    
    test_messages = [
        "Olá ISA, você está funcionando?",
        "Liste os últimos 5 leads",
        "Gere um relatório de vendas",
        "Qual é o status do sistema?",
        "Execute comando: status agentes"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📤 TESTE {i}: {message}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/isa/chat",
                headers=headers,
                json={"message": message},
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ RESPOSTA RECEBIDA:")
                print(f"   📝 Mensagem: {data.get('message', 'N/A')[:100]}...")
                print(f"   🔧 Comando executado: {data.get('command_executed', False)}")
                print(f"   📊 Dados: {len(str(data.get('result', {})))} chars")
                
                # Verificar se é resposta real ou mock
                response_text = data.get('message', '').lower()
                if any(mock_word in response_text for mock_word in ['mock', 'simulação', 'simulando', 'teste']):
                    print("   ⚠️ POSSÍVEL MOCK DETECTADO")
                else:
                    print("   ✅ RESPOSTA PARECE REAL")
                    
            elif response.status_code == 403:
                print("   🔒 ACESSO NEGADO - Precisa ser admin")
            elif response.status_code == 500:
                print("   💥 ERRO INTERNO DO SERVIDOR")
                print(f"   📄 Detalhes: {response.text[:200]}")
            else:
                print(f"   ❌ ERRO: {response.status_code}")
                print(f"   📄 Resposta: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print("   💀 SERVIDOR NÃO RESPONDE")
        except requests.exceptions.Timeout:
            print("   ⏰ TIMEOUT - Servidor muito lento")
        except Exception as e:
            print(f"   ❌ ERRO INESPERADO: {e}")

def test_isa_history_endpoint():
    """Testa se histórico ISA funciona"""
    print("\n=== 📚 TESTE REAL: ISA HISTORY ENDPOINT ===")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/isa/history",
            headers=headers,
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            commands = data.get('commands', [])
            print(f"✅ HISTÓRICO ENCONTRADO: {len(commands)} comandos")
            
            if commands:
                print("📋 ÚLTIMOS COMANDOS:")
                for cmd in commands[:3]:
                    print(f"   - {cmd.get('user_message', 'N/A')[:50]}...")
            else:
                print("📭 HISTÓRICO VAZIO (pode ser normal)")
                
        elif response.status_code == 500:
            print("💥 ERRO 500 - Problema no servidor")
            print(f"Detalhes: {response.text[:300]}")
        else:
            print(f"❌ ERRO: {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")

def analyze_isa_frontend_code():
    """Analisa código frontend da ISA para detectar mocks"""
    print("\n=== 🔍 ANÁLISE: CÓDIGO FRONTEND ISA ===")
    
    try:
        with open("src/pages/dashboard/AssistenteIsaPage.tsx", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Procurar por indicadores de mock
        mock_indicators = [
            "mock",
            "setTimeout",
            "fake",
            "simulação",
            "// Mock",
            "fallback",
            "try {",
            "catch"
        ]
        
        print("🔍 INDICADORES ENCONTRADOS:")
        for indicator in mock_indicators:
            count = content.lower().count(indicator.lower())
            if count > 0:
                print(f"   {indicator}: {count} ocorrências")
        
        # Verificar se usa service real
        if "isaService.sendMessage" in content:
            print("✅ USA SERVICE REAL: isaService.sendMessage")
        else:
            print("❌ NÃO USA SERVICE REAL")
            
        # Verificar fallbacks
        if "catch" in content and "mock" in content.lower():
            print("⚠️ TEM FALLBACK PARA MOCK")
        
    except FileNotFoundError:
        print("❌ Arquivo não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

def analyze_isa_service_code():
    """Analisa código do service ISA"""
    print("\n=== 🔍 ANÁLISE: ISA SERVICE ===")
    
    try:
        with open("src/services/isaService.ts", 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📋 ANÁLISE DO SERVICE:")
        
        if "apiClient.post" in content:
            print("✅ FAZ CHAMADAS HTTP REAIS")
        else:
            print("❌ NÃO FAZ CHAMADAS HTTP")
            
        if "catch" in content:
            print("⚠️ TEM TRATAMENTO DE ERRO")
            
        if "fallback" in content.lower() or "mock" in content.lower():
            print("⚠️ TEM FALLBACK PARA MOCK")
            
        # Contar linhas de código real vs mock
        lines = content.split('\n')
        real_lines = [l for l in lines if 'apiClient' in l or 'await' in l]
        mock_lines = [l for l in lines if 'mock' in l.lower() or 'simulação' in l.lower()]
        
        print(f"📊 LINHAS REAIS: {len(real_lines)}")
        print(f"📊 LINHAS MOCK: {len(mock_lines)}")
        
    except FileNotFoundError:
        print("❌ Arquivo não encontrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

def final_verdict():
    """Veredicto final sobre ISA"""
    print("\n" + "="*60)
    print("🎯 VEREDICTO FINAL: ISA É REAL OU MOCK?")
    print("="*60)
    
    print("\n📋 EVIDÊNCIAS COLETADAS:")
    print("1. Teste de endpoints HTTP")
    print("2. Análise de código frontend")
    print("3. Análise de service")
    print("4. Verificação de fallbacks")
    
    print("\n🔍 CONCLUSÃO:")
    print("Baseado nos testes acima, ISA é:")
    print("[ ] 100% Real - Conecta ao backend funcionando")
    print("[ ] Híbrido - Service real com fallback mock")
    print("[ ] 100% Mock - Apenas simulação visual")
    
    print("\n⚠️ IMPORTANTE:")
    print("Esta análise é baseada em TESTES REAIS, não suposições.")
    print("Se endpoints falharem = ISA não é totalmente funcional.")

if __name__ == "__main__":
    print("🔍 VALIDAÇÃO REAL: ISA É AGENTE FUNCIONAL OU MOCK?")
    print("="*60)
    print("📅 Data:", "12/12/2025")
    print("🎯 Objetivo: Descobrir se ISA realmente funciona")
    print("⚠️ Método: Testes empíricos, não suposições")
    print("="*60)
    
    try:
        test_isa_chat_endpoint()
        test_isa_history_endpoint()
        analyze_isa_frontend_code()
        analyze_isa_service_code()
        final_verdict()
        
        print("\n🎉 VALIDAÇÃO CONCLUÍDA!")
        print("📄 Resultados baseados em evidências reais")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE VALIDAÇÃO: {e}")
        print("Validação interrompida")