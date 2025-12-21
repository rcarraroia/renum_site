#!/usr/bin/env python3
"""
Script para corrigir o constraint NOT NULL da coluna role
"""

import psycopg2
from psycopg2.extras import RealDictCursor

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
        
        # 1. Verificar constraint atual da coluna role
        print("\n=== VERIFICANDO CONSTRAINT DA COLUNA ROLE ===")
        cursor.execute("""
            SELECT column_name, is_nullable, column_default, data_type
            FROM information_schema.columns 
            WHERE table_name = 'agents' AND column_name = 'role'
        """)
        
        role_info = cursor.fetchone()
        if role_info:
            print(f"Coluna role: {role_info['data_type']}, Nullable: {role_info['is_nullable']}, Default: {role_info['column_default']}")
        
        # 2. Verificar se há registros com role NULL
        cursor.execute("SELECT COUNT(*) as count FROM agents WHERE role IS NULL")
        null_roles = cursor.fetchone()['count']
        print(f"Registros com role NULL: {null_roles}")
        
        # 3. Atualizar registros com role NULL para um valor padrão
        if null_roles > 0:
            print(f"\n🔧 ATUALIZANDO {null_roles} REGISTROS COM ROLE NULL...")
            cursor.execute("""
                UPDATE agents 
                SET role = 'assistant'::agent_role_enum
                WHERE role IS NULL
            """)
            conn.commit()
            print("✅ Registros atualizados!")
        
        # 4. Alterar coluna role para permitir NULL temporariamente
        print("\n🔧 ALTERANDO CONSTRAINT DA COLUNA ROLE...")
        try:
            cursor.execute("ALTER TABLE agents ALTER COLUMN role DROP NOT NULL")
            conn.commit()
            print("✅ Constraint NOT NULL removida da coluna role!")
        except Exception as e:
            print(f"⚠️ Erro alterando constraint: {e}")
            # Pode ser que já esteja nullable
        
        # 5. Definir valor padrão para a coluna role
        print("\n🔧 DEFININDO VALOR PADRÃO PARA COLUNA ROLE...")
        try:
            cursor.execute("ALTER TABLE agents ALTER COLUMN role SET DEFAULT 'assistant'::agent_role_enum")
            conn.commit()
            print("✅ Valor padrão definido para coluna role!")
        except Exception as e:
            print(f"⚠️ Erro definindo padrão: {e}")
        
        # 6. Verificar estrutura final
        print("\n=== ESTRUTURA FINAL DA COLUNA ROLE ===")
        cursor.execute("""
            SELECT column_name, is_nullable, column_default, data_type
            FROM information_schema.columns 
            WHERE table_name = 'agents' AND column_name = 'role'
        """)
        
        final_role_info = cursor.fetchone()
        if final_role_info:
            print(f"Coluna role: {final_role_info['data_type']}, Nullable: {final_role_info['is_nullable']}, Default: {final_role_info['column_default']}")
        
        # 7. Testar inserção
        print("\n🧪 TESTANDO INSERÇÃO SEM ROLE...")
        try:
            cursor.execute("""
                INSERT INTO agents (name, description, config) 
                VALUES ('Test Agent', 'Test Description', '{}')
                RETURNING id, name, role
            """)
            test_agent = cursor.fetchone()
            print(f"✅ Teste bem-sucedido! Agent criado: {test_agent['name']}, Role: {test_agent['role']}")
            
            # Limpar teste
            cursor.execute("DELETE FROM agents WHERE id = %s", (test_agent['id'],))
            conn.commit()
            print("✅ Registro de teste removido")
            
        except Exception as e:
            print(f"❌ Teste falhou: {e}")
            conn.rollback()
        
        cursor.close()
        conn.close()
        
        print("\n🎉 CORREÇÃO DA COLUNA ROLE CONCLUÍDA!")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    main()