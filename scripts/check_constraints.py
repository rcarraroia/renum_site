#!/usr/bin/env python3
"""
Script para verificar constraints e valores válidos nas tabelas
"""

import os
import sys
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def main():
    print("🔍 Verificando constraints e valores válidos...")
    
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # 1. Verificar valores existentes em messages.sender
        print(f"\n📨 Valores existentes em messages.sender:")
        try:
            result = supabase.table('messages').select('sender').execute()
            if result.data:
                senders = set(msg.get('sender') for msg in result.data if msg.get('sender'))
                print(f"  Valores encontrados: {list(senders)}")
            else:
                print("  Nenhuma mensagem encontrada")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
        
        # 2. Verificar se existe tabela interviews
        print(f"\n🎤 Verificando tabela interviews:")
        try:
            result = supabase.table('interviews').select('id').limit(5).execute()
            if result.data:
                print(f"  ✅ Tabela interviews existe com {len(result.data)} registros")
                print(f"  IDs encontrados: {[r['id'] for r in result.data]}")
            else:
                print("  ⚠️ Tabela interviews existe mas está vazia")
        except Exception as e:
            print(f"  ❌ Erro ao acessar interviews: {e}")
        
        # 3. Verificar se existe tabela conversations
        print(f"\n💬 Verificando tabela conversations:")
        try:
            result = supabase.table('conversations').select('id').limit(5).execute()
            if result.data:
                print(f"  ✅ Tabela conversations existe com {len(result.data)} registros")
                print(f"  IDs encontrados: {[r['id'] for r in result.data]}")
            else:
                print("  ⚠️ Tabela conversations existe mas está vazia")
        except Exception as e:
            print(f"  ❌ Erro ao acessar conversations: {e}")
        
        # 4. Tentar inserir uma mensagem simples para ver o erro
        print(f"\n🧪 Testando inserção em messages:")
        try:
            # Primeiro, criar uma conversation se não existir
            conv_id = "test-conversation-123"
            try:
                supabase.table('conversations').insert({
                    'id': conv_id,
                    'status': 'open',
                    'created_at': '2025-12-23T18:00:00Z'
                }).execute()
                print(f"  ✅ Conversation criada: {conv_id}")
            except Exception as e:
                print(f"  ⚠️ Erro ao criar conversation (pode já existir): {e}")
            
            # Tentar diferentes valores para sender
            test_senders = ['user', 'assistant', 'system', 'bot', 'agent', 'client']
            
            for sender in test_senders:
                try:
                    test_msg = {
                        'conversation_id': conv_id,
                        'sender': sender,
                        'type': 'text',
                        'content': f'Teste com sender={sender}',
                        'timestamp': '2025-12-23T18:00:00Z',
                        'is_read': False,
                        'metadata': {},
                        'channel': 'test'
                    }
                    
                    result = supabase.table('messages').insert(test_msg).execute()
                    print(f"  ✅ Sender '{sender}' funcionou")
                    
                    # Deletar a mensagem de teste
                    supabase.table('messages').delete().eq('id', result.data[0]['id']).execute()
                    break
                    
                except Exception as e:
                    print(f"  ❌ Sender '{sender}' falhou: {str(e)[:100]}...")
                    
        except Exception as e:
            print(f"  ❌ Erro geral no teste: {e}")
        
        print("\n✅ Verificação de constraints concluída!")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()