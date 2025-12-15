"""
Script para verificar estrutura da tabela clients
"""
from src.utils.supabase_client import get_client

def check_clients_table():
    supabase = get_client()
    
    print("🔍 Verificando estrutura da tabela clients...\n")
    
    try:
        # Buscar um cliente existente para ver a estrutura
        result = supabase.table('clients').select('*').limit(1).execute()
        
        if result.data:
            print("✅ Estrutura de um cliente existente:")
            print("-" * 60)
            
            client = result.data[0]
            for key, value in client.items():
                print(f"{key:20} = {value}")
            
            print("\n📋 Campos disponíveis:")
            print(", ".join(client.keys()))
        else:
            print("⚠️ Nenhum cliente encontrado para verificar estrutura")
            print("Tentando inserir um cliente de teste...")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_clients_table()
