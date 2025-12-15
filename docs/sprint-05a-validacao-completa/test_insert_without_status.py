"""
Script para testar inserção SEM campo status
"""
from src.utils.supabase_client import get_client
import uuid

def test_insert_without_status():
    supabase = get_client()
    
    print("🔍 Testando inserção SEM campo status...\n")
    
    client_data = {
        "id": str(uuid.uuid4()),
        "company_name": "Teste Sem Status",
        "document": "12345678000199",
        "segment": "Tecnologia",
        "contact": {
            "email": "teste@teste.com",
            "phone": "11999999999"
        }
        # SEM campo status
    }
    
    try:
        result = supabase.table('clients').insert(client_data).execute()
        print(f"✅ SUCESSO!")
        print(f"   ID criado: {result.data[0]['id']}")
        print(f"   Status default: {result.data[0].get('status', 'N/A')}")
        
        print("\n📋 Cliente criado:")
        for key, value in result.data[0].items():
            print(f"   {key:20} = {value}")
        
        # Deletar para não poluir
        supabase.table('clients').delete().eq('id', result.data[0]['id']).execute()
        print(f"\n   (Cliente de teste deletado)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_insert_without_status()
