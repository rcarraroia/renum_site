#!/usr/bin/env python3
"""
TESTE DE FUNCIONALIDADES CRÍTICAS - RENUM
Valida manualmente as funcionalidades essenciais do sistema
"""

import requests
import json
from datetime import datetime
from supabase import create_client, Client

# Configurações
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

BACKEND_URL = "http://localhost:8000"

def testar_conexao_supabase():
    """Testa conexão com Supabase"""
    print("🔍 TESTANDO CONEXÃO SUPABASE...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # Teste simples: contar agentes
        result = supabase.table('agents').select('id').execute()
        
        print(f"  ✅ Conectado ao Supabase")
        print(f"  ✅ {len(result.data)} agentes encontrados")
        return True, supabase
        
    except Exception as e:
        print(f"  ❌ Erro ao conectar: {e}")
        return False, None

def testar_rls_vazamento(supabase):
    """Testa se RLS está funcionando (simulando usuário não-admin)"""
    print("\n🔒 TESTANDO VAZAMENTO DE DADOS (RLS)...")
    
    try:
        # Usar anon key (simula usuário comum)
        supabase_anon = create_client(
            SUPABASE_URL, 
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NTc2NTMsImV4cCI6MjA3OTQzMzY1M30.E8YARatueM44zcA8lgQBd4hi2J1P3rA3EyvH5d4Wa-4"
        )
        
        # Tentar acessar agentes sem autenticação
        result = supabase_anon.table('agents').select('*').execute()
        
        if result.data:
            print(f"  ❌ VAZAMENTO: {len(result.data)} agentes acessíveis sem auth")
            print(f"      Agentes vazados: {[a['name'] for a in result.data]}")
            return False
        else:
            print("  ✅ RLS bloqueou acesso não autorizado")
            return True
            
    except Exception as e:
        if "JWT" in str(e) or "auth" in str(e).lower():
            print("  ✅ RLS bloqueou acesso (erro de auth esperado)")
            return True
        else:
            print(f"  ⚠️ Erro inesperado: {e}")
            return False

def testar_backend_rodando():
    """Testa se backend está rodando"""
    print("\n🖥️ TESTANDO BACKEND...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        
        if response.status_code == 200:
            print("  ✅ Backend respondendo na porta 8000")
            return True
        else:
            print(f"  ❌ Backend retornou status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  ❌ Backend não está rodando na porta 8000")
        return False
    except requests.exceptions.Timeout:
        print("  ❌ Backend não respondeu em 5 segundos")
        return False
    except Exception as e:
        print(f"  ❌ Erro ao testar backend: {e}")
        return False

def testar_historico_conversas(supabase):
    """Testa se histórico de conversas funciona"""
    print("\n💬 TESTANDO HISTÓRICO DE CONVERSAS...")
    
    try:
        # Buscar última entrevista
        result = supabase.table('interviews').select('*').order('created_at', desc=True).limit(1).execute()
        
        if not result.data:
            print("  ❌ Nenhuma entrevista encontrada")
            return False
        
        entrevista = result.data[0]
        print(f"  ✅ Última entrevista: {entrevista['id']}")
        print(f"      Nome: {entrevista.get('contact_name', 'N/A')}")
        print(f"      Status: {entrevista['status']}")
        
        # Buscar mensagens da entrevista
        msgs_result = supabase.table('interview_messages').select('*').eq('interview_id', entrevista['id']).order('created_at').execute()
        
        print(f"      Mensagens: {len(msgs_result.data)}")
        
        if len(msgs_result.data) > 0:
            print("  ✅ Mensagens encontradas")
            
            # Verificar se há mensagens do usuário e do assistente
            roles = [msg['role'] for msg in msgs_result.data]
            has_user = 'user' in roles
            has_assistant = 'assistant' in roles
            
            print(f"      Mensagens do usuário: {'✅' if has_user else '❌'}")
            print(f"      Mensagens do assistente: {'✅' if has_assistant else '❌'}")
            
            return has_user and has_assistant
        else:
            print("  ❌ Nenhuma mensagem encontrada")
            return False
            
    except Exception as e:
        print(f"  ❌ Erro ao testar histórico: {e}")
        return False

def testar_client_id_obrigatorio(supabase):
    """Testa se client_id é obrigatório"""
    print("\n🏢 TESTANDO CLIENT_ID OBRIGATÓRIO...")
    
    try:
        # Tentar criar agente sem client_id
        test_agent = {
            'name': 'TESTE_AGENT_SEM_CLIENT_ID',
            'description': 'Agente de teste para validar client_id obrigatório',
            'status': 'active'
            # Propositalmente sem client_id
        }
        
        result = supabase.table('agents').insert(test_agent).execute()
        
        if result.data:
            # Se conseguiu inserir, client_id não é obrigatório
            agent_id = result.data[0]['id']
            print("  ❌ client_id NÃO é obrigatório (agente criado sem client_id)")
            
            # Limpar teste
            supabase.table('agents').delete().eq('id', agent_id).execute()
            print("      (agente de teste removido)")
            
            return False
        else:
            print("  ✅ client_id é obrigatório (inserção falhou)")
            return True
            
    except Exception as e:
        if "null value" in str(e).lower() or "not null" in str(e).lower():
            print("  ✅ client_id é obrigatório (constraint NOT NULL)")
            return True
        else:
            print(f"  ⚠️ Erro inesperado: {e}")
            return False

def testar_sub_agentes(supabase):
    """Testa se sub-agentes existem"""
    print("\n🤖 TESTANDO SUB-AGENTES...")
    
    try:
        result = supabase.table('sub_agents').select('*').execute()
        
        total = len(result.data)
        print(f"  Sub-agentes encontrados: {total}")
        
        if total == 0:
            print("  ❌ Nenhum sub-agente implementado")
            return False
        
        # Verificar Discovery Specialist
        discovery_found = False
        for sub_agent in result.data:
            print(f"    - {sub_agent['name']} ({sub_agent.get('type', 'N/A')})")
            if 'discovery' in sub_agent['name'].lower():
                discovery_found = True
        
        if discovery_found:
            print("  ✅ Discovery Specialist encontrado")
        else:
            print("  ❌ Discovery Specialist não encontrado")
        
        return discovery_found
        
    except Exception as e:
        print(f"  ❌ Erro ao testar sub-agentes: {e}")
        return False

def gerar_relatorio_testes(resultados):
    """Gera relatório dos testes"""
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE TESTES FUNCIONAIS")
    print("="*60)
    
    total_testes = len(resultados)
    testes_ok = sum(1 for r in resultados.values() if r)
    
    print(f"Total de testes: {total_testes}")
    print(f"Testes passaram: {testes_ok}")
    print(f"Testes falharam: {total_testes - testes_ok}")
    print(f"Taxa de sucesso: {(testes_ok/total_testes)*100:.1f}%")
    
    print("\nDetalhamento:")
    for teste, passou in resultados.items():
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        print(f"  {teste}: {status}")
    
    # Salvar relatório
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relatorio = {
        'timestamp': timestamp,
        'data_teste': datetime.now().isoformat(),
        'total_testes': total_testes,
        'testes_ok': testes_ok,
        'testes_falhou': total_testes - testes_ok,
        'taxa_sucesso': (testes_ok/total_testes)*100,
        'resultados': resultados
    }
    
    filename = f'teste_funcionalidades_{timestamp}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✅ Relatório salvo: {filename}")
    
    return relatorio

def main():
    """Função principal"""
    print("🧪 INICIANDO TESTES DE FUNCIONALIDADES CRÍTICAS")
    print("="*60)
    
    resultados = {}
    
    # Teste 1: Conexão Supabase
    conectou, supabase = testar_conexao_supabase()
    resultados['conexao_supabase'] = conectou
    
    if not conectou:
        print("❌ Não foi possível conectar ao Supabase. Abortando testes.")
        return
    
    # Teste 2: RLS (vazamento de dados)
    resultados['rls_funcionando'] = testar_rls_vazamento(supabase)
    
    # Teste 3: Backend rodando
    resultados['backend_rodando'] = testar_backend_rodando()
    
    # Teste 4: Histórico de conversas
    resultados['historico_conversas'] = testar_historico_conversas(supabase)
    
    # Teste 5: client_id obrigatório
    resultados['client_id_obrigatorio'] = testar_client_id_obrigatorio(supabase)
    
    # Teste 6: Sub-agentes
    resultados['sub_agentes_implementados'] = testar_sub_agentes(supabase)
    
    # Gerar relatório
    relatorio = gerar_relatorio_testes(resultados)
    
    # Conclusão
    if relatorio['taxa_sucesso'] >= 80:
        print("\n🎉 SISTEMA EM BOM ESTADO (≥80% dos testes passaram)")
    elif relatorio['taxa_sucesso'] >= 60:
        print("\n⚠️ SISTEMA PRECISA DE ATENÇÃO (60-79% dos testes passaram)")
    else:
        print("\n🚨 SISTEMA COM PROBLEMAS CRÍTICOS (<60% dos testes passaram)")

if __name__ == "__main__":
    main()