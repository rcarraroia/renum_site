#!/usr/bin/env python3
"""
AUDITORIA EXECUTIVA - RENUM
Verifica estado real do sistema no Supabase
"""

import os
import sys
import json
from datetime import datetime
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def conectar_supabase():
    """Conecta ao Supabase"""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("✅ Conectado ao Supabase")
        return supabase
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def verificar_rls(supabase):
    """Verifica RLS em todas as tabelas"""
    print("\n🔒 VERIFICANDO RLS...")
    
    tabelas_criticas = [
        'agents', 'sub_agents', 'tools', 'integrations',
        'memory_chunks', 'learning_logs', 'behavior_patterns',
        'sicc_settings', 'agent_metrics', 'conversations',
        'messages', 'interviews', 'clients', 'profiles'
    ]
    
    # Query para verificar RLS
    query = """
    SELECT tablename, rowsecurity 
    FROM pg_tables 
    WHERE schemaname = 'public'
    AND tablename = ANY(%s)
    ORDER BY tablename;
    """
    
    try:
        result = supabase.rpc('exec_sql', {
            'query': query,
            'params': [tabelas_criticas]
        }).execute()
        
        rls_status = {}
        for row in result.data:
            rls_status[row['tablename']] = row['rowsecurity']
            status = "✅ HABILITADO" if row['rowsecurity'] else "❌ DESABILITADO"
            print(f"  {row['tablename']}: {status}")
            
        return rls_status
    except Exception as e:
        print(f"❌ Erro ao verificar RLS: {e}")
        return {}

def verificar_politicas(supabase):
    """Verifica políticas RLS"""
    print("\n📋 VERIFICANDO POLÍTICAS RLS...")
    
    query = """
    SELECT schemaname, tablename, policyname, permissive, roles, cmd
    FROM pg_policies
    WHERE schemaname = 'public'
    ORDER BY tablename, policyname;
    """
    
    try:
        result = supabase.rpc('exec_sql', {'query': query}).execute()
        
        politicas = {}
        for row in result.data:
            tabela = row['tablename']
            if tabela not in politicas:
                politicas[tabela] = []
            politicas[tabela].append({
                'nome': row['policyname'],
                'comando': row['cmd'],
                'roles': row['roles']
            })
        
        for tabela, pols in politicas.items():
            print(f"  {tabela}: {len(pols)} políticas")
            for pol in pols:
                print(f"    - {pol['nome']} ({pol['comando']})")
                
        return politicas
    except Exception as e:
        print(f"❌ Erro ao verificar políticas: {e}")
        return {}

