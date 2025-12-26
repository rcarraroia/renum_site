#!/usr/bin/env python3
"""
Teste do Backend Local - Validação Completa
"""
import requests
import json
import sys
from datetime import datetime

def test_backend_endpoints():
    """Testa endpoints principais do backend"""
    
    base_url = "http://127.0.0.1:8000"
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {},
        "summary": {"passed": 0, "failed": 0, "total": 0}
    }
    
    # Lista de endpoints para testar
    endpoints = [
        {"path": "/", "method": "GET", "name": "Root"},
        {"path": "/health", "method": "GET", "name": "Health Check"},
        {"path": "/docs", "method": "GET", "name": "API Docs"},
        {"path": "/api/auth/status", "method": "GET", "name": "Auth Status"},
    ]
    
    print("🧪 Testando Backend Local")
    print("=" * 50)
    
    for endpoint in endpoints:
        test_name = endpoint["name"]
        url = f"{base_url}{endpoint['path']}"
        
        try:
            print(f"🔍 Testando {test_name}...")
            
            response = requests.get(url, timeout=5)
            
            # Verificar status code
            if response.status_code in [200, 201]:
                print(f"✅ {test_name}: Status {response.status_code}")
                
                # Tentar parsear JSON
                try:
                    data = response.json()
                    results["tests"][test_name] = {
                        "status": "PASS",
                        "status_code": response.status_code,
                        "response_size": len(response.text),
                        "has_json": True,
                        "data": data if len(str(data)) < 500 else "Response too large"
                    }
                except:
                    results["tests"][test_name] = {
                        "status": "PASS",
                        "status_code": response.status_code,
                        "response_size": len(response.text),
                        "has_json": False,
                        "content_type": response.headers.get("content-type", "unknown")
                    }
                
                results["summary"]["passed"] += 1
                
            else:
                print(f"❌ {test_name}: Status {response.status_code}")
                results["tests"][test_name] = {
                    "status": "FAIL",
                    "status_code": response.status_code,
                    "error": f"Unexpected status code: {response.status_code}"
                }
                results["summary"]["failed"] += 1
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {test_name}: Conexão recusada")
            results["tests"][test_name] = {
                "status": "FAIL",
                "error": "Connection refused - Backend não está rodando?"
            }
            results["summary"]["failed"] += 1
            
        except requests.exceptions.Timeout:
            print(f"❌ {test_name}: Timeout")
            results["tests"][test_name] = {
                "status": "FAIL",
                "error": "Request timeout"
            }
            results["summary"]["failed"] += 1
            
        except Exception as e:
            print(f"❌ {test_name}: Erro - {e}")
            results["tests"][test_name] = {
                "status": "FAIL",
                "error": str(e)
            }
            results["summary"]["failed"] += 1
        
        results["summary"]["total"] += 1
    
    # Resumo final
    print("\n📊 Resumo dos Testes:")
    print(f"✅ Passou: {results['summary']['passed']}")
    print(f"❌ Falhou: {results['summary']['failed']}")
    print(f"📋 Total: {results['summary']['total']}")
    
    # Salvar resultados
    with open("backend_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Resultados salvos em: backend_test_results.json")
    
    # Retornar sucesso se todos passaram
    return results["summary"]["failed"] == 0

if __name__ == "__main__":
    success = test_backend_endpoints()
    sys.exit(0 if success else 1)