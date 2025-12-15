"""
Script de teste de conectividade Supabase
"""
from src.config.settings import settings
from src.utils.supabase_client import get_client

def test_supabase():
    print("🔍 Testando conexão Supabase...")
    print(f"URL: {settings.SUPABASE_URL}")
    print(f"Key: {settings.SUPABASE_ANON_KEY[:20]}...")
    
    try:
        supabase = get_client()
        print("✅ Cliente Supabase criado")
        
        # Testar query simples
        result = supabase.table('profiles').select('*').limit(1).execute()
        print(f"✅ Query funcionou - {len(result.data)} registros")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_supabase()
    exit(0 if success else 1)