def verificar_client_id(supabase):
    """Verifica client_id obrigatório"""
    print("\n🏢 VERIFICANDO CLIENT_ID...")
    
    # Verificar estrutura da tabela agents
    try:
        query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'agents'
        AND column_name = 'client_id';
        """
        
        result = supabase.rpc('exec_sql', {'query': query}).execute()
        
        if result.data:
            col_info = result.data[0]
            nullable = col_info['is_nullable'] == 'YES'
            print(f"  Campo client_id: {'nullable' if nullable else 'NOT NULL'}")
        else:
            print("  ❌ Campo client_id não existe!")
            return {}
        
        # Verificar agentes sem client_id
        agents_result = supabase.table('agents').select('id, name, client_id').execute()
        
        sem_client_id = []
        com_client_id = []
        
        for agent in agents_result.data:
            if agent['client_id'] is None:
                sem_client_id.append(agent)
                print(f"  ❌ {agent['name']}: SEM CLIENT_ID")
            else:
                com_client_id.append(agent)
                print(f"  ✅ {agent['name']}: {agent['client_id']}")
        
        return {
            'nullable': nullable,
            'sem_client_id': sem_client_id,
            'com_client_id': com_client_id
        }
        
    except Exception as e:
        print(f"❌ Erro ao verificar client_id: {e}")
        return {}

def verificar_cliente_renum(supabase):
    """Verifica cliente RENUM (Interno)"""
    print("\n🏠 VERIFICANDO CLIENTE RENUM...")
    
    try:
        # Procurar cliente RENUM
        result = supabase.table('clients').select('*').ilike('company_name', '%renum%').execute()
        
        if result.data:
            cliente = result.data[0]
            print(f"  ✅ Cliente RENUM encontrado: {cliente['id']}")
            print(f"     Nome: {cliente['company_name']}")
            print(f"     Status: {cliente['status']}")
            return cliente
        else:
            # Verificar UUID específico
            uuid_renum = '00000000-0000-0000-0000-000000000000'
            result2 = supabase.table('clients').select('*').eq('id', uuid_renum).execute()
            
            if result2.data:
                cliente = result2.data[0]
                print(f"  ✅ Cliente com UUID padrão: {cliente['company_name']}")
                return cliente
            else:
                print("  ❌ Cliente RENUM não encontrado!")
                return None
                
    except Exception as e:
        print(f"❌ Erro ao verificar cliente RENUM: {e}")
        return None

def verificar_cliente_slim(supabase):
    """Verifica cliente Slim Quality"""
    print("\n🏭 VERIFICANDO CLIENTE SLIM QUALITY...")
    
    try:
        result = supabase.table('clients').select('*').ilike('company_name', '%slim%').execute()
        
        if result.data:
            cliente = result.data[0]
            print(f"  ✅ Slim Quality encontrado: {cliente['id']}")
            print(f"     CNPJ: {cliente.get('cnpj', 'N/A')}")
            print(f"     Plano: {cliente.get('plan', 'N/A')}")
            
            # Verificar agente vinculado
            agents_result = supabase.table('agents').select('*').eq('client_id', cliente['id']).execute()
            
            if agents_result.data:
                print(f"  ✅ Agente vinculado: {agents_result.data[0]['name']}")
            else:
                print("  ⚠️ Nenhum agente vinculado")
                
            return cliente
        else:
            print("  ❌ Cliente Slim Quality não encontrado!")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao verificar Slim Quality: {e}")
        return None

def verificar_sub_agentes(supabase):
    """Verifica sub-agentes"""
    print("\n🤖 VERIFICANDO SUB-AGENTES...")
    
    try:
        # Verificar tabela sub_agents
        result = supabase.table('sub_agents').select('*').execute()
        
        print(f"  Total de sub-agentes: {len(result.data)}")
        
        discovery_found = False
        for sub_agent in result.data:
            print(f"  - {sub_agent['name']} ({sub_agent['type']})")
            if 'discovery' in sub_agent['name'].lower():
                discovery_found = True
                print(f"    ✅ Discovery Specialist encontrado!")
        
        if not discovery_found:
            print("  ❌ Discovery Specialist não encontrado!")
            
        return {
            'total': len(result.data),
            'discovery_found': discovery_found,
            'sub_agents': result.data
        }
        
    except Exception as e:
        print(f"❌ Erro ao verificar sub-agentes: {e}")
        return {}

def verificar_historico_conversas(supabase):
    """Verifica se histórico de conversas funciona"""
    print("\n💬 VERIFICANDO HISTÓRICO DE CONVERSAS...")
    
    try:
        # Verificar última entrevista
        result = supabase.table('interviews').select('*').order('created_at', desc=True).limit(1).execute()
        
        if result.data:
            entrevista = result.data[0]
            print(f"  ✅ Última entrevista: {entrevista['id']}")
            print(f"     Nome: {entrevista.get('contact_name', 'N/A')}")
            print(f"     País: {entrevista.get('country', 'N/A')}")
            print(f"     Status: {entrevista['status']}")
            
            # Verificar mensagens da entrevista
            msgs_result = supabase.table('interview_messages').select('*').eq('interview_id', entrevista['id']).order('created_at').execute()
            
            print(f"     Mensagens: {len(msgs_result.data)}")
            
            # Verificar se campos são extraídos
            campos_extraidos = {
                'contact_name': entrevista.get('contact_name') is not None,
                'country': entrevista.get('country') is not None,
                'company': entrevista.get('company') is not None
            }
            
            return {
                'ultima_entrevista': entrevista,
                'total_mensagens': len(msgs_result.data),
                'campos_extraidos': campos_extraidos
            }
        else:
            print("  ❌ Nenhuma entrevista encontrada!")
            return {}
            
    except Exception as e:
        print(f"❌ Erro ao verificar histórico: {e}")
        return {}

def gerar_relatorio(dados):
    """Gera relatório final"""
    print("\n📊 GERANDO RELATÓRIO...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    relatorio = {
        'timestamp': timestamp,
        'data_auditoria': datetime.now().isoformat(),
        'resultados': dados,
        'resumo': {
            'rls_habilitado': sum(1 for v in dados.get('rls_status', {}).values() if v),
            'total_tabelas': len(dados.get('rls_status', {})),
            'agentes_sem_client_id': len(dados.get('client_id_info', {}).get('sem_client_id', [])),
            'cliente_renum_existe': dados.get('cliente_renum') is not None,
            'cliente_slim_existe': dados.get('cliente_slim') is not None,
            'sub_agentes_total': dados.get('sub_agentes_info', {}).get('total', 0),
            'discovery_specialist': dados.get('sub_agentes_info', {}).get('discovery_found', False),
            'ultima_entrevista_existe': bool(dados.get('historico_conversas', {}).get('ultima_entrevista'))
        }
    }
    
    # Salvar JSON
    with open(f'auditoria_executiva_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ Relatório salvo: auditoria_executiva_{timestamp}.json")
    
    return relatorio

def main():
    """Função principal"""
    print("🔍 INICIANDO AUDITORIA EXECUTIVA - RENUM")
    print("=" * 50)
    
    # Conectar ao Supabase
    supabase = conectar_supabase()
    if not supabase:
        sys.exit(1)
    
    # Executar verificações
    dados = {}
    
    try:
        dados['rls_status'] = verificar_rls(supabase)
        dados['politicas'] = verificar_politicas(supabase)
        dados['client_id_info'] = verificar_client_id(supabase)
        dados['cliente_renum'] = verificar_cliente_renum(supabase)
        dados['cliente_slim'] = verificar_cliente_slim(supabase)
        dados['sub_agentes_info'] = verificar_sub_agentes(supabase)
        dados['historico_conversas'] = verificar_historico_conversas(supabase)
        
        # Gerar relatório
        relatorio = gerar_relatorio(dados)
        
        print("\n" + "=" * 50)
        print("📋 RESUMO EXECUTIVO:")
        print(f"  RLS Habilitado: {relatorio['resumo']['rls_habilitado']}/{relatorio['resumo']['total_tabelas']} tabelas")
        print(f"  Agentes sem client_id: {relatorio['resumo']['agentes_sem_client_id']}")
        print(f"  Cliente RENUM: {'✅' if relatorio['resumo']['cliente_renum_existe'] else '❌'}")
        print(f"  Cliente Slim: {'✅' if relatorio['resumo']['cliente_slim_existe'] else '❌'}")
        print(f"  Sub-agentes: {relatorio['resumo']['sub_agentes_total']}")
        print(f"  Discovery Specialist: {'✅' if relatorio['resumo']['discovery_specialist'] else '❌'}")
        print(f"  Histórico funciona: {'✅' if relatorio['resumo']['ultima_entrevista_existe'] else '❌'}")
        
    except Exception as e:
        print(f"❌ Erro durante auditoria: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()