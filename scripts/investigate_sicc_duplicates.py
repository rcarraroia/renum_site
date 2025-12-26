#!/usr/bin/env python3
"""
Investigação de Duplicatas de Tabelas SICC
Objetivo: Determinar se tabelas com prefixo agent_ são obsoletas ou têm propósito específico
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

# Conexão Supabase
DB_CONFIG = {
    "host": "db.vhixvzaxswphwoymdhgg.supabase.co",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "BD5yEMQ9iDMOkeGW"
}

# Pares de duplicatas a investigar
DUPLICATE_PAIRS = [
    ("memory_chunks", "agent_memory_chunks"),
    ("learning_logs", "agent_learning_logs"),
    ("behavior_patterns", "agent_behavior_patterns"),
    ("agent_snapshots", "agent_knowledge_snapshots"),
    ("agent_metrics", "agent_performance_metrics"),
    ("sicc_settings", "agent_dna"),
]

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_table_columns(cursor, table_name):
    """Retorna colunas de uma tabela"""
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = %s AND table_schema = 'public'
        ORDER BY ordinal_position
    """, (table_name,))
    return cursor.fetchall()

def get_table_indexes(cursor, table_name):
    """Retorna índices de uma tabela"""
    cursor.execute("""
        SELECT indexname, indexdef
        FROM pg_indexes 
        WHERE tablename = %s AND schemaname = 'public'
        ORDER BY indexname
    """, (table_name,))
    return cursor.fetchall()

def get_table_constraints(cursor, table_name):
    """Retorna constraints de uma tabela"""
    cursor.execute("""
        SELECT conname, contype, pg_get_constraintdef(c.oid)
        FROM pg_constraint c
        JOIN pg_class t ON c.conrelid = t.oid
        JOIN pg_namespace n ON t.relnamespace = n.oid
        WHERE t.relname = %s AND n.nspname = 'public'
        ORDER BY contype, conname
    """, (table_name,))
    return cursor.fetchall()

def get_rls_policies(cursor, table_name):
    """Retorna políticas RLS de uma tabela"""
    cursor.execute("""
        SELECT policyname, cmd, qual, with_check
        FROM pg_policies 
        WHERE tablename = %s AND schemaname = 'public'
        ORDER BY policyname
    """, (table_name,))
    return cursor.fetchall()

def get_foreign_keys_to_table(cursor, table_name):
    """Retorna FKs que apontam para esta tabela"""
    cursor.execute("""
        SELECT 
            tc.table_name as source_table,
            tc.constraint_name,
            kcu.column_name as source_column,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
        AND ccu.table_name = %s
    """, (table_name,))
    return cursor.fetchall()

def get_row_count(cursor, table_name):
    """Retorna contagem de registros"""
    try:
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        return cursor.fetchone()[0]
    except:
        return "ERRO"

def table_exists(cursor, table_name):
    """Verifica se tabela existe"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = %s
        )
    """, (table_name,))
    return cursor.fetchone()[0]

def compare_columns(cols1, cols2):
    """Compara duas listas de colunas"""
    set1 = {c[0] for c in cols1}
    set2 = {c[0] for c in cols2}
    
    only_in_1 = set1 - set2
    only_in_2 = set2 - set1
    common = set1 & set2
    
    # Verificar tipos diferentes
    dict1 = {c[0]: c[1] for c in cols1}
    dict2 = {c[0]: c[1] for c in cols2}
    
    type_diffs = []
    for col in common:
        if dict1.get(col) != dict2.get(col):
            type_diffs.append((col, dict1.get(col), dict2.get(col)))
    
    return {
        "only_in_first": list(only_in_1),
        "only_in_second": list(only_in_2),
        "common": list(common),
        "type_differences": type_diffs,
        "identical": len(only_in_1) == 0 and len(only_in_2) == 0 and len(type_diffs) == 0
    }

