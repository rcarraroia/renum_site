#!/usr/bin/env python3
"""
Script de validação das tabelas SICC no Supabase
Verifica se as tabelas existem e têm dados
"""

import os
import sys
from pathlib import Path

# Carrega .env do backend
backend_env = Path(__file__).parent.parent / 'backend' / '.env'
if backend_env.exists():
    from dotenv import load_dotenv
    load_dotenv(backend_env)

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERRO: Variáveis SUPABASE_URL e SUPABASE_KEY não configuradas")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_table(table_name: str) -> dict:
    """Verifica se tabela existe e conta registros"""
    try:
        result = supabase.table(table_name).select("*", count="exact").limit(5).execute()
        return {
            "exists": True,
            "count": result.count if hasattr(result, 'count') else len(result.data),
            "sample": result.data[:3] if result.data else []
        }
    except Exception as e:
        error_msg = str(e)
        if "does not exist" in error_msg or "relation" in error_msg:
            return {"exists": False, "count": 0, "error": "Tabela não existe"}
        return {"exists": False, "count": 0, "error": error_msg}

def main():
    print("=" * 60)
    print("🔍 VALIDAÇÃO TABELAS SICC - SUPABASE")
    print("=" * 60)
    print(f"URL: {SUPABASE_URL[:50]}...")
    print()

    tables = [
        "memory_chunks",
        "learning_logs", 
        "behavior_patterns",
        "agent_metrics",
        "sicc_settings",
        "agents"  # Para verificar se há agentes cadastrados
    ]

    results = {}
    for table in tables:
        print(f"Verificando {table}...", end=" ")
        result = check_table(table)
        results[table] = result
        
        if result["exists"]:
            print(f"✅ Existe | {result['count']} registros")
        else:
            print(f"❌ {result.get('error', 'Erro desconhecido')}")

    print()
    print("=" * 60)
    print("📊 RESUMO")
    print("=" * 60)
    
    total_tables = len(tables)
    existing = sum(1 for r in results.values() if r["exists"])
    with_data = sum(1 for r in results.values() if r["exists"] and r["count"] > 0)
    
    print(f"Tabelas existentes: {existing}/{total_tables}")
    print(f"Tabelas com dados: {with_data}/{total_tables}")
    
    # Mostrar agentes disponíveis
    if results.get("agents", {}).get("exists") and results["agents"]["count"] > 0:
        print()
        print("🤖 AGENTES DISPONÍVEIS:")
        for agent in results["agents"].get("sample", []):
            print(f"   - {agent.get('name', 'N/A')} (slug: {agent.get('slug', 'N/A')}, id: {agent.get('id', 'N/A')[:8]}...)")
    
    # Verificar se precisa criar dados de teste
    sicc_tables = ["memory_chunks", "learning_logs", "behavior_patterns", "agent_metrics"]
    empty_sicc = [t for t in sicc_tables if results.get(t, {}).get("exists") and results[t]["count"] == 0]
    
    if empty_sicc:
        print()
        print("⚠️  TABELAS SICC VAZIAS:")
        for t in empty_sicc:
            print(f"   - {t}")
        print()
        print("💡 Execute: python scripts/seed_sicc_test_data.py para criar dados de teste")
    
    print()
    return results

if __name__ == "__main__":
    main()
