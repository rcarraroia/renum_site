"""
Script para investigar e corrigir constraint da tabela clients
"""
from src.utils.supabase_client import get_client

def investigate_constraint():
    supabase = get_client()
    
    print("🔍 Investigando constraint da tabela clients...\n")
    
    # Tentar buscar informações sobre a tabela
    try:
        # Buscar um cliente existente para ver estrutura
        result = supabase.table('clients').select('*').limit(1).execute()
        
        if result.data:
            print("✅ Estrutura de cliente existente:")
            for key, value in result.data[0].items():
                print(f"   {key}: {value} ({type(value).__name__})")
        else:
            print("⚠️ Nenhum cliente no banco para verificar estrutura")
        
        print("\n📝 Tentando inserir com diferentes valores de status...\n")
        
        # Tentar inserir sem status (para ver o default)
        import uuid
        test_id = str(uuid.uuid4())
        
        # Primeiro, vamos ver se há um ENUM definido
        # Tentando valores em português
        status_values = [
            None,  # Sem status
            "ativo",
            "inativo", 
            "suspenso",
            "pendente",
            "ativa",
            "inativa",
            "suspensa"
        ]
        
        for status_val in status_values:
            test_data = {
                "id": str(uuid.uuid4()),
                "company_name": f"Teste {status_val}",
                "document": "12345678000199",
                "segment": "Tecnologia"
            }
            
            if status_val is not None:
                test_data["status"] = status_val
            
            try:
                result = supabase.table('clients').insert(test_data).execute()
                print(f"✅ SUCESSO com status='{status_val}'")
                
                # Verificar o valor salvo
                saved = result.data[0]
                print(f"   Status salvo: '{saved.get('status')}'")
                
                # Deletar teste
                supabase.table('clients').delete().eq('id', saved['id']).execute()
                print(f"   (Deletado)\n")
                
                return saved.get('status')
                
            except Exception as e:
                error_msg = str(e)
                if "clients_status_check" in error_msg:
                    print(f"❌ Falhou com status='{status_val}' - constraint violado")
                elif "not-null" in error_msg:
                    print(f"❌ Falhou com status='{status_val}' - campo obrigatório")
                else:
                    print(f"❌ Falhou com status='{status_val}' - {error_msg[:80]}")
        
        print("\n⚠️ Nenhum valor funcionou!")
        print("\n📋 AÇÃO NECESSÁRIA:")
        print("Precisamos acessar o Supabase Dashboard para:")
        print("1. Ver a definição do CHECK constraint")
        print("2. Ver se há um ENUM definido")
        print("3. Corrigir manualmente")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    investigate_constraint()
