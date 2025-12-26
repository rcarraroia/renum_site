#!/usr/bin/env python3
"""
Script para verificar constraints da tabela leads
"""

from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def main():
    print("🔍 Verificando constraints da tabela leads...")
    
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # 1. Verificar valores existentes em leads.source
        print(f"\n📋 Valores existentes em leads.source:")
        try:
            result = supabase.table('leads').select('source').execute()
            if result.data:
                sources = set(lead.get('source') for lead in result.data if lead.get('source'))
                print(f"  Valores encontrados: {list(sources)}")
            else:
                print("  Nenhum lead encontrado")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
        
        # 2. Verificar valores existentes em leads.status
        print(f"\n📊 Valores existentes em leads.status:")
        try:
            result = supabase.table('leads').select('status').execute()
            if result.data:
                statuses = set(lead.get('status') for lead in result.data if lead.get('status'))
                print(f"  Valores encontrados: {list(statuses)}")
            else:
                print("  Nenhum lead encontrado")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
        
        # 3. Tentar inserir com diferentes valores de source
        print(f"\n🧪 Testando valores de source:")
        
        test_sources = ['chat', 'whatsapp', 'email', 'website', 'manual', 'api', 'form', 'phone']
        
        for source in test_sources:
            try:
                test_lead = {
                    'name': f'Teste {source}',
                    'phone': f'+551199999{source[-4:].zfill(4)}',
                    'email': f'teste_{source}@teste.com',
                    'source': source,
                    'status': 'novo',
                    'score': 50
                }
                
                result = supabase.table('leads').insert(test_lead).execute()
                print(f"  ✅ Source '{source}' funcionou")
                
                # Deletar o lead de teste
                if result.data:
                    supabase.table('leads').delete().eq('id', result.data[0]['id']).execute()
                break
                
            except Exception as e:
                print(f"  ❌ Source '{source}' falhou: {str(e)[:100]}...")
        
        # 4. Tentar inserir com diferentes valores de status
        print(f"\n🧪 Testando valores de status:")
        
        test_statuses = ['novo', 'ativo', 'qualificado', 'convertido', 'inativo', 'perdido']
        
        for status in test_statuses:
            try:
                test_lead = {
                    'name': f'Teste {status}',
                    'phone': f'+551199999{status[-4:].zfill(4)}',
                    'email': f'teste_{status}@teste.com',
                    'source': 'chat',  # Usar um source que sabemos que funciona
                    'status': status,
                    'score': 50
                }
                
                result = supabase.table('leads').insert(test_lead).execute()
                print(f"  ✅ Status '{status}' funcionou")
                
                # Deletar o lead de teste
                if result.data:
                    supabase.table('leads').delete().eq('id', result.data[0]['id']).execute()
                break
                
            except Exception as e:
                print(f"  ❌ Status '{status}' falhou: {str(e)[:100]}...")
        
        print("\n✅ Verificação de constraints concluída!")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")

if __name__ == "__main__":
    main()