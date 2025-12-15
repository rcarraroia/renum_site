#!/usr/bin/env python3
"""
Execute Migration 010: Migrate Sub-Agents to Agents
Sprint 09 - Fase B
"""
import psycopg2

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def main():
    print("=" * 80)
    print("🚀 EXECUTANDO MIGRATION 010: MIGRATE SUB-AGENTS TO AGENTS")
    print("=" * 80)
    
    print("\n📡 Conectando ao Supabase via PostgreSQL...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conectado!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    migration_file = "backend/migrations/010_migrate_subagents_to_agents.sql"
    
    print(f"\n📄 Executando: {migration_file}")
    
    try:
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        
        # Capturar notices do PostgreSQL
        for notice in conn.notices:
            print(notice.strip())
        
        cursor.close()
        
        print(f"\n✅ Migration executada com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro ao executar migration: {e}")
        conn.rollback()
        conn.close()
        return
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ MIGRATION 010 CONCLUÍDA")
    print("=" * 80)
    print("\n📋 Próximos passos:")
    print("   1. Fase C: Atualizar Wizard para salvar em agents")
    print("   2. Fase D: Criar routes de sub-agents por agent")

if __name__ == "__main__":
    main()
