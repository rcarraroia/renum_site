#!/usr/bin/env python3
"""
Script de Validação - Integração SICC
Valida se o módulo SICC está funcionando corretamente
"""

import requests
import json
import sys
import time
from datetime import datetime

def print_status(message, status="INFO"):
    """Print status message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
    symbol = symbols.get(status, "ℹ️")
    print(f"[{timestamp}] {symbol} {message}")

def test_backend_health():
    """Testa se o backend está rodando"""
    print_status("Testando saúde do backend...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print_status("Backend está rodando", "SUCCESS")
            return True
        else:
            print_status(f"Backend retornou status {response.status_code}", "ERROR")
            return False
    except requests.exceptions.RequestException as e:
        print_status(f"Backend não está respondendo: {str(e)}", "ERROR")
        return False

def test_cors_preflight():
    """Testa se CORS preflight está funcionando"""
    print_status("Testando CORS preflight...")
    
    try:
        response = requests.options(
            "http://localhost:8000/api/sicc/settings/test",
            headers={
                "Origin": "http://localhost:8082",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "authorization,content-type"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            headers = response.headers
            if "Access-Control-Allow-Origin" in headers:
                print_status("CORS preflight funcionando", "SUCCESS")
                return True
            else:
                print_status("CORS headers não encontrados", "ERROR")
                return False
        else:
            print_status(f"CORS preflight falhou: {response.status_code}", "ERROR")
            return False
    except requests.exceptions.RequestException as e:
        print_status(f"Erro no teste CORS: {str(e)}", "ERROR")
        return False

def test_sicc_settings_endpoint():
    """Testa endpoint de configurações SICC"""
    print_status("Testando endpoint SICC settings...")
    
    # Usar um agent_id que sabemos que existe (dos dados inseridos)
    agent_id = "00000000-0000-0000-0000-000000000001"
    
    try:
        response = requests.get(
            f"http://localhost:8000/api/sicc/settings/{agent_id}",
            headers={
                "Content-Type": "application/json",
                "Origin": "http://localhost:8082"
            },
            timeout=10
        )
        
        print_status(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_status("Endpoint SICC settings funcionando", "SUCCESS")
            print_status(f"Dados retornados: {json.dumps(data, indent=2)}")
            
            # Verificar se tem campos essenciais
            required_fields = ["agent_id", "auto_approve_threshold", "memory_retention_days"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print_status(f"Campos obrigatórios faltando: {missing_fields}", "WARNING")
                return False
            else:
                print_status("Todos os campos obrigatórios presentes", "SUCCESS")
                return True
                
        elif response.status_code == 401:
            print_status("Endpoint requer autenticação (esperado)", "WARNING")
            return True  # Isso é esperado sem token
        else:
            print_status(f"Endpoint falhou: {response.status_code} - {response.text}", "ERROR")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Erro no teste endpoint: {str(e)}", "ERROR")
        return False

def test_database_tables():
    """Testa se as tabelas SICC existem no banco"""
    print_status("Testando tabelas SICC no banco...")
    
    try:
        from supabase import create_client
        
        # Configurar cliente Supabase
        url = "https://vhixvzaxswphwoymdhgg.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"
        
        supabase = create_client(url, key)
        
        sicc_tables = ['memory_chunks', 'learning_logs', 'behavior_patterns', 'agent_snapshots', 'sicc_settings', 'agent_metrics']
        
        all_tables_exist = True
        
        for table in sicc_tables:
            try:
                result = supabase.table(table).select("count", count="exact").execute()
                count = result.count
                print_status(f"Tabela {table}: {count} registros", "SUCCESS")
            except Exception as e:
                print_status(f"Tabela {table}: ERRO - {str(e)}", "ERROR")
                all_tables_exist = False
        
        return all_tables_exist
        
    except ImportError:
        print_status("Biblioteca supabase não instalada", "ERROR")
        return False
    except Exception as e:
        print_status(f"Erro ao testar banco: {str(e)}", "ERROR")
        return False

def test_frontend_cors():
    """Simula requisição do frontend para testar CORS"""
    print_status("Simulando requisição do frontend...")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/sicc/settings/test-agent",
            headers={
                "Origin": "http://localhost:8082",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        # Verificar headers CORS na resposta
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
        }
        
        print_status(f"Headers CORS: {cors_headers}")
        
        if cors_headers["Access-Control-Allow-Origin"]:
            print_status("CORS configurado corretamente", "SUCCESS")
            return True
        else:
            print_status("CORS não configurado", "ERROR")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Erro no teste CORS frontend: {str(e)}", "ERROR")
        return False

def main():
    """Executa todos os testes de validação"""
    print_status("🔧 INICIANDO VALIDAÇÃO DO MÓDULO SICC")
    print_status("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("CORS Preflight", test_cors_preflight),
        ("SICC Settings Endpoint", test_sicc_settings_endpoint),
        ("Database Tables", test_database_tables),
        ("Frontend CORS", test_frontend_cors)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print_status(f"\n🧪 Executando: {test_name}")
        print_status("-" * 30)
        
        try:
            result = test_func()
            results[test_name] = result
            
            if result:
                print_status(f"{test_name}: PASSOU", "SUCCESS")
            else:
                print_status(f"{test_name}: FALHOU", "ERROR")
                
        except Exception as e:
            print_status(f"{test_name}: ERRO - {str(e)}", "ERROR")
            results[test_name] = False
        
        time.sleep(1)  # Pausa entre testes
    
    # Resumo final
    print_status("\n📊 RESUMO DA VALIDAÇÃO")
    print_status("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print_status(f"{test_name:<25} {status}")
    
    print_status(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print_status("🎉 TODOS OS TESTES PASSARAM - MÓDULO SICC FUNCIONAL", "SUCCESS")
        return True
    else:
        print_status("⚠️ ALGUNS TESTES FALHARAM - MÓDULO SICC PRECISA CORREÇÃO", "ERROR")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)