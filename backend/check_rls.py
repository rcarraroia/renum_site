"""
Script para verificar Row Level Security (RLS) e políticas
"""
from src.utils.supabase_client import get_client

def check_rls():
    supabase = get_client()
    
    print("🔍 Verificando RLS e Políticas...\n")
    
    # Query para verificar RLS habilitado
    rls_query = """
    SELECT 
        tablename,
        rowsecurity
    FROM pg_tables 
    WHERE schemaname = 'public'
        AND tablename IN (
            'profiles', 'clients', 'leads', 'projects',
            'conversations', 'messages', 'interviews',
            'interview_messages', 'sub_agents', 'tools',
            'isa_commands', 'renus_config'
        )
    ORDER BY tablename;
    """
    
    try:
        result = supabase.rpc('exec_sql', {'query': rls_query}).execute()
        print("RLS Status por Tabela:")
        print("-" * 50)
        for row in result.data:
            status = "✅ HABILITADO" if row['rowsecurity'] else "❌ DESABILITADO"
            print(f"{row['tablename']:25} {status}")
    except Exception as e:
        print(f"⚠️ Não foi possível verificar RLS via RPC: {e}")
        print("Tentando método alternativo...")
        
        # Método alternativo: tentar acessar pg_tables diretamente
        try:
            # Nota: Isso pode não funcionar dependendo das permissões
            print("\n⚠️ Verificação de RLS requer acesso direto ao PostgreSQL")
            print("Recomendação: Verificar manualmente no Supabase Dashboard → Database → Tables")
        except Exception as e2:
            print(f"❌ Erro no método alternativo: {e2}")
    
    # Verificar políticas
    print("\n\n🔍 Verificando Políticas RLS...\n")
    
    policies_query = """
    SELECT 
        schemaname,
        tablename,
        policyname,
        permissive,
        roles,
        cmd
    FROM pg_policies
    WHERE schemaname = 'public'
    ORDER BY tablename, policyname;
    """
    
    try:
        result = supabase.rpc('exec_sql', {'query': policies_query}).execute()
        
        if result.data:
            print("Políticas Encontradas:")
            print("-" * 80)
            current_table = None
            for row in result.data:
                if row['tablename'] != current_table:
                    current_table = row['tablename']
                    print(f"\n📋 Tabela: {current_table}")
                
                print(f"  ✅ {row['policyname']}")
                print(f"     Comando: {row['cmd']}, Roles: {row['roles']}")
        else:
            print("⚠️ Nenhuma política encontrada")
            
    except Exception as e:
        print(f"⚠️ Não foi possível verificar políticas via RPC: {e}")
        print("\n📝 RECOMENDAÇÃO:")
        print("Execute estas queries manualmente no Supabase Dashboard → SQL Editor:")
        print("\n1. Verificar RLS:")
        print(rls_query)
        print("\n2. Verificar Políticas:")
        print(policies_query)

if __name__ == "__main__":
    check_rls()
