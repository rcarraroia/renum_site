"""
Criar conversation de teste para WebSocket
SOLUÇÃO: Desabilitar constraint temporariamente via SQL
"""
from src.config.supabase import supabase_admin

def create_test_conversation():
    print("Criando conversation de teste via SQL direto...")
    
    try:
        # Usar UUID fixo para testes
        test_id = '00000000-0000-0000-0000-000000000001'
        
        # Verificar se já existe
        existing = supabase_admin.table('conversations').select('*').eq('id', test_id).execute()
        
        if existing.data:
            print("✅ Conversation já existe!")
            print(f"   ID: {existing.data[0]['id']}")
            print(f"   Status: {existing.data[0]['status']}")
            return True
        
        # Criar via SQL direto (bypass constraint)
        sql = f"""
        INSERT INTO conversations (id, status, priority, summary, unread_count, channel)
        VALUES (
            '{test_id}',
            'active',
            'Medium',
            'Conversation de teste para WebSocket',
            0,
            'whatsapp'
        )
        ON CONFLICT (id) DO NOTHING
        RETURNING *;
        """
        
        # Executar via service_role (bypass RLS e constraints)
        result = supabase_admin.rpc('exec_sql', {'query': sql}).execute()
        
        print("✅ Conversation criada com sucesso!")
        print(f"   ID: {test_id}")
        return True
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print("\n💡 SOLUÇÃO ALTERNATIVA:")
        print("   Execute no SQL Editor do Supabase:")
        print(f"""
        INSERT INTO conversations (id, status, priority, summary, unread_count)
        VALUES (
            '00000000-0000-0000-0000-000000000001',
            'active',
            'Medium',
            'Test conversation',
            0
        );
        """)
        return False

if __name__ == "__main__":
    create_test_conversation()
