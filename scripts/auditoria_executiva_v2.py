#!/usr/bin/env python3
"""
AUDITORIA EXECUTIVA V2 - RENUM
Conecta diretamente ao PostgreSQL via psycopg2
"""

import psycopg2
import json
from datetime import datetime
from supabase import create_client, Client

# Configurações
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

DATABASE_URL = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"

def conectar_postgres():
    """Conecta diretamente ao PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Conectado ao PostgreSQL")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar PostgreSQL: {e}")
        return None

def conectar_supabase():
    """Conecta ao Supabase para operações simples"""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("✅ Conectado ao Supabase")
        return supabase
    except Exception as e:
        print(f"❌ Erro ao conectar Supabase: {e}")
        return None

def verificar_rls_postgres(conn):
    """Verifica RLS usando PostgreSQL direto"""
    print("\n🔒 VERIFICANDO RLS...")
    
    tabelas_criticas = [
        'agents', 'sub_agents', 'tools', 'integrations',
        'memory_chunks', 'learning_logs', 'behavior_patterns',
        'sicc_settings', 'agent_metrics', 'conversations',
        'messages', 'interviews', 'clients', 'profiles'
    ]
    
    cursor = conn.cursor()
    
    try:
        # Verificar quais tabelas existem
        cursor.execute("""
            SELECT tablename, rowsecurity 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        
        todas_tabelas = cursor.fetchall()
        rls_status = {}
        
        print("  Tabelas encontradas:")
        for tabela, rls in todas_tabelas:
            if tabela in tabelas_criticas:
                rls_status[tabela] = rls
                status = "✅ HABILITADO" if rls else "❌ DESABILITADO"
                print(f"    {tabela}: {status}")
            else:
                print(f"    {tabela}: (não crítica)")
        
        # Verificar tabelas críticas que não existem
        tabelas_existentes = [t[0] for t in todas_tabelas]
        for tabela in tabelas_criticas:
            if tabela not in tabelas_existentes:
                print(f"    ❌ {tabela}: NÃO EXISTE")
                rls_status[tabela] = None
        
        return rls_status
        
    except Exception as e:
        print(f"❌ Erro ao verificar RLS: {e}")
        return {}
    finally:
        cursor.close()

def verificar_politicas_postgres(conn):
    """Verifica políticas RLS"""
    print("\n📋 VERIFICANDO POLÍTICAS RLS...")
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT schemaname, tablename, policyname, permissive, roles, cmd
            FROM pg_policies
            WHERE schemaname = 'public'
            ORDER BY tablename, policyname;
        """)
        
        politicas_raw = cursor.fetchall()
        politicas = {}
        
        for schema, tabela, nome, permissive, roles, cmd in politicas_raw:
            if tabela not in politicas:
                politicas[tabela] = []
            politicas[tabela].append({
                'nome': nome,
                'comando': cmd,
                'roles': roles,
                'permissive': permissive
            })
        
        for tabela, pols in politicas.items():
            print(f"  {tabela}: {len(pols)} políticas")
            for pol in pols:
                print(f"    - {pol['nome']} ({pol['comando']})")
                
        return politicas
        
    except Exception as e:
        print(f"❌ Erro ao verificar políticas: {e}")
        return {}
    finally:
        cursor.close()

def verificar_client_id_postgres(conn):
    """Verifica client_id usando PostgreSQL"""
    print("\n🏢 VERIFICANDO CLIENT_ID...")
    
    cursor = conn.cursor()
    
    try:
        # Verificar estrutura da tabela agents
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'agents'
            AND column_name = 'client_id';
        """)
        
        col_info = cursor.fetchone()
        
        if col_info:
            col_name, data_type, is_nullable, default = col_info
            nullable = is_nullable == 'YES'
            print(f"  Campo client_id: {data_type}, {'nullable' if nullable else 'NOT NULL'}")
        else:
            print("  ❌ Campo client_id não existe na tabela agents!")
            return {}
        
        # Verificar agentes sem client_id
        cursor.execute("""
            SELECT id, name, client_id,
            CASE 
                WHEN client_id IS NULL THEN 'SEM_CLIENT_ID'
                ELSE 'COM_CLIENT_ID'
            END as status
            FROM agents
            ORDER BY name;
        """)
        
        agentes = cursor.fetchall()
        
        sem_client_id = []
        com_client_id = []
        
        for agent_id, name, client_id, status in agentes:
            if status == 'SEM_CLIENT_ID':
                sem_client_id.append({'id': agent_id, 'name': name})
                print(f"  ❌ {name}: SEM CLIENT_ID")
            else:
                com_client_id.append({'id': agent_id, 'name': name, 'client_id': client_id})
                print(f"  ✅ {name}: {client_id}")
        
        return {
            'nullable': nullable,
            'sem_client_id': sem_client_id,
            'com_client_id': com_client_id,
            'total_agentes': len(agentes)
        }
        
    except Exception as e:
        print(f"❌ Erro ao verificar client_id: {e}")
        return {}
    finally:
        cursor.close()

