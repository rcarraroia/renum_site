#!/usr/bin/env python3
"""
Script para corrigir o enum da coluna role
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
        
        # 1. Verificar enums existentes
        print("\n=== VERIFICANDO ENUMS EXISTENTES ===")
        cursor.execute("""
            SELECT typname, enumlabel 
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid 
            WHERE typname LIKE '%role%' OR typname LIKE '%agent%'
            ORDER BY typname, enumlabel
        """)
        
        enums = cursor.fetchall()
        if enums:
            current_enum = None
            for enum in enums:
                if current_enum != enum['typname']:
                    print(f"\nEnum: {enum['typname']}")
                    current_enum = enum['typname']
                print(f"  - {enum['enumlabel']}")
        else:
            print("Nenhum enum relacionado a role encontrado")
        
        # 2. Verificar tipo da coluna role
        cursor.execute("""
            SELECT 
                c.column_name,
                c.data_type,
                c.udt_name,
                c.is_nullable,
                c.column_default
            FROM information_schema.columns c
            WHERE c.table_name = 'agents' AND c.column_name = 'role'
        """)
        
        role_column = cursor.fetchone()
        if role_column:
            print(f"\n=== COLUNA ROLE ===")
            print(f"Nome: {role_column['column_name']}")
            print(f"Tipo: {role_column['data_type']}")
            print(f"UDT Name: {role_column['udt_name']}")
            print(f"Nullable: {role_column['is_nullable']}")
            print(f"Default: {role_column['column_default']}")
        
        # 3. Verificar valores atuais na coluna role
        cursor.execute("SELECT DISTINCT role FROM agents WHERE role IS NOT NULL")
        current_roles = cursor.fetchall()
        print(f"\n=== VALORES ATUAIS NA COLUNA ROLE ===")
        for role in current_roles:
            print(f"  - {role['role']}")
        
        # 4. Definir valor padrão usando o enum correto
        if role_column and role_column['udt_name']:
            enum_name = role_column['udt_name']
            print(f"\n🔧 DEFININDO VALOR PADRÃO USANDO ENUM {enum_name}...")
            
            try:
                # Primeiro, vamos ver quais valores são válidos para este enum
                cursor.execute("""
                    SELECT enumlabel 
                    FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = %s
                    ORDER BY enumlabel
                """, (enum_name,))
                
                valid_values = [row['enumlabel'] for row in cursor.fetchall()]
                print(f"Valores válidos para {enum_name}: {valid_values}")
                
                # Escolher um valor padrão apropriado
                if 'assistant' in valid_values:
                    default_value = 'assistant'
                elif 'admin' in valid_values:
                    default_value = 'admin'
                elif valid_values:
                    default_value = valid_values[0]
                else:
                    print("❌ Nenhum valor válido encontrado no enum")
                    return
                
                print(f"Usando valor padrão: {default_value}")
                
                # Definir o padrão
                cursor.execute(f"ALTER TABLE agents ALTER COLUMN role SET DEFAULT '{default_value}'::{enum_name}")
                conn.commit()
                print("✅ Valor padrão definido com sucesso!")
                
            except Exception as e:
                print(f"❌ Erro definindo padrão: {e}")
                conn.rollback()
        
        # 5. Testar inserção
        print("\n🧪 TESTANDO INSERÇÃO SEM ROLE...")
        try:
            cursor.execute("""
                INSERT INTO agents (name, description, config) 
                VALUES ('Test Agent Role', 'Test Description', '{}')
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
        
        print("\n🎉 CORREÇÃO DO ENUM ROLE CONCLUÍDA!")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    main()