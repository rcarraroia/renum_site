"""
Script para criar trigger que auto-cria profile após registro
"""
import psycopg2

def create_trigger():
    conn_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    print("🔧 Criando trigger para auto-criar profiles...\n")
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("✅ Conectado ao PostgreSQL\n")
        
        # Passo 1: Criar função
        print("1️⃣ Criando função handle_new_user...")
        cursor.execute("""
            CREATE OR REPLACE FUNCTION public.handle_new_user()
            RETURNS trigger AS $$
            BEGIN
                INSERT INTO public.profiles (id, email, first_name, last_name, role)
                VALUES (
                    NEW.id,
                    NEW.email,
                    COALESCE(NEW.raw_user_meta_data->>'first_name', 'User'),
                    COALESCE(NEW.raw_user_meta_data->>'last_name', ''),
                    'guest'
                )
                ON CONFLICT (id) DO NOTHING;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql SECURITY DEFINER;
        """)
        print("   ✅ Função criada\n")
        
        # Passo 2: Remover trigger antigo se existir
        print("2️⃣ Removendo trigger antigo (se existir)...")
        cursor.execute("""
            DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
        """)
        print("   ✅ Trigger antigo removido\n")
        
        # Passo 3: Criar novo trigger
        print("3️⃣ Criando novo trigger...")
        cursor.execute("""
            CREATE TRIGGER on_auth_user_created
                AFTER INSERT ON auth.users
                FOR EACH ROW
                EXECUTE FUNCTION public.handle_new_user();
        """)
        print("   ✅ Trigger criado\n")
        
        # Passo 4: Commit
        conn.commit()
        print("4️⃣ Commit realizado\n")
        
        # Passo 5: Verificar
        print("5️⃣ Verificando trigger...")
        cursor.execute("""
            SELECT 
                trigger_name,
                event_manipulation,
                action_statement
            FROM information_schema.triggers
            WHERE trigger_name = 'on_auth_user_created';
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"   ✅ Trigger verificado:")
            print(f"      Nome: {result[0]}")
            print(f"      Evento: {result[1]}")
            print(f"      Ação: {result[2][:50]}...\n")
        
        cursor.close()
        conn.close()
        
        print("="*70)
        print("✅ TRIGGER CRIADO COM SUCESSO!")
        print("="*70)
        print("\nFuncionalidade:")
        print("  - Ao criar usuário no Auth, profile é criado automaticamente")
        print("  - Role padrão: 'guest'")
        print("  - Usa first_name e last_name do metadata")
        print("\n📝 Próximo passo: Testar criando novo usuário")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_trigger()
    exit(0 if success else 1)
