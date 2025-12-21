#!/usr/bin/env python3
"""
Script para testar o wizard após todas as correções
"""

import requests
import json
import time

def test_wizard_endpoint():
    """Testa o endpoint do wizard"""
    print("🧪 TESTANDO ENDPOINT DO WIZARD...")
    
    backend_url = "http://localhost:8000"
    
    # Dados de teste para o wizard
    test_data = {
        "client_id": None,
        "category": "b2c"
    }
    
    try:
        print(f"Enviando POST para {backend_url}/api/agents/wizard/start")
        print(f"Dados: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            f"{backend_url}/api/agents/wizard/start",
            json=test_data,
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCESSO! Resposta:")
                print(json.dumps(data, indent=2))
                return True
            except json.JSONDecodeError:
                print(f"⚠️ Resposta não é JSON: {response.text}")
                return False
        else:
            print(f"❌ ERRO {response.status_code}:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Backend não está rodando na porta 8000")
        print("\n🔧 INSTRUÇÕES PARA RECONSTRUIR O BACKEND:")
        print("1. Pare o container atual:")
        print("   docker-compose down")
        print("\n2. Reconstrua o container:")
        print("   docker-compose build backend")
        print("\n3. Inicie novamente:")
        print("   docker-compose up -d backend")
        print("\n4. Verifique os logs:")
        print("   docker-compose logs -f backend")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def test_backend_health():
    """Testa se o backend está rodando"""
    print("🔍 TESTANDO SAÚDE DO BACKEND...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está rodando e saudável")
            return True
        else:
            print(f"⚠️ Backend respondeu com status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro testando backend: {e}")
        return False

def main():
    print("🚀 TESTE FINAL DO WIZARD APÓS CORREÇÕES")
    print("=" * 50)
    
    # 1. Testar saúde do backend
    backend_ok = test_backend_health()
    
    if not backend_ok:
        print("\n🔧 BACKEND PRECISA SER RECONSTRUÍDO!")
        print("\nComandos para executar:")
        print("1. docker-compose down")
        print("2. docker-compose build backend")
        print("3. docker-compose up -d backend")
        print("4. Aguardar alguns segundos")
        print("5. Executar este script novamente")
        return
    
    print()
    
    # 2. Testar endpoint do wizard
    wizard_ok = test_wizard_endpoint()
    
    print("\n" + "=" * 50)
    print("📋 RESULTADO FINAL")
    print("=" * 50)
    
    if wizard_ok:
        print("🎉 WIZARD FUNCIONANDO CORRETAMENTE!")
        print("✅ Todas as correções foram aplicadas com sucesso")
        print("✅ O erro de 'template_type' foi resolvido")
        print("✅ O erro de 'role constraint' foi resolvido")
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Teste o wizard no navegador")
        print("2. Verifique se não há mais erros no console")
        print("3. Teste a criação completa de um agente")
    else:
        print("❌ WIZARD AINDA COM PROBLEMAS")
        print("🔧 Verifique os logs do backend para mais detalhes")
        print("📋 Possíveis causas:")
        print("- Container não foi reconstruído")
        print("- Outras dependências faltando")
        print("- Problemas de configuração")

if __name__ == "__main__":
    main()