def main():
    print("=" * 80)
    print("INVESTIGAÇÃO DE DUPLICATAS DE TABELAS SICC")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    results = {}
    
    for table1, table2 in DUPLICATE_PAIRS:
        print(f"\n{'='*80}")
        print(f"COMPARANDO: {table1} vs {table2}")
        print("="*80)
        
        exists1 = table_exists(cursor, table1)
        exists2 = table_exists(cursor, table2)
        
        print(f"\n📊 EXISTÊNCIA:")
        print(f"  - {table1}: {'✅ EXISTE' if exists1 else '❌ NÃO EXISTE'}")
        print(f"  - {table2}: {'✅ EXISTE' if exists2 else '❌ NÃO EXISTE'}")
        
        if not exists1 and not exists2:
            print("  ⚠️ NENHUMA DAS TABELAS EXISTE!")
            results[f"{table1}_vs_{table2}"] = {"status": "BOTH_MISSING"}
            continue
        
        if not exists1:
            print(f"  ⚠️ {table1} NÃO EXISTE - apenas {table2} existe")
            results[f"{table1}_vs_{table2}"] = {"status": "FIRST_MISSING", "existing": table2}
            continue
            
        if not exists2:
            print(f"  ⚠️ {table2} NÃO EXISTE - apenas {table1} existe")
            results[f"{table1}_vs_{table2}"] = {"status": "SECOND_MISSING", "existing": table1}
            continue
        
        # Ambas existem - comparar
        cols1 = get_table_columns(cursor, table1)
        cols2 = get_table_columns(cursor, table2)
        
        print(f"\n📋 COLUNAS:")
        print(f"  - {table1}: {len(cols1)} colunas")
        for c in cols1:
            print(f"      • {c[0]} ({c[1]})")
        print(f"  - {table2}: {len(cols2)} colunas")
        for c in cols2:
            print(f"      • {c[0]} ({c[1]})")
        
        col_comparison = compare_columns(cols1, cols2)
        print(f"\n  📊 COMPARAÇÃO DE COLUNAS:")
        print(f"      Idênticas: {'✅ SIM' if col_comparison['identical'] else '❌ NÃO'}")
        if col_comparison['only_in_first']:
            print(f"      Apenas em {table1}: {col_comparison['only_in_first']}")
        if col_comparison['only_in_second']:
            print(f"      Apenas em {table2}: {col_comparison['only_in_second']}")
        if col_comparison['type_differences']:
            print(f"      Tipos diferentes: {col_comparison['type_differences']}")
        
        # Índices
        idx1 = get_table_indexes(cursor, table1)
        idx2 = get_table_indexes(cursor, table2)
        print(f"\n📑 ÍNDICES:")
        print(f"  - {table1}: {len(idx1)} índices")
        print(f"  - {table2}: {len(idx2)} índices")
        
        # Constraints
        cons1 = get_table_constraints(cursor, table1)
        cons2 = get_table_constraints(cursor, table2)
        print(f"\n🔗 CONSTRAINTS:")
        print(f"  - {table1}: {len(cons1)} constraints")
        print(f"  - {table2}: {len(cons2)} constraints")
        
        # RLS
        rls1 = get_rls_policies(cursor, table1)
        rls2 = get_rls_policies(cursor, table2)
        print(f"\n🔒 RLS POLICIES:")
        print(f"  - {table1}: {len(rls1)} policies")
        print(f"  - {table2}: {len(rls2)} policies")
        
        # FKs dependentes
        fk1 = get_foreign_keys_to_table(cursor, table1)
        fk2 = get_foreign_keys_to_table(cursor, table2)
        print(f"\n🔀 FKs DEPENDENTES (outras tabelas apontando para):")
        print(f"  - {table1}: {len(fk1)} FKs")
        if fk1:
            for fk in fk1:
                print(f"      • {fk[0]}.{fk[2]} -> {fk[3]}.{fk[4]}")
        print(f"  - {table2}: {len(fk2)} FKs")
        if fk2:
            for fk in fk2:
                print(f"      • {fk[0]}.{fk[2]} -> {fk[3]}.{fk[4]}")
        
        # Contagem de registros
        count1 = get_row_count(cursor, table1)
        count2 = get_row_count(cursor, table2)
        print(f"\n📊 REGISTROS:")
        print(f"  - {table1}: {count1} registros")
        print(f"  - {table2}: {count2} registros")
        
        # Decisão
        print(f"\n🎯 ANÁLISE:")
        
        can_delete_first = (
            col_comparison['identical'] and 
            len(fk1) == 0 and 
            (count1 == 0 or count1 == "ERRO")
        )
        can_delete_second = (
            col_comparison['identical'] and 
            len(fk2) == 0 and 
            (count2 == 0 or count2 == "ERRO")
        )
        
        if col_comparison['identical']:
            print("  ✅ Estrutura IDÊNTICA")
        else:
            print("  ❌ Estrutura DIFERENTE - NÃO são duplicatas simples")
        
        if len(fk1) == 0 and len(fk2) == 0:
            print("  ✅ Nenhuma FK dependente em ambas")
        else:
            print(f"  ⚠️ FKs dependentes: {table1}={len(fk1)}, {table2}={len(fk2)}")
        
        if count1 == 0 and count2 == 0:
            print("  ✅ Ambas vazias")
        elif count1 == 0:
            print(f"  ⚠️ {table1} vazia, {table2} tem {count2} registros")
        elif count2 == 0:
            print(f"  ⚠️ {table2} vazia, {table1} tem {count1} registros")
        else:
            print(f"  ⚠️ Ambas têm dados: {table1}={count1}, {table2}={count2}")
        
        results[f"{table1}_vs_{table2}"] = {
            "table1": table1,
            "table2": table2,
            "exists1": exists1,
            "exists2": exists2,
            "columns_identical": col_comparison['identical'],
            "col_comparison": col_comparison,
            "indexes1": len(idx1),
            "indexes2": len(idx2),
            "constraints1": len(cons1),
            "constraints2": len(cons2),
            "rls1": len(rls1),
            "rls2": len(rls2),
            "fk_dependents1": len(fk1),
            "fk_dependents2": len(fk2),
            "count1": count1,
            "count2": count2,
            "can_delete_first": can_delete_first,
            "can_delete_second": can_delete_second
        }
    
    cursor.close()
    conn.close()
    
    # Resumo final
    print("\n" + "="*80)
    print("RESUMO FINAL - RECOMENDAÇÕES")
    print("="*80)
    
    for key, data in results.items():
        if data.get("status") in ["BOTH_MISSING", "FIRST_MISSING", "SECOND_MISSING"]:
            print(f"\n{key}: {data.get('status')}")
            continue
            
        t1, t2 = data["table1"], data["table2"]
        print(f"\n{t1} vs {t2}:")
        
        if data["columns_identical"]:
            if data["count1"] == 0 and data["count2"] > 0:
                print(f"  🗑️ RECOMENDAÇÃO: DELETAR {t1} (vazia, {t2} tem dados)")
            elif data["count2"] == 0 and data["count1"] > 0:
                print(f"  🗑️ RECOMENDAÇÃO: DELETAR {t2} (vazia, {t1} tem dados)")
            elif data["count1"] == 0 and data["count2"] == 0:
                print(f"  🗑️ RECOMENDAÇÃO: DELETAR UMA (ambas vazias) - preferir manter a sem prefixo agent_")
            else:
                print(f"  ⚠️ INVESTIGAR: Ambas têm dados - verificar qual é usada no código")
        else:
            print(f"  ⚠️ MANTER AMBAS: Estruturas diferentes - não são duplicatas simples")
    
    # Salvar JSON
    with open("sicc_duplicates_analysis.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n📄 Resultados salvos em: sicc_duplicates_analysis.json")

if __name__ == "__main__":
    main()
