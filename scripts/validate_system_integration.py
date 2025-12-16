#!/usr/bin/env python3
"""
Script de Validação Completa do Sistema RENUM
Testa integração Frontend-Backend seguindo as regras de checkpoint-validation.md
"""
import requests
import time
from datetime import datetime

def print_header(title):
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_result(test_name, success, details=""):
    status = "✅ PASSOU" if success else "❌ FALHOU"
    print(f"{status} - {test_name}")
    if details:
        print(f"   {details}")

def test_backend_health():
    """Testa se o backend está rodando e saudável"""
    print_header("VALIDAÇÃO DO BACKEND")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        success = response.status_code == 200
        details = f"Status: {response.status_code}, Response: {response.json()}"
        print_result("Backend Health Check", success, details)
        return success
    except Exception as e:
        print_result("Backend Health Check", False, f"Erro: {e}")
        return False

def test_frontend_availability():
    """Testa se o frontend está disponível"""
    print_header("VALIDAÇÃO DO FRONTEND")
    
    try:
        response = requests.get("http://localhost:8083", timeout=5)
        success = response.status_code == 200 and "html" in response.text.lower()
        details = f"Status: {response.status_code}, Content-Type: {response.headers.get('content-type', 'N/A')}"
        print_result("Frontend Disponibilidade", success, details)
        return success
    except Exception as e:
        print_result("Frontend Disponibilidade", False, f"Erro: {e}")
        return False

def test_cors_configuration():
    """Testa se CORS está configurado corretamente"""
    print_header("VALIDAÇÃO DO CORS")
    
    # Token válido para testes
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjczMjM5LCJpYXQiOjE3NjU1ODY4MzksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.HgEqRYi7ijWwaqj1Vkt-ofRIB5dWY4bRyDNGiKMpDsk"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:8083"  # Simula requisição do frontend
    }
    
    try:
        # Teste real: requisição GET com headers CORS
        response = requests.get(
            "http://localhost:8000/api/dashboard/stats", 
            headers=headers, 
            timeout=5
        )
        cors_headers = response.headers
        
        # Verifica headers CORS necessários
        has_allow_origin = "access-control-allow-origin" in cors_headers
        has_credentials = "access-control-allow-credentials" in cors_headers
        correct_origin = cors_headers.get("access-control-allow-origin") == "http://localhost:8083"
        
        success = response.status_code == 200 and has_allow_origin and correct_origin
        details = f"Status: {response.status_code}, Origin: {cors_headers.get('access-control-allow-origin', 'N/A')}, Credentials: {cors_headers.get('access-control-allow-credentials', 'N/A')}"
        print_result("CORS Headers", success, details)
        
        return success
    except Exception as e:
        print_result("CORS Headers", False, f"Erro: {e}")
        return False

def test_api_endpoints():
    """Testa endpoints críticos da API"""
    print_header("VALIDAÇÃO DOS ENDPOINTS DA API")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjczMjM5LCJpYXQiOjE3NjU1ODY4MzksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.HgEqRYi7ijWwaqj1Vkt-ofRIB5dWY4bRyDNGiKMpDsk"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:8083"
    }
    
    endpoints = [
        ("/api/dashboard/stats", "Dashboard Stats"),
        ("/api/clients", "Clientes"),
        ("/api/leads", "Leads"),
        ("/api/projects", "Projetos"),
        ("/api/conversations", "Conversas")
    ]
    
    results = []
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", headers=headers, timeout=5)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if endpoint == "/api/dashboard/stats":
                    details = f"Clientes: {data.get('total_clients', 'N/A')}, Leads: {data.get('total_leads', 'N/A')}"
                else:
                    items_count = len(data.get('items', [])) if isinstance(data, dict) else len(data) if isinstance(data, list) else 'N/A'
                    details = f"Total de itens: {items_count}"
            else:
                details = f"Status: {response.status_code}, Erro: {response.text[:100]}"
            
            print_result(f"Endpoint {name}", success, details)
            results.append(success)
            
        except Exception as e:
            print_result(f"Endpoint {name}", False, f"Erro: {e}")
            results.append(False)
    
    return all(results)

def test_data_persistence():
    """Testa se os dados estão sendo persistidos no Supabase"""
    print_header("VALIDAÇÃO DA PERSISTÊNCIA DE DADOS")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzY1NjczMjM5LCJpYXQiOjE3NjU1ODY4MzksInN1YiI6Ijg3NmJlMzMxLTk1NTMtNGU5YS05ZjI5LTYzY2ZhNzExZTA1NiIsImVtYWlsIjoicmNhcnJhcm8yMDE1QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJyY2FycmFybzIwMTVAZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6IkFkbWluIiwibGFzdF9uYW1lIjoiUmVudW0ifX0.HgEqRYi7ijWwaqj1Vkt-ofRIB5dWY4bRyDNGiKMpDsk"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:8083"
    }
    
    try:
        # Testa se há dados reais (não mockados)
        response = requests.get("http://localhost:8000/api/dashboard/stats", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verifica se há dados reais
            has_clients = data.get('total_clients', 0) > 0
            has_leads = data.get('total_leads', 0) > 0
            has_conversations = data.get('total_conversations', 0) > 0
            
            success = has_clients or has_leads or has_conversations
            details = f"Clientes: {data.get('total_clients', 0)}, Leads: {data.get('total_leads', 0)}, Conversas: {data.get('total_conversations', 0)}"
            
            print_result("Dados Reais no Banco", success, details)
            
            if not success:
                print("   ⚠️  ATENÇÃO: Sistema pode estar usando dados mockados!")
            
            return success
        else:
            print_result("Dados Reais no Banco", False, f"Erro ao acessar dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print_result("Dados Reais no Banco", False, f"Erro: {e}")
        return False

def generate_validation_report(results):
    """Gera relatório final de validação"""
    print_header("RELATÓRIO FINAL DE VALIDAÇÃO")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"📊 RESUMO EXECUTIVO:")
    print(f"   Total de testes: {total_tests}")
    print(f"   Testes aprovados: {passed_tests}")
    print(f"   Taxa de sucesso: {success_rate:.1f}%")
    print(f"   Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    print(f"\n📋 DETALHAMENTO:")
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {status} - {test_name}")
    
    print(f"\n🎯 CONCLUSÃO:")
    if success_rate >= 90:
        print("   ✅ SISTEMA APROVADO - Pronto para uso")
    elif success_rate >= 70:
        print("   ⚠️  SISTEMA PARCIAL - Necessita correções menores")
    else:
        print("   ❌ SISTEMA REPROVADO - Necessita correções críticas")
    
    print(f"\n📝 PRÓXIMOS PASSOS:")
    if success_rate < 100:
        print("   1. Corrigir testes que falharam")
        print("   2. Executar validação novamente")
        print("   3. Só então marcar como completo")
    else:
        print("   1. Sistema validado e aprovado")
        print("   2. Pode ser marcado como completo")

def main():
    """Executa validação completa do sistema"""
    print("🚀 INICIANDO VALIDAÇÃO COMPLETA DO SISTEMA RENUM")
    print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Executa todos os testes
    results = {
        "Backend Health": test_backend_health(),
        "Frontend Disponível": test_frontend_availability(),
        "CORS Configurado": test_cors_configuration(),
        "Endpoints da API": test_api_endpoints(),
        "Dados Persistidos": test_data_persistence()
    }
    
    # Gera relatório final
    generate_validation_report(results)
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)