#!/usr/bin/env python3
"""
Script para verificar o estado real do banco de dados Supabase
e comparar com as especificações dos sprints.
"""

import psycopg2
import json
from typing import Dict, List, Any

# Credenciais do Supabase
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def connect_to_database():
    """Conecta ao banco de dados Supabase"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def get_tables(conn):
    """Lista todas as tabelas do schema public"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return tables

def get_table_structure(conn, table_name):
    """Obtém a estrutura de uma tabela específica"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            column_name, 
            data_type, 
            is_nullable,
            column_default,
            character_maximum_length
        FROM information_schema.columns 
        WHERE table_name = %s AND table_schema = 'public'
        ORDER BY ordinal_position;
    """, (table_name,))
    
    columns = []
    for row in cursor.fetchall():
        columns.append({
            'name': row[0],
            'type': row[1],
            'nullable': row[2] == 'YES',
            'default': row[3],
            'max_length': row[4]
        })
    
    cursor.close()
    return columns

def get_rls_status(conn):
    """Verifica status do RLS para todas as tabelas"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tablename, rowsecurity 
        FROM pg_tables 
        WHERE schemaname = 'public'
        ORDER BY tablename;
    """)
    
    rls_status = {}
    for row in cursor.fetchall():
        rls_status[row[0]] = row[1]
    
    cursor.close()
    return rls_status

def get_policies(conn):
    """Lista todas as políticas RLS"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            schemaname,
            tablename,
            policyname,
            permissive,
            roles,
            cmd,
            qual
        FROM pg_policies
        WHERE schemaname = 'public'
        ORDER BY tablename, policyname;
    """)
    
    policies = {}
    for row in cursor.fetchall():
        table = row[1]
        if table not in policies:
            policies[table] = []
        
        policies[table].append({
            'name': row[2],
            'permissive': row[3],
            'roles': row[4],
            'command': row[5],
            'condition': row[6]
        })
    
    cursor.close()
    return policies

def get_indexes(conn):
    """Lista todos os índices"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            tablename,
            indexname,
            indexdef
        FROM pg_indexes
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname;
    """)
    
    indexes = {}
    for row in cursor.fetchall():
        table = row[0]
        if table not in indexes:
            indexes[table] = []
        
        indexes[table].append({
            'name': row[1],
            'definition': row[2]
        })
    
    cursor.close()
    return indexes

def get_triggers(conn):
    """Lista todos os triggers"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            event_object_table,
            trigger_name,
            event_manipulation,
            action_statement
        FROM information_schema.triggers
        WHERE trigger_schema = 'public'
        ORDER BY event_object_table, trigger_name;
    """)
    
    triggers = {}
    for row in cursor.fetchall():
        table = row[0]
        if table not in triggers:
            triggers[table] = []
        
        triggers[table].append({
            'name': row[1],
            'event': row[2],
            'action': row[3]
        })
    
    cursor.close()
    return triggers

def get_functions(conn):
    """Lista todas as functions customizadas"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            routine_name,
            routine_type,
            routine_definition
        FROM information_schema.routines
        WHERE routine_schema = 'public'
        AND routine_name NOT LIKE 'pg_%'
        ORDER BY routine_name;
    """)
    
    functions = []
    for row in cursor.fetchall():
        functions.append({
            'name': row[0],
            'type': row[1],
            'definition': row[2]
        })
    
    cursor.close()
    return functions

def count_records(conn, table_name):
    """Conta registros em uma tabela"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except Exception as e:
        return f"Erro: {e}"

def main():
    """Função principal para verificar o estado do banco"""
    print("🔍 VERIFICAÇÃO DO ESTADO DO BANCO DE DADOS SUPABASE")
    print("=" * 60)
    
    conn = connect_to_database()
    if not conn:
        print("❌ Não foi possível conectar ao banco de dados")
        return
    
    print("✅ Conectado ao Supabase com sucesso!")
    print()
    
    # Verificar tabelas
    print("📋 TABELAS EXISTENTES:")
    tables = get_tables(conn)
    for table in tables:
        count = count_records(conn, table)
        print(f"  - {table} ({count} registros)")
    print()
    
    # Verificar RLS
    print("🔒 STATUS DO RLS:")
    rls_status = get_rls_status(conn)
    for table, enabled in rls_status.items():
        status = "✅ Habilitado" if enabled else "❌ Desabilitado"
        print(f"  - {table}: {status}")
    print()
    
    # Verificar políticas
    print("📜 POLÍTICAS RLS:")
    policies = get_policies(conn)
    if policies:
        for table, table_policies in policies.items():
            print(f"  {table}:")
            for policy in table_policies:
                print(f"    - {policy['name']} ({policy['command']})")
    else:
        print("  Nenhuma política encontrada")
    print()
    
    # Verificar índices
    print("📊 ÍNDICES:")
    indexes = get_indexes(conn)
    for table, table_indexes in indexes.items():
        if table_indexes:
            print(f"  {table}:")
            for index in table_indexes:
                if not index['name'].endswith('_pkey'):  # Pular primary keys
                    print(f"    - {index['name']}")
    print()
    
    # Verificar triggers
    print("⚡ TRIGGERS:")
    triggers = get_triggers(conn)
    if triggers:
        for table, table_triggers in triggers.items():
            print(f"  {table}:")
            for trigger in table_triggers:
                print(f"    - {trigger['name']} ({trigger['event']})")
    else:
        print("  Nenhum trigger encontrado")
    print()
    
    # Verificar functions
    print("🔧 FUNCTIONS:")
    functions = get_functions(conn)
    if functions:
        for func in functions:
            print(f"  - {func['name']} ({func['type']})")
    else:
        print("  Nenhuma function encontrada")
    print()
    
    # Estrutura detalhada das tabelas principais
    expected_tables = [
        'profiles', 'clients', 'leads', 'interviews', 'interview_messages',
        'projects', 'conversations', 'messages', 'renus_config', 'tools',
        'sub_agents', 'isa_commands'
    ]
    
    print("🏗️ ESTRUTURA DAS TABELAS PRINCIPAIS:")
    for table in expected_tables:
        if table in tables:
            print(f"\n  📋 {table.upper()}:")
            structure = get_table_structure(conn, table)
            for col in structure:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f" DEFAULT {col['default']}" if col['default'] else ""
                print(f"    - {col['name']}: {col['type']} {nullable}{default}")
        else:
            print(f"\n  ❌ {table.upper()}: NÃO EXISTE")
    
    conn.close()
    print("\n✅ Verificação concluída!")

if __name__ == "__main__":
    main()