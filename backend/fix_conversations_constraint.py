"""
Script para investigar e corrigir o constraint de conversations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.supabase import supabase_admin

print("=" * 60)
print("INVESTIGAÇÃO: Constraint de conversations")
print("=" * 60)

# 1. Verificar constraint atual
print("\n1. Verificando constraint atual...")
try:
    # Query para ver o constraint
    query = """
    SELECT 
        conname as constraint_name,
        pg_get_constraintdef(oid) as constraint_definition
    FROM pg_constraint 
    WHERE conrelid = 'conversations'::regclass 
    AND contype = 'c';
    """
    
    result = supabase_admin.rpc('exec_sql', {'query': query}).execute()
    print(f"   Constraints encontrados: {result.data if result.data else 'Nenhum'}")
except Exception as e:
    print(f"   ⚠️ Não foi possível consultar via RPC: {e}")
    print("   Tentando método alternativo...")

# 2. Tentar inserir com diferentes valores para descobrir o aceito
print("\n2. Testando valores aceitos para 'channel'...")

test_values = ['whatsapp', 'email', 'web', 'sms', 'phone', 'chat', 'telegram']

# Criar um cliente de teste primeiro
from src.models.client import ClientCreate
from src.services.client_service import client_service
import asyncio

async def test_channels():
    # Criar cliente
    test_client = ClientCreate(
        company_name="Teste Constraint",
        document="11111111000111",
        segment="Teste",  # Obrigatório!
        status="active"
    )
    client = await client_service.create(test_client)
    client_id = str(client.id)
    
    print(f"   Cliente de teste criado: {client_id}")
    
    accepted_channels = []
    
    for channel_value in test_values:
        try:
            # Tentar inserir diretamente
            data = {
                'client_id': client_id,
                'status': 'active',
                'channel': channel_value,
                'priority': 'Medium',
                'unread_count': 0,
                'tags': []
            }
            
            result = supabase_admin.table('conversations').insert(data).execute()
            
            if result.data:
                accepted_channels.append(channel_value)
                print(f"   ✅ '{channel_value}' - ACEITO")
                # Deletar imediatamente
                conv_id = result.data[0]['id']
                supabase_admin.table('conversations').delete().eq('id', conv_id).execute()
            else:
                print(f"   ❌ '{channel_value}' - REJEITADO")
                
        except Exception as e:
            error_msg = str(e)
            if 'check constraint' in error_msg.lower():
                print(f"   ❌ '{channel_value}' - REJEITADO (constraint)")
            else:
                print(f"   ⚠️ '{channel_value}' - ERRO: {error_msg[:100]}")
    
    # Limpar cliente de teste
    await client_service.delete(client_id)
    
    print(f"\n3. RESUMO:")
    print(f"   Valores aceitos: {accepted_channels if accepted_channels else 'NENHUM!'}")
    
    if not accepted_channels:
        print("\n⚠️ PROBLEMA CRÍTICO: Nenhum valor é aceito!")
        print("   O constraint precisa ser removido ou corrigido no Supabase.")
        print("\n   SQL para corrigir:")
        print("   ALTER TABLE conversations DROP CONSTRAINT IF EXISTS conversations_channel_check;")
        print("   ALTER TABLE conversations ADD CONSTRAINT conversations_channel_check")
        print("   CHECK (channel IN ('whatsapp', 'email', 'web', 'sms'));")
    
    return accepted_channels

if __name__ == "__main__":
    result = asyncio.run(test_channels())
    sys.exit(0 if result else 1)
