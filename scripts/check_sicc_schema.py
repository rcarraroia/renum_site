#!/usr/bin/env python3
"""
Script para verificar a estrutura real das tabelas SICC
"""

import os
import sys
from pathlib import Path

backend_env = Path(__file__).parent.parent / 'backend' / '.env'
if backend_env.exists():
    from dotenv import load_dotenv
    load_dotenv(backend_env)

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_ANON_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_table_columns(table_name: str):
    """Busca um registro para ver as colunas"""
    try:
        result = supabase.table(table_name).select("*").limit(1).execute()
        if result.data:
            return list(result.data[0].keys())
        # Se não tem dados, tenta inserir e ver o erro
        return "Tabela vazia - não é possível determinar colunas"
    except Exception as e:
        return f"Erro: {e}"

def main():
    print("=" * 60)
    print("🔍 ESTRUTURA DAS TABELAS SICC")
    print("=" * 60)
    
    tables = ["memory_chunks", "learning_logs", "behavior_patterns", "agent_metrics", "sicc_settings"]
    
    for table in tables:
        print(f"\n📋 {table}:")
        cols = get_table_columns(table)
        if isinstance(cols, list):
            for col in cols:
                print(f"   - {col}")
        else:
            print(f"   {cols}")

if __name__ == "__main__":
    main()
