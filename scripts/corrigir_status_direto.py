#!/usr/bin/env python3
"""
Script para adicionar coluna status usando conexão direta PostgreSQL
MISSÃO: Correção Wizard - PASSO 1
"""

import psycopg2
from psycopg2.extras import RealDictCursor

def conectar_postgres():
    """Conecta diretamente ao PostgreSQL do Supabase"""
    connection_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    try:
        conn = psycopg2.connect(connection_string)
        print("✅ Conectado ao PostgreSQL do Supabase")
        return conn
    except Exception as e:
        print(f"❌ Erro conectando ao PostgreSQL: {e}")
        return None

def executar_sql(conn, sql, description):
    """Executa comando SQL"""
    print(f"🔧 {description}")
    print(f"   SQL: {sql}")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            print(f"✅ {description} - SUCESSO")
            return True
    except Exception as e:
        print(f"❌ {description} - ERRO: {e}")
        conn.rollback()
        return False

def verificar_estrutura(conn):
    """Verifica estrutura atual da tabela"""
    print("🔍 Verificando estrutura atual...")
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Verificar se coluna status existe
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'agents' AND column_name = 'status'
            """)
            
            result = cursor.fetchone()
            if result:
                print(f"✅ Coluna status já existe: {dict(result)}")
                return True
            else:
                print("❌ Coluna status não existe")
                return False
                
    except Exception as e:
        print(f"❌ Erro verificando estrutura: {e}")
        return False

def validar_resultado(conn):
    """Valida se a correção foi aplicada"""
    print("\n📊 VALIDANDO RESULTADO...")
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Contar agentes por status
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_agentes,
                    COUNT(CASE WHEN status IS NOT NULL THEN 1 END) as com_status,
                    COUNT(CASE WHEN status IS NULL THEN 1 END) as sem_status
                FROM agents
            """)
            
            stats = cursor.fetchone()
            print(f"📈 Estatísticas:")
            print(f"   Total de agentes: {stats['total_agentes']}")
            print(f"   Com status: {stats['com_status']}")
            print(f"   Sem status: {stats['sem_status']}")
            
            # Mostrar agentes individuais
            cursor.execute("""
                SELECT id, name, status, created_at 
                FROM agents 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            
            agentes = cursor.fetchall()
            print(f"\n📋 Agentes (últimos 5):")
            for agent in agentes:
                name = agent['name'] or 'Sem nome'
                status = agent['status'] or 'NULL'
                print(f"   ✅ {name}: status = '{status}'")
            
            # Verificar se todos têm status
            if stats['sem_status'] == 0:
                print("\n🎉 VALIDAÇÃO PASSOU - Todos os agentes têm status!")
                return True
            else:
                print(f"\n⚠️ VALIDAÇÃO FALHOU - {stats['sem_status']} agentes sem status")
                return False
                
    except Exception as e:
        print(f"❌ Erro validando: {e}")
        return False

def main():
    print("🎯 MISSÃO: Correção Wizard - PASSO 1 (Conexão Direta)")
    print("Objetivo: Adicionar coluna 'status' à tabela agents")
    print("=" * 60)
    
    # 1. Conectar
    conn = conectar_postgres()
    if not conn:
        print("❌ Falha na conexão - MISSÃO ABORTADA")
        return False
    
    try:
        # 2. Verificar se já existe
        if verificar_estrutura(conn):
            print("✅ Coluna status já existe - pulando para validação")
        else:
            print("\n🚀 EXECUTANDO CORREÇÕES...")
            
            # 3. Criar enum
            sql_enum = """
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'agent_status') THEN
                    CREATE TYPE agent_status AS ENUM ('draft', 'active', 'paused', 'inactive');
                END IF;
            END $$;
            """
            
            if not executar_sql(conn, sql_enum, "Criando enum agent_status"):
                return False
            
            # 4. Adicionar coluna
            sql_column = """
            ALTER TABLE agents ADD COLUMN IF NOT EXISTS status agent_status DEFAULT 'draft';
            """
            
            if not executar_sql(conn, sql_column, "Adicionando coluna status"):
                return False
            
            # 5. Atualizar registros existentes
            sql_update = """
            UPDATE agents SET status = 'draft' WHERE status IS NULL;
            """
            
            if not executar_sql(conn, sql_update, "Atualizando agentes existentes"):
                return False
        
        # 6. Validar resultado
        if validar_resultado(conn):
            print("\n🎉 PASSO 1 CONCLUÍDO COM SUCESSO!")
            print("✅ Coluna 'status' adicionada e configurada")
            print("✅ Todos os agentes têm status definido")
            print("\n🔄 PRÓXIMO PASSO: Testar wizard end-to-end")
            return True
        else:
            print("\n❌ VALIDAÇÃO FALHOU!")
            return False
            
    finally:
        conn.close()
        print("🔌 Conexão fechada")

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)