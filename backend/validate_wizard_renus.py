"""
Validação Crítica: Wizard e RENUS
Parte 1: Verificar estado PRÉ-TESTE do banco
"""

from supabase import create_client, Client
from datetime import datetime

# Credenciais
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def main():
    print("=" * 80)
    print("VALIDAÇÃO WIZARD E RENUS - PARTE 1: ESTADO PRÉ-TESTE")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # Conectar
    print("🔌 Conectando ao Supabase...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    print("✅ Conectado!")
    print()
    
    # ========================================
    # 1. CONTAR REGISTROS PRÉ-TESTE
    # ========================================
    print("=" * 80)
    print("1. CONTAGEM DE REGISTROS (PRÉ-TESTE)")
    print("=" * 80)
    print()
    
    try:
        # sub_agents
        sub_agents_result = supabase.table('sub_agents').select('*', count='exact').execute()
        sub_agents_count = sub_agents_result.count or 0
        print(f"📊 sub_agents: {sub_agents_count} registros")
        
        # renus_config
        renus_config_result = supabase.table('renus_config').select('*', count='exact').execute()
        renus_config_count = renus_config_result.count or 0
        print(f"📊 renus_config: {renus_config_count} registros")
        
    except Exception as e:
        print(f"❌ Erro ao contar: {e}")
    
    print()
    
    # ========================================
    # 2. ÚLTIMOS 3 REGISTROS DE CADA TABELA
    # ========================================
    print("=" * 80)
    print("2. ÚLTIMOS 3 REGISTROS")
    print("=" * 80)
    print()
    
    try:
        print("📋 sub_agents (últimos 3):")
        print("-" * 80)
        sub_agents_last = supabase.table('sub_agents')\
            .select('id, name, created_at, status, template_type')\
            .order('created_at', desc=True)\
            .limit(3)\
            .execute()
        
        for agent in sub_agents_last.data:
            print(f"  ID: {agent.get('id')}")
            print(f"  Nome: {agent.get('name')}")
            print(f"  Template: {agent.get('template_type')}")
            print(f"  Status: {agent.get('status')}")
            print(f"  Criado: {agent.get('created_at')}")
            print("-" * 80)
        
        print()
        print("📋 renus_config (últimos 3):")
        print("-" * 80)
        renus_config_last = supabase.table('renus_config')\
            .select('id, client_id, agent_type, created_at')\
            .order('created_at', desc=True)\
            .limit(3)\
            .execute()
        
        if renus_config_last.data:
            for config in renus_config_last.data:
                print(f"  ID: {config.get('id')}")
                print(f"  Client ID: {config.get('client_id')}")
                print(f"  Agent Type: {config.get('agent_type')}")
                print(f"  Criado: {config.get('created_at')}")
                print("-" * 80)
        else:
            print("  (Nenhum registro)")
            print("-" * 80)
        
    except Exception as e:
        print(f"❌ Erro ao buscar últimos registros: {e}")
    
    print()
    
    # ========================================
    # 3. LISTAR TODAS AS TABELAS
    # ========================================
    print("=" * 80)
    print("3. TODAS AS TABELAS DO SCHEMA PUBLIC")
    print("=" * 80)
    print()
    
    try:
        # Usar RPC ou query direta não funciona bem com Supabase client
        # Vamos listar as tabelas conhecidas e tentar acessá-las
        known_tables = [
            'profiles', 'clients', 'leads', 'projects',
            'conversations', 'messages', 'interviews', 'interview_messages',
            'sub_agents', 'renus_config', 'tools', 'isa_commands',
            'integrations', 'triggers', 'wizard_sessions'
        ]
        
        print("Verificando tabelas conhecidas:")
        existing_tables = []
        
        for table in known_tables:
            try:
                result = supabase.table(table).select('id').limit(1).execute()
                existing_tables.append(table)
                print(f"  ✅ {table}")
            except:
                print(f"  ❌ {table} (não existe)")
        
        print()
        print(f"Total de tabelas existentes: {len(existing_tables)}")
        
    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")
    
    print()
    
    # ========================================
    # 4. VERIFICAR TABELA WIZARD_SESSIONS
    # ========================================
    print("=" * 80)
    print("4. VERIFICAR TABELA WIZARD_SESSIONS")
    print("=" * 80)
    print()
    
    try:
        wizard_result = supabase.table('wizard_sessions').select('*', count='exact').execute()
        wizard_count = wizard_result.count or 0
        print(f"📊 wizard_sessions: {wizard_count} registros")
        
        if wizard_count > 0:
            print()
            print("Últimos 3 registros:")
            print("-" * 80)
            wizard_last = supabase.table('wizard_sessions')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(3)\
                .execute()
            
            for session in wizard_last.data:
                print(f"  ID: {session.get('id')}")
                print(f"  Client ID: {session.get('client_id')}")
                print(f"  Current Step: {session.get('current_step')}")
                print(f"  Status: {session.get('status')}")
                print(f"  Criado: {session.get('created_at')}")
                print("-" * 80)
        
    except Exception as e:
        print(f"⚠️ Tabela wizard_sessions não existe ou erro: {e}")
    
    print()
    
    # ========================================
    # RESUMO PRÉ-TESTE
    # ========================================
    print("=" * 80)
    print("RESUMO PRÉ-TESTE")
    print("=" * 80)
    print()
    print(f"✅ sub_agents: {sub_agents_count} registros")
    print(f"✅ renus_config: {renus_config_count} registros")
    print()
    print("⏭️ PRÓXIMO PASSO:")
    print("   1. Acessar frontend: http://localhost:8081/dashboard/admin/agents")
    print("   2. Criar agente via Wizard")
    print("   3. Executar script PÓS-TESTE")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
