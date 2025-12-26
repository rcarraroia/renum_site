#!/usr/bin/env python3
"""
CORREÇÃO DE BUGS CRÍTICOS - RENUM
Corrige os problemas de segurança identificados na auditoria
"""

import psycopg2
from datetime import datetime

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def conectar_postgres():
    """Conecta ao PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conectado ao PostgreSQL")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def corrigir_rls_agents(conn):
    """Habilita RLS na tabela agents e cria políticas"""
    print("\n🔒 CORRIGINDO RLS - TABELA AGENTS...")
    
    cursor = conn.cursor()
    
    try:
        # 1. Habilitar RLS
        print("  1. Habilitando RLS...")
        cursor.execute("ALTER TABLE agents ENABLE ROW LEVEL SECURITY;")
        
        # 2. Criar política para admins
        print("  2. Criando política para admins...")
        cursor.execute("""
            CREATE POLICY "Admins have full access to agents"
                ON agents FOR ALL TO authenticated
                USING (
                    EXISTS (
                        SELECT 1 FROM profiles
                        WHERE profiles.id = auth.uid()
                        AND profiles.role = 'admin'
                    )
                );
        """)
        
        # 3. Criar política para clientes
        print("  3. Criando política para clientes...")
        cursor.execute("""
            CREATE POLICY "Clients can manage own agents"
                ON agents FOR ALL TO authenticated
                USING (
                    client_id IN (
                        SELECT id FROM clients
                        WHERE profile_id = auth.uid()
                    )
                );
        """)
        
        conn.commit()
        print("  ✅ RLS habilitado na tabela agents")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao habilitar RLS: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def corrigir_rls_sub_agents(conn):
    """Habilita RLS na tabela sub_agents e cria políticas"""
    print("\n🔒 CORRIGINDO RLS - TABELA SUB_AGENTS...")
    
    cursor = conn.cursor()
    
    try:
        # 1. Habilitar RLS
        print("  1. Habilitando RLS...")
        cursor.execute("ALTER TABLE sub_agents ENABLE ROW LEVEL SECURITY;")
        
        # 2. Criar política para admins
        print("  2. Criando política para admins...")
        cursor.execute("""
            CREATE POLICY "Admins have full access to sub_agents"
                ON sub_agents FOR ALL TO authenticated
                USING (
                    EXISTS (
                        SELECT 1 FROM profiles
                        WHERE profiles.id = auth.uid()
                        AND profiles.role = 'admin'
                    )
                );
        """)
        
        # 3. Criar política para clientes (via agent_id)
        print("  3. Criando política para clientes...")
        cursor.execute("""
            CREATE POLICY "Clients can manage own sub_agents"
                ON sub_agents FOR ALL TO authenticated
                USING (
                    agent_id IN (
                        SELECT id FROM agents
                        WHERE client_id IN (
                            SELECT id FROM clients
                            WHERE profile_id = auth.uid()
                        )
                    )
                );
        """)
        
        conn.commit()
        print("  ✅ RLS habilitado na tabela sub_agents")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao habilitar RLS: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def corrigir_client_id_obrigatorio(conn):
    """Torna client_id obrigatório na tabela agents"""
    print("\n🏢 CORRIGINDO CLIENT_ID OBRIGATÓRIO...")
    
    cursor = conn.cursor()
    
    try:
        # 1. Verificar se há agentes sem client_id
        print("  1. Verificando agentes sem client_id...")
        cursor.execute("SELECT id, name FROM agents WHERE client_id IS NULL;")
        agentes_sem_client = cursor.fetchall()
        
        if agentes_sem_client:
            print(f"  ⚠️ Encontrados {len(agentes_sem_client)} agentes sem client_id:")
            for agent_id, name in agentes_sem_client:
                print(f"    - {name} ({agent_id})")
            
            # Atribuir ao cliente RENUM (interno)
            print("  2. Atribuindo agentes órfãos ao cliente RENUM...")
            cursor.execute("""
                UPDATE agents 
                SET client_id = '00000000-0000-0000-0000-000000000000'
                WHERE client_id IS NULL;
            """)
            print(f"    ✅ {len(agentes_sem_client)} agentes atualizados")
        else:
            print("  ✅ Todos os agentes já têm client_id")
        
        # 3. Tornar campo NOT NULL
        print("  3. Tornando client_id obrigatório...")
        cursor.execute("ALTER TABLE agents ALTER COLUMN client_id SET NOT NULL;")
        
        conn.commit()
        print("  ✅ client_id agora é obrigatório")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao tornar client_id obrigatório: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def criar_cliente_slim_quality(conn):
    """Cria cliente Slim Quality para testes"""
    print("\n🏭 CRIANDO CLIENTE SLIM QUALITY...")
    
    cursor = conn.cursor()
    
    try:
        # Verificar se já existe
        cursor.execute("SELECT id FROM clients WHERE company_name ILIKE '%slim%';")
        if cursor.fetchone():
            print("  ✅ Cliente Slim Quality já existe")
            return True
        
        # Criar cliente
        print("  1. Criando cliente...")
        cursor.execute("""
            INSERT INTO clients (
                id,
                company_name,
                document,
                segment,
                status,
                created_at,
                updated_at
            ) VALUES (
                '11111111-1111-1111-1111-111111111111',
                'Slim Quality',
                '12.345.678/0001-90',
                'health',
                'active',
                NOW(),
                NOW()
            );
        """)
        
        conn.commit()
        print("  ✅ Cliente Slim Quality criado")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao criar cliente: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def criar_sub_agentes_basicos(conn):
    """Cria sub-agentes básicos"""
    print("\n🤖 CRIANDO SUB-AGENTES BÁSICOS...")
    
    cursor = conn.cursor()
    
    try:
        # Verificar se já existem
        cursor.execute("SELECT COUNT(*) FROM sub_agents;")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"  ✅ {count} sub-agentes já existem")
            return True
        
        # Buscar ID do agente RENUS
        cursor.execute("SELECT id FROM agents WHERE name = 'RENUS';")
        renus_result = cursor.fetchone()
        
        if not renus_result:
            print("  ❌ Agente RENUS não encontrado")
            return False
        
        renus_id = renus_result[0]
        
        # Criar Discovery Specialist
        print("  1. Criando Discovery Specialist...")
        cursor.execute("""
            INSERT INTO sub_agents (
                id,
                agent_id,
                name,
                slug,
                type,
                description,
                enabled,
                created_at,
                updated_at
            ) VALUES (
                '22222222-2222-2222-2222-222222222222',
                %s,
                'Discovery Specialist',
                'discovery-specialist',
                'discovery',
                'Especialista em descoberta e qualificação de leads',
                true,
                NOW(),
                NOW()
            );
        """, (renus_id,))
        
        # Criar MMN Specialist
        print("  2. Criando MMN Specialist...")
        cursor.execute("""
            INSERT INTO sub_agents (
                id,
                agent_id,
                name,
                slug,
                type,
                description,
                enabled,
                created_at,
                updated_at
            ) VALUES (
                '33333333-3333-3333-3333-333333333333',
                %s,
                'MMN Specialist',
                'mmn-specialist',
                'mmn',
                'Especialista em Marketing Multinível',
                true,
                NOW(),
                NOW()
            );
        """, (renus_id,))
        
        conn.commit()
        print("  ✅ Sub-agentes básicos criados")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao criar sub-agentes: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def validar_correcoes(conn):
    """Valida se as correções funcionaram"""
    print("\n✅ VALIDANDO CORREÇÕES...")
    
    cursor = conn.cursor()
    
    try:
        # 1. Verificar RLS em agents
        cursor.execute("SELECT rowsecurity FROM pg_tables WHERE tablename = 'agents';")
        rls_agents = cursor.fetchone()[0]
        print(f"  RLS agents: {'✅ HABILITADO' if rls_agents else '❌ DESABILITADO'}")
        
        # 2. Verificar RLS em sub_agents
        cursor.execute("SELECT rowsecurity FROM pg_tables WHERE tablename = 'sub_agents';")
        rls_sub_agents = cursor.fetchone()[0]
        print(f"  RLS sub_agents: {'✅ HABILITADO' if rls_sub_agents else '❌ DESABILITADO'}")
        
        # 3. Verificar client_id NOT NULL
        cursor.execute("""
            SELECT is_nullable FROM information_schema.columns 
            WHERE table_name = 'agents' AND column_name = 'client_id';
        """)
        nullable = cursor.fetchone()[0] == 'YES'
        print(f"  client_id nullable: {'❌ SIM' if nullable else '✅ NÃO'}")
        
        # 4. Contar sub-agentes
        cursor.execute("SELECT COUNT(*) FROM sub_agents;")
        sub_agents_count = cursor.fetchone()[0]
        print(f"  Sub-agentes: {sub_agents_count} criados")
        
        # 5. Verificar cliente Slim
        cursor.execute("SELECT COUNT(*) FROM clients WHERE company_name ILIKE '%slim%';")
        slim_count = cursor.fetchone()[0]
        print(f"  Cliente Slim: {'✅ EXISTE' if slim_count > 0 else '❌ NÃO EXISTE'}")
        
        # Resumo
        correcoes_ok = rls_agents and rls_sub_agents and not nullable and sub_agents_count > 0
        
        if correcoes_ok:
            print("\n🎉 TODAS AS CORREÇÕES APLICADAS COM SUCESSO!")
        else:
            print("\n⚠️ ALGUMAS CORREÇÕES FALHARAM - VERIFICAR LOGS")
        
        return correcoes_ok
        
    except Exception as e:
        print(f"  ❌ Erro na validação: {e}")
        return False
    finally:
        cursor.close()

def main():
    """Função principal"""
    print("🔧 INICIANDO CORREÇÃO DE BUGS CRÍTICOS")
    print("="*60)
    
    # Conectar
    conn = conectar_postgres()
    if not conn:
        return
    
    try:
        # Aplicar correções
        resultados = {}
        
        resultados['rls_agents'] = corrigir_rls_agents(conn)
        resultados['rls_sub_agents'] = corrigir_rls_sub_agents(conn)
        resultados['client_id_obrigatorio'] = corrigir_client_id_obrigatorio(conn)
        resultados['cliente_slim'] = criar_cliente_slim_quality(conn)
        resultados['sub_agentes'] = criar_sub_agentes_basicos(conn)
        
        # Validar
        validacao_ok = validar_correcoes(conn)
        
        # Relatório final
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE CORREÇÕES")
        print("="*60)
        
        total = len(resultados)
        sucesso = sum(1 for r in resultados.values() if r)
        
        print(f"Total de correções: {total}")
        print(f"Correções aplicadas: {sucesso}")
        print(f"Correções falharam: {total - sucesso}")
        print(f"Validação final: {'✅ OK' if validacao_ok else '❌ FALHOU'}")
        
        if validacao_ok:
            print("\n🎉 SISTEMA CORRIGIDO - PRONTO PARA TESTES")
        else:
            print("\n⚠️ CORREÇÕES INCOMPLETAS - VERIFICAR MANUALMENTE")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()