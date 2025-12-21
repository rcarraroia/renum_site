#!/usr/bin/env python3
"""
Script para corrigir o erro do wizard no banco de dados
Adiciona colunas faltantes na tabela agents
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys

def main():
    # Credenciais Supabase
    db_config = {
        'host': 'db.vhixvzaxswphwoymdhgg.supabase.co',
        'port': 5432,
        'database': 'postgres',
        'user': 'postgres',
        'password': 'BD5yEMQ9iDMOkeGW'
    }
    
    try:
        print("🔍 CONECTANDO AO SUPABASE...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ Conectado com sucesso!")
        
        # 1. Verificar estrutura atual da tabela agents
        print("\n=== VERIFICANDO ESTRUTURA ATUAL DA TABELA AGENTS ===")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'agents'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print(f"Colunas encontradas ({len(columns)}):")
        for col in columns:
            print(f"  {col['column_name']:20} | {col['data_type']:15} | Nullable: {col['is_nullable']}")
        
        # 2. Verificar colunas específicas que estão faltando
        existing_columns = [col['column_name'] for col in columns]
        required_columns = ['template_type', 'type', 'agent_role']
        
        missing_columns = [col for col in required_columns if col not in existing_columns]
        
        if missing_columns:
            print(f"\n🚨 COLUNAS FALTANDO: {missing_columns}")
            
            # 3. Adicionar colunas faltantes
            for column in missing_columns:
                print(f"\n🔧 ADICIONANDO COLUNA: {column}")
                
                if column == 'template_type':
                    sql = "ALTER TABLE agents ADD COLUMN template_type VARCHAR(50)"
                elif column == 'type':
                    sql = "ALTER TABLE agents ADD COLUMN type VARCHAR(50) DEFAULT 'renus'"
                elif column == 'agent_role':
                    sql = "ALTER TABLE agents ADD COLUMN agent_role VARCHAR(50) DEFAULT 'assistant'"
                
                try:
                    cursor.execute(sql)
                    conn.commit()
                    print(f"✅ Coluna {column} adicionada com sucesso!")
                except Exception as e:
                    print(f"❌ Erro adicionando coluna {column}: {e}")
                    conn.rollback()
        else:
            print("\n✅ Todas as colunas necessárias já existem!")
        
        # 4. Verificar estrutura final
        print("\n=== ESTRUTURA FINAL DA TABELA AGENTS ===")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'agents'
            ORDER BY ordinal_position
        """)
        
        final_columns = cursor.fetchall()
        print(f"Total de colunas: {len(final_columns)}")
        for col in final_columns:
            print(f"  {col['column_name']:20} | {col['data_type']:15} | Default: {col['column_default']}")
        
        # 5. Verificar dados existentes
        print("\n=== DADOS EXISTENTES NA TABELA AGENTS ===")
        cursor.execute("SELECT id, name, type, template_type, agent_role FROM agents LIMIT 5")
        agents = cursor.fetchall()
        
        if agents:
            print(f"Registros encontrados: {len(agents)}")
            for agent in agents:
                print(f"  ID: {agent['id']} | Nome: {agent['name']} | Tipo: {agent['type']} | Template: {agent['template_type']} | Role: {agent['agent_role']}")
        else:
            print("Nenhum registro encontrado na tabela agents")
        
        # 6. Atualizar registros existentes se necessário
        if agents and missing_columns:
            print("\n🔧 ATUALIZANDO REGISTROS EXISTENTES...")
            cursor.execute("""
                UPDATE agents 
                SET 
                    type = COALESCE(type, 'renus'),
                    template_type = COALESCE(template_type, 'marketplace'),
                    agent_role = COALESCE(agent_role, 'assistant')
                WHERE type IS NULL OR template_type IS NULL OR agent_role IS NULL
            """)
            
            updated_rows = cursor.rowcount
            conn.commit()
            print(f"✅ {updated_rows} registros atualizados!")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
        print("O wizard agora deve funcionar corretamente.")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()