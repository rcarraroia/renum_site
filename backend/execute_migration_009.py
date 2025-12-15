#!/usr/bin/env python3
"""
Execute Migration 009: Create Agents Table
Sprint 09 - Fase A
Connects to Supabase and runs SQL migration directly via psycopg2
"""
import os
import psycopg2

# Connection string
DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def execute_sql_file(conn, filepath: str):
    """Execute SQL file"""
    print(f"\n📄 Executando: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        
        print(f"✅ Migration executada com sucesso!")
        return True
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar migration: {e}")
        conn.rollback()
        return False

def main():
    print("=" * 80)
    print("🚀 EXECUTANDO MIGRATION 009: CREATE AGENTS TABLE")
    print("=" * 80)
    
    # Conectar ao PostgreSQL
    print("\n📡 Conectando ao Supabase via PostgreSQL...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conectado!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # Migration a executar
    migration_file = "backend/migrations/009_create_agents_table.sql"
    
    print("\n" + "=" * 80)
    print("📋 EXECUTANDO MIGRATION")
    print("=" * 80)
    
    success = execute_sql_file(conn, migration_file)
    
    # Verificar se tabela foi criada
    if success:
        print("\n🔍 Verificando se tabela agents foi criada...")
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'agents'")
            count = cursor.fetchone()[0]
            cursor.close()
            
            if count > 0:
                print("✅ Tabela 'agents' criada com sucesso!")
                
                # Verificar RLS
                cursor = conn.cursor()
                cursor.execute("SELECT rowsecurity FROM pg_tables WHERE tablename = 'agents'")
                rls_enabled = cursor.fetchone()[0]
                cursor.close()
                
                if rls_enabled:
                    print("✅ RLS habilitado em 'agents'")
                else:
                    print("⚠️  RLS NÃO habilitado em 'agents'")
                
                # Contar políticas
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM pg_policies WHERE tablename = 'agents'")
                policies_count = cursor.fetchone()[0]
                cursor.close()
                
                print(f"✅ {policies_count} políticas RLS criadas")
                
            else:
                print("❌ Tabela 'agents' NÃO foi criada")
                
        except Exception as e:
            print(f"⚠️  Erro ao verificar: {e}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ MIGRATION 009 EXECUTADA COM SUCESSO")
        print("=" * 80)
        print("\n🎉 Tabela agents criada!")
        print("\n📋 Próximos passos:")
        print("   1. Fase B: Migrar dados de sub_agents para agents")
        print("   2. Fase C: Atualizar Wizard para salvar em agents")
    else:
        print("❌ MIGRATION 009 FALHOU")
        print("=" * 80)
        print("\n⚠️  Verifique os erros acima.")

if __name__ == "__main__":
    main()
