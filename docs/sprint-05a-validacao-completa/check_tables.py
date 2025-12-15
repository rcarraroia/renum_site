"""
Script para verificar existência de todas as tabelas no Supabase
"""
from src.utils.supabase_client import get_client

def check_tables():
    supabase = get_client()
    
    tables = [
        'profiles',
        'clients',
        'leads',
        'projects',
        'conversations',
        'messages',
        'interviews',
        'interview_messages',
        'sub_agents',
        'tools',
        'isa_commands',
        'renus_config'
    ]
    
    print("🔍 Verificando tabelas do Supabase...\n")
    
    results = {
        'success': [],
        'failed': []
    }
    
    for table in tables:
        try:
            result = supabase.table(table).select('id').limit(1).execute()
            print(f"✅ {table}: OK ({len(result.data)} registros na amostra)")
            results['success'].append(table)
        except Exception as e:
            print(f"❌ {table}: ERRO - {str(e)[:100]}")
            results['failed'].append(table)
    
    print(f"\n📊 RESUMO:")
    print(f"✅ Sucesso: {len(results['success'])}/{len(tables)}")
    print(f"❌ Falhas: {len(results['failed'])}/{len(tables)}")
    
    if results['failed']:
        print(f"\n⚠️ Tabelas com problema: {', '.join(results['failed'])}")
        return False
    
    return True

if __name__ == "__main__":
    success = check_tables()
    exit(0 if success else 1)
