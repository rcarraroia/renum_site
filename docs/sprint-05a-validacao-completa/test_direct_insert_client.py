"""
Script para testar inserção direta no Supabase
"""
from src.utils.supabase_client import get_client
import uuid

def test_direct_insert():
    supabase = get_client()
    
    print("🔍 Testando inserção direta na tabela clients...\n")
    
    # Tentar diferentes valores de status
    status_values = ["ativo", "inativo", "suspenso", "active", "inactive", "suspended"]
    
    for status_val in status_values:
        print(f"Tentando status: '{status_val}'")
        
        client_data = {
            "id": str(uuid.uuid4()),
            "company_name": f"Teste Status {status_val}",
            "document": "12345678000199",
            "segment": "Tecnologia",
            "status": status_val,
            "contact": {
                "email": "teste@teste.com",
                "phone": "11999999999"
            }
        }
        
        try:
            result = supabase.table('clients').insert(client_data).execute()
            print(f"✅ SUCESSO com status='{status_val}'!")
            print(f"   ID criado: {result.data[0]['id']}")
            
            # Deletar para não poluir o banco
            supabase.table('clients').delete().eq('id', result.data[0]['id']).execute()
            print(f"   (Cliente de teste deletado)\n")
            
            return status_val
            
        except Exception as e:
            error_msg = str(e)
            if "clients_status_check" in error_msg:
                print(f"❌ Falhou - constraint violado\n")
            else:
                print(f"❌ Erro: {error_msg[:100]}\n")
    
    print("⚠️ Nenhum valor de status funcionou!")
    print("\n📝 RECOMENDAÇÃO:")
    print("Verifique no Supabase Dashboard → Database → Tables → clients")
    print("Qual é o tipo ENUM ou CHECK constraint do campo 'status'")

if __name__ == "__main__":
    test_direct_insert()
