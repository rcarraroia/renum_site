#!/usr/bin/env python3
"""
FASE 1: Mapear Sistema de Configuração de Agentes
Objetivo: Entender estrutura completa de configuração
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

def analisar_renus():
    """Analisa configuração completa do RENUS"""
    print("🔍 1.1 ANALISANDO RENUS (Agente Existente)")
    print("=" * 50)
    
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    conn = psycopg2.connect(conn_string)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT id, name, config, role, description, sicc_enabled, 
                   is_active, created_at, updated_at, slug, is_public
            FROM agents 
            WHERE name = 'RENUS'
        """)
        
        renus = cursor.fetchone()
        if renus:
            print("=== RENUS CONFIG COMPLETO ===")
            print(f"ID: {renus['id']}")
            print(f"Name: {renus['name']}")
            print(f"Role: {renus['role']}")
            print(f"Description: {renus['description']}")
            print(f"SICC Enabled: {renus['sicc_enabled']}")
            print(f"Is Active: {renus['is_active']}")
            print(f"Is Public: {renus['is_public']}")
            print(f"Slug: {renus['slug']}")
            print(f"Created: {renus['created_at']}")
            print(f"Updated: {renus['updated_at']}")
            print()
            print("CONFIG JSONB:")
            print(json.dumps(renus['config'], indent=2, ensure_ascii=False))
            
            return renus
        else:
            print("❌ RENUS não encontrado")
            return None
    
    conn.close()

def analisar_todos_agentes():
    """Analisa todos os agentes para entender padrões"""
    print("\n🔍 1.2 ANALISANDO TODOS OS AGENTES")
    print("=" * 50)
    
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    conn = psycopg2.connect(conn_string)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT id, name, role, config, sicc_enabled, is_active
            FROM agents 
            ORDER BY name
        """)
        
        agentes = cursor.fetchall()
        print(f"Total de agentes: {len(agentes)}")
        print()
        
        for agent in agentes:
            print(f"📋 {agent['name']}")
            print(f"   Role: {agent['role']}")
            print(f"   SICC: {agent['sicc_enabled']}")
            print(f"   Active: {agent['is_active']}")
            
            # Analisar estrutura do config
            config = agent['config']
            if config:
                print(f"   Config keys: {list(config.keys())}")
                
                # Verificar se tem system_prompt
                if 'system_prompt' in config:
                    prompt_len = len(config['system_prompt']) if config['system_prompt'] else 0
                    print(f"   System prompt: {prompt_len} chars")
                
                # Verificar se tem model
                if 'model' in config:
                    print(f"   Model: {config['model']}")
                
                # Verificar se tem tools
                if 'tools' in config:
                    print(f"   Tools: {config['tools']}")
                
                # Verificar se tem sub_agents
                if 'sub_agents' in config:
                    print(f"   Sub-agents: {config['sub_agents']}")
            else:
                print("   Config: vazio")
            print()
        
        return agentes
    
    conn.close()

def verificar_tabela_sub_agents():
    """Verifica se tabela sub_agents existe e sua estrutura"""
    print("\n🔍 1.3 VERIFICANDO TABELA SUB_AGENTS")
    print("=" * 50)
    
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    conn = psycopg2.connect(conn_string)
    
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        # Verificar se tabela existe
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'sub_agents'
        """)
        
        if cursor.fetchone():
            print("✅ Tabela 'sub_agents' existe")
            
            # Ver estrutura
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'sub_agents'
                ORDER BY ordinal_position
            """)
            
            colunas = cursor.fetchall()
            print("\n📋 Estrutura da tabela:")
            for col in colunas:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
                print(f"   {col['column_name']}: {col['data_type']} {nullable}{default}")
            
            # Ver dados
            cursor.execute("SELECT COUNT(*) as count FROM sub_agents")
            count = cursor.fetchone()['count']
            print(f"\n📊 Total de sub-agentes: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM sub_agents LIMIT 5")
                sub_agents = cursor.fetchall()
                print("\n📋 Primeiros 5 sub-agentes:")
                for sa in sub_agents:
                    print(f"   - {sa.get('name', 'N/A')}: {sa.get('type', 'N/A')}")
        else:
            print("❌ Tabela 'sub_agents' NÃO existe")
    
    conn.close()

def verificar_tabelas_relacionadas():
    """Verifica outras tabelas relacionadas a agentes"""
    print("\n🔍 1.4 VERIFICANDO TABELAS RELACIONADAS")
    print("=" * 50)
    
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    conn = psycopg2.connect(conn_string)
    
    tabelas_interesse = [
        'tools',
        'knowledge',
        'documents',
        'integrations',
        'triggers',
        'guardrails',
        'webhooks'
    ]
    
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        for tabela in tabelas_interesse:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = %s
            """, (tabela,))
            
            if cursor.fetchone():
                cursor.execute(f"SELECT COUNT(*) as count FROM {tabela}")
                count = cursor.fetchone()['count']
                print(f"✅ {tabela}: {count} registros")
            else:
                print(f"❌ {tabela}: não existe")
    
    conn.close()

def main():
    print("🔍 MISSÃO: Mapear Sistema de Configuração de Agentes")
    print("📋 FASE 1: MAPEAR ESTRUTURA DE CONFIGURAÇÃO")
    print("=" * 60)
    
    # 1.1 Analisar RENUS
    renus = analisar_renus()
    
    # 1.2 Analisar todos os agentes
    agentes = analisar_todos_agentes()
    
    # 1.3 Verificar sub_agents
    verificar_tabela_sub_agents()
    
    # 1.4 Verificar tabelas relacionadas
    verificar_tabelas_relacionadas()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO FASE 1")
    print("=" * 60)
    print(f"✅ RENUS analisado: {'Sim' if renus else 'Não'}")
    print(f"✅ Total de agentes: {len(agentes) if agentes else 0}")
    print("✅ Estrutura de configuração mapeada")
    print("✅ Tabelas relacionadas verificadas")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)