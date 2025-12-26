#!/usr/bin/env python3
"""
Script de Validação do Sistema RENUM + SICC
Valida se o sistema principal está funcionando e se o SICC pode ser integrado
"""

import requests
import json
import sys
from datetime import datetime

def test_backend_health():
    """Testa se o backend está respondendo"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend Health Check - OK")
            return True
        else:
            print(f"❌ Backend Health Check - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Health Check - Erro: {e}")
        return False

def test_backend_root():
    """Testa endpoint raiz"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Root - OK: {data.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Backend Root - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Root - Erro: {e}")
        return False

def test_cors_preflight():
    """Testa se CORS preflight está funcionando"""
    try:
        response = requests.options(
            "http://localhost:8000/api/sicc/settings/test",
            headers={
                "Origin": "http://localhost:8082",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "authorization"
            },
            timeout=5
        )
        if response.status_code == 200:
            print("✅ CORS Preflight - OK")
            return True
        else:
            print(f"❌ CORS Preflight - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS Preflight - Erro: {e}")
        return False

def test_sicc_settings_endpoint():
    """Testa endpoint SICC settings (sem autenticação)"""
    try:
        response = requests.get("http://localhost:8000/api/sicc/settings/test-agent", timeout=5)
        # Esperamos 401 (não autorizado) ou 200 (funcionando)
        if response.status_code in [200, 401, 422]:
            print(f"✅ SICC Settings Endpoint - OK (Status {response.status_code})")
            return True
        else:
            print(f"❌ SICC Settings Endpoint - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ SICC Settings Endpoint - Erro: {e}")
        return False

def test_database_connection():
    """Testa se consegue conectar ao Supabase"""
    try:
        # Importa dentro da função para não quebrar se houver erro de import
        import sys
        import os
        sys.path.append('/app')  # Para Docker
        sys.path.append('backend')  # Para local
        
        from src.utils.supabase_client import get_client
        
        supabase = get_client()
        result = supabase.table("profiles").select("id").limit(1).execute()
        
        if result.data is not None:
            print("✅ Database Connection - OK")
            return True
        else:
            print("❌ Database Connection - Sem dados")
            return False
    except Exception as e:
        print(f"❌ Database Connection - Erro: {e}")
        return False

def test_sicc_tables():
    """Testa se as tabelas SICC existem"""
    try:
        import sys
        import os
        sys.path.append('/app')  # Para Docker
        sys.path.append('backend')  # Para local
        
        from src.utils.supabase_client import get_client
        
        supabase = get_client()
        
        sicc_tables = [
            "memory_chunks",
            "learning_logs", 
            "behavior_patterns",
            "agent_snapshots",
            "sicc_settings",
            "agent_metrics"
        ]
        
        existing_tables = []
        missing_tables = []
        
        for table in sicc_tables:
            try:
                result = supabase.table(table).select("id").limit(1).execute()
                existing_tables.append(table)
            except Exception:
                missing_tables.append(table)
        
        print(f"✅ Tabelas SICC existentes: {len(existing_tables)}/6")
        if missing_tables:
            print(f"⚠️  Tabelas SICC faltando: {missing_tables}")
        
        return len(existing_tables) >= 4  # Pelo menos 4 das 6 tabelas
        
    except Exception as e:
        print(f"❌ SICC Tables Check - Erro: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🔍 VALIDAÇÃO DO SISTEMA RENUM + SICC")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Backend Root", test_backend_root),
        ("CORS Preflight", test_cors_preflight),
        ("SICC Settings Endpoint", test_sicc_settings_endpoint),
        ("Database Connection", test_database_connection),
        ("SICC Tables", test_sicc_tables),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🧪 Testando: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - Erro crítico: {e}")
            results.append((test_name, False))
        print()
    
    # Resumo
    print("=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print()
    print(f"📈 Resultado: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 SISTEMA TOTALMENTE FUNCIONAL!")
        return 0
    elif passed >= total * 0.8:
        print("⚠️  SISTEMA FUNCIONAL COM RESSALVAS")
        return 1
    else:
        print("🚨 SISTEMA COM PROBLEMAS CRÍTICOS")
        return 2

if __name__ == "__main__":
    sys.exit(main())