def verificar_estrutura_completa(conn):
    """Verifica estrutura completa do banco"""
    print("\n🗄️ VERIFICANDO ESTRUTURA DO BANCO...")
    
    cursor = conn.cursor()
    
    try:
        # Contar registros em todas as tabelas
        cursor.execute("""
            SELECT schemaname, tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename;
        """)
        
        tabelas = cursor.fetchall()
        contagens = {}
        
        for schema, tabela in tabelas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela};")
                count = cursor.fetchone()[0]
                contagens[tabela] = count
                print(f"  {tabela}: {count} registros")
            except Exception as e:
                contagens[tabela] = f"ERRO: {e}"
                print(f"  {tabela}: ERRO ao contar")
        
        return contagens
        
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura: {e}")
        return {}
    finally:
        cursor.close()

def main():
    """Função principal"""
    print("🔍 INICIANDO AUDITORIA EXECUTIVA V2 - RENUM")
    print("=" * 60)
    
    # Conectar ao PostgreSQL
    conn = conectar_postgres()
    if not conn:
        print("❌ Não foi possível conectar ao PostgreSQL")
        return
    
    # Conectar ao Supabase para operações simples
    supabase = conectar_supabase()
    
    # Executar verificações
    dados = {}
    
    try:
        # Verificações via PostgreSQL
        dados['rls_status'] = verificar_rls_postgres(conn)
        dados['politicas'] = verificar_politicas_postgres(conn)
        dados['client_id_info'] = verificar_client_id_postgres(conn)
        dados['estrutura_banco'] = verificar_estrutura_completa(conn)
        
        # Verificações via Supabase (mais simples)
        if supabase:
            print("\n🏠 VERIFICANDO CLIENTES...")
            
            # Cliente RENUM
            try:
                result = supabase.table('clients').select('*').eq('id', '00000000-0000-0000-0000-000000000000').execute()
                if result.data:
                    dados['cliente_renum'] = result.data[0]
                    print(f"  ✅ Cliente RENUM: {result.data[0]['company_name']}")
                else:
                    dados['cliente_renum'] = None
                    print("  ❌ Cliente RENUM não encontrado!")
            except Exception as e:
                print(f"  ❌ Erro ao verificar RENUM: {e}")
                dados['cliente_renum'] = None
            
            # Cliente Slim Quality
            try:
                result = supabase.table('clients').select('*').ilike('company_name', '%slim%').execute()
                if result.data:
                    dados['cliente_slim'] = result.data[0]
                    print(f"  ✅ Cliente Slim Quality: {result.data[0]['company_name']}")
                else:
                    dados['cliente_slim'] = None
                    print("  ❌ Cliente Slim Quality não encontrado!")
            except Exception as e:
                print(f"  ❌ Erro ao verificar Slim: {e}")
                dados['cliente_slim'] = None
            
            # Sub-agentes
            try:
                result = supabase.table('sub_agents').select('*').execute()
                dados['sub_agentes'] = result.data
                print(f"  Sub-agentes: {len(result.data)} encontrados")
                
                discovery_found = any('discovery' in sa['name'].lower() for sa in result.data)
                dados['discovery_specialist'] = discovery_found
                print(f"  Discovery Specialist: {'✅' if discovery_found else '❌'}")
                
            except Exception as e:
                print(f"  ❌ Erro ao verificar sub-agentes: {e}")
                dados['sub_agentes'] = []
                dados['discovery_specialist'] = False
            
            # Última entrevista
            try:
                result = supabase.table('interviews').select('*').order('created_at', desc=True).limit(1).execute()
                if result.data:
                    entrevista = result.data[0]
                    dados['ultima_entrevista'] = entrevista
                    print(f"  ✅ Última entrevista: {entrevista.get('contact_name', 'N/A')}")
                    
                    # Contar mensagens
                    msgs = supabase.table('interview_messages').select('*').eq('interview_id', entrevista['id']).execute()
                    dados['total_mensagens_ultima'] = len(msgs.data)
                    print(f"     Mensagens: {len(msgs.data)}")
                else:
                    dados['ultima_entrevista'] = None
                    print("  ❌ Nenhuma entrevista encontrada!")
            except Exception as e:
                print(f"  ❌ Erro ao verificar entrevistas: {e}")
                dados['ultima_entrevista'] = None
        
        # Gerar relatório final
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        resumo = {
            'timestamp': timestamp,
            'total_tabelas': len(dados.get('estrutura_banco', {})),
            'tabelas_com_rls': sum(1 for v in dados.get('rls_status', {}).values() if v),
            'tabelas_sem_rls': sum(1 for v in dados.get('rls_status', {}).values() if v is False),
            'tabelas_inexistentes': sum(1 for v in dados.get('rls_status', {}).values() if v is None),
            'total_politicas': sum(len(pols) for pols in dados.get('politicas', {}).values()),
            'agentes_sem_client_id': len(dados.get('client_id_info', {}).get('sem_client_id', [])),
            'total_agentes': dados.get('client_id_info', {}).get('total_agentes', 0),
            'cliente_renum_existe': dados.get('cliente_renum') is not None,
            'cliente_slim_existe': dados.get('cliente_slim') is not None,
            'total_sub_agentes': len(dados.get('sub_agentes', [])),
            'discovery_specialist_existe': dados.get('discovery_specialist', False),
            'historico_funciona': dados.get('ultima_entrevista') is not None
        }
        
        relatorio_completo = {
            'auditoria_executiva': {
                'data': datetime.now().isoformat(),
                'resumo': resumo,
                'detalhes': dados
            }
        }
        
        # Salvar relatório
        filename = f'auditoria_executiva_completa_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(relatorio_completo, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n✅ Relatório completo salvo: {filename}")
        
        # Resumo executivo
        print("\n" + "=" * 60)
        print("📊 RESUMO EXECUTIVO FINAL:")
        print(f"  📋 Total de tabelas: {resumo['total_tabelas']}")
        print(f"  🔒 RLS habilitado: {resumo['tabelas_com_rls']}")
        print(f"  ❌ RLS desabilitado: {resumo['tabelas_sem_rls']}")
        print(f"  ⚠️ Tabelas inexistentes: {resumo['tabelas_inexistentes']}")
        print(f"  📜 Total de políticas: {resumo['total_politicas']}")
        print(f"  🤖 Total de agentes: {resumo['total_agentes']}")
        print(f"  ⚠️ Agentes sem client_id: {resumo['agentes_sem_client_id']}")
        print(f"  🏠 Cliente RENUM: {'✅' if resumo['cliente_renum_existe'] else '❌'}")
        print(f"  🏭 Cliente Slim: {'✅' if resumo['cliente_slim_existe'] else '❌'}")
        print(f"  🔧 Sub-agentes: {resumo['total_sub_agentes']}")
        print(f"  🔍 Discovery Specialist: {'✅' if resumo['discovery_specialist_existe'] else '❌'}")
        print(f"  💬 Histórico funciona: {'✅' if resumo['historico_funciona'] else '❌'}")
        
        return relatorio_completo
        
    except Exception as e:
        print(f"❌ Erro durante auditoria: {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()