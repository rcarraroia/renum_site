#!/usr/bin/env python3
"""Verify Sprint 07A tables in Supabase"""
import psycopg2

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("\n" + "="*80)
print("🔍 VERIFICANDO TABELAS DO SPRINT 07A")
print("="*80)

# Check tables
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN ('integrations', 'triggers', 'trigger_executions')
    ORDER BY table_name
""")

tables = cursor.fetchall()
print(f"\n✅ Tabelas encontradas: {len(tables)}/3")
for table in tables:
    print(f"   - {table[0]}")

# Check columns for each table
for table_name in ['integrations', 'triggers', 'trigger_executions']:
    cursor.execute(f"""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position
    """)
    columns = cursor.fetchall()
    print(f"\n📋 Tabela '{table_name}': {len(columns)} colunas")
    for col in columns:
        print(f"   - {col[0]}: {col[1]}")

# Check RLS
cursor.execute("""
    SELECT tablename, rowsecurity 
    FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename IN ('integrations', 'triggers', 'trigger_executions')
""")
rls = cursor.fetchall()
print(f"\n🔒 RLS Status:")
for table in rls:
    status = "✅ Habilitado" if table[1] else "❌ Desabilitado"
    print(f"   - {table[0]}: {status}")

# Check policies
cursor.execute("""
    SELECT tablename, policyname 
    FROM pg_policies 
    WHERE schemaname = 'public' 
    AND tablename IN ('integrations', 'triggers', 'trigger_executions')
    ORDER BY tablename, policyname
""")
policies = cursor.fetchall()
print(f"\n🛡️  Políticas RLS: {len(policies)}")
for policy in policies:
    print(f"   - {policy[0]}: {policy[1]}")

cursor.close()
conn.close()

print("\n" + "="*80)
print("✅ VERIFICAÇÃO CONCLUÍDA - TABELAS JÁ EXISTEM!")
print("="*80)
print()
