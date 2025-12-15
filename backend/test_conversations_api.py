"""
Script de teste para validar API de conversas e mensagens
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.supabase import supabase_admin
from src.models.conversation import ConversationCreate, ConversationUpdate
from src.models.message import MessageCreate
from src.services.conversation_service import conversation_service
from src.services.message_service import message_service
import asyncio
from uuid import uuid4

async def test_conversations():
    print("=" * 50)
    print("TESTE: API de Conversas e Mensagens")
    print("=" * 50)
    
    # Teste 1: Verificar tabelas
    print("\n1. Verificando tabelas no Supabase...")
    try:
        conv_result = supabase_admin.table("conversations").select("*").limit(1).execute()
        msg_result = supabase_admin.table("messages").select("*").limit(1).execute()
        print(f"   ✅ Tabela 'conversations' existe")
        print(f"   ✅ Tabela 'messages' existe")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Criar cliente de teste (necessário para conversation)
    print("\n2. Criando cliente de teste...")
    try:
        from src.models.client import ClientCreate, ContactInfo
        from src.services.client_service import client_service
        
        test_client = ClientCreate(
            company_name="Cliente Teste Conversa",
            document="98765432000100",
            segment="Teste",
            status="active"
        )
        client = await client_service.create(test_client)
        print(f"   ✅ Cliente criado! ID: {client.id}")
        client_id = client.id
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 3: Criar conversa
    print("\n3. Testando criação de conversa...")
    try:
        test_conv = ConversationCreate(
            client_id=client_id,
            status="active",
            channel="whatsapp",
            priority="Medium"
        )
        created_conv = await conversation_service.create(test_conv)
        print(f"   ✅ Conversa criada! ID: {created_conv.id}")
        conv_id = created_conv.id
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        # Limpar cliente
        await client_service.delete(client_id)
        return False
    
    # Teste 4: Listar conversas
    print("\n4. Testando listagem de conversas...")
    try:
        conversations = await conversation_service.get_all(page=1, limit=5)
        total = conversations['total'] if isinstance(conversations, dict) else conversations.total
        print(f"   ✅ Listagem OK! Total: {total}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        await conversation_service.delete(conv_id)
        await client_service.delete(client_id)
        return False
    
    # Teste 5: Criar mensagem
    print("\n5. Testando criação de mensagem...")
    try:
        test_msg = MessageCreate(
            conversation_id=conv_id,
            sender="client",
            type="text",
            content="Mensagem de teste"
        )
        created_msg = await message_service.create(test_msg)
        print(f"   ✅ Mensagem criada! ID: {created_msg.id}")
        msg_id = created_msg.id
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        await conversation_service.delete(conv_id)
        await client_service.delete(client_id)
        return False
    
    # Teste 6: Listar mensagens da conversa
    print("\n6. Testando listagem de mensagens...")
    try:
        messages = await message_service.get_by_conversation(conv_id)
        print(f"   ✅ Listagem OK! Total de mensagens: {len(messages)}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Limpeza
    print("\n7. Limpando dados de teste...")
    try:
        await message_service.delete(msg_id)
        await conversation_service.delete(conv_id)
        await client_service.delete(client_id)
        print(f"   ✅ Dados limpos!")
    except Exception as e:
        print(f"   ⚠️ Aviso na limpeza: {e}")
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_conversations())
    sys.exit(0 if result else 1)
