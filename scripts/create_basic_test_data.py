#!/usr/bin/env python3
"""
Script para criar dados básicos de teste para validação do TRACK 2
"""

import os
import sys
from supabase import create_client, Client
from uuid import UUID
from datetime import datetime

# Configurações do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

# IDs de teste
TEST_SUB_AGENT_ID = "12345678-1234-5678-9012-123456789012"
TEST_CONVERSATION_ID = "87654321-4321-8765-2109-876543210987"
TEST_INTERVIEW_ID = "11111111-2222-3333-4444-555555555555"

def main():
    print("📝 Criando dados básicos de teste...")
    
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # 1. Criar mensagens de teste em interview_messages
        print(f"\n💬 Criando mensagens de teste...")
        
        # Verificar se já existem
        existing = supabase.table('interview_messages').select('*').eq('interview_id', TEST_INTERVIEW_ID).execute()
        
        if not existing.data:
            messages = [
                {
                    'id': '11111111-1111-1111-1111-111111111111',
                    'interview_id': TEST_INTERVIEW_ID,
                    'role': 'user',
                    'content': 'Olá, meu nome é João Silva e meu email é joao@teste.com',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {}
                },
                {
                    'id': '22222222-2222-2222-2222-222222222222',
                    'interview_id': TEST_INTERVIEW_ID,
                    'role': 'assistant',
                    'content': 'Olá João! Como posso ajudá-lo hoje?',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {}
                },
                {
                    'id': '33333333-3333-3333-3333-333333333333',
                    'interview_id': TEST_INTERVIEW_ID,
                    'role': 'user',
                    'content': 'Quero saber os preços dos planos disponíveis',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'metadata': {}
                }
            ]
            
            for msg in messages:
                try:
                    supabase.table('interview_messages').insert(msg).execute()
                    print(f"  ✅ Mensagem criada: {msg['role']} - {msg['content'][:50]}...")
                except Exception as e:
                    print(f"  ⚠️ Erro ao criar mensagem: {e}")
        else:
            print(f"  ✅ Mensagens já existem ({len(existing.data)} encontradas)")
        
        # 2. Criar mensagens de teste em messages (fallback)
        print(f"\n📨 Criando mensagens de conversa...")
        
        existing_conv = supabase.table('messages').select('*').eq('conversation_id', TEST_CONVERSATION_ID).execute()
        
        if not existing_conv.data:
            conv_messages = [
                {
                    'id': '44444444-4444-4444-4444-444444444444',
                    'conversation_id': TEST_CONVERSATION_ID,
                    'sender': 'user',
                    'type': 'text',
                    'content': 'Olá, sou Maria Santos, preciso de ajuda com vendas',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'is_read': False,
                    'metadata': {},
                    'channel': 'whatsapp'
                },
                {
                    'id': '55555555-5555-5555-5555-555555555555',
                    'conversation_id': TEST_CONVERSATION_ID,
                    'sender': 'assistant',
                    'type': 'text',
                    'content': 'Olá Maria! Vou te conectar com nosso especialista em vendas.',
                    'timestamp': datetime.now().isoformat(),
                    'created_at': datetime.now().isoformat(),
                    'is_read': True,
                    'metadata': {},
                    'channel': 'whatsapp'
                }
            ]
            
            for msg in conv_messages:
                try:
                    supabase.table('messages').insert(msg).execute()
                    print(f"  ✅ Mensagem de conversa criada: {msg['sender']} - {msg['content'][:50]}...")
                except Exception as e:
                    print(f"  ⚠️ Erro ao criar mensagem de conversa: {e}")
        else:
            print(f"  ✅ Mensagens de conversa já existem ({len(existing_conv.data)} encontradas)")
        
        # 3. Verificar dados finais
        print(f"\n📊 Resumo final:")
        
        # Contar interview_messages
        try:
            result = supabase.table('interview_messages').select('id', count='exact').execute()
            print(f"  Interview messages: {result.count}")
        except Exception as e:
            print(f"  Erro contando interview_messages: {e}")
        
        # Contar messages
        try:
            result = supabase.table('messages').select('id', count='exact').execute()
            print(f"  Conversation messages: {result.count}")
        except Exception as e:
            print(f"  Erro contando messages: {e}")
        
        # Contar leads
        try:
            result = supabase.table('leads').select('id', count='exact').execute()
            print(f"  Leads: {result.count}")
        except Exception as e:
            print(f"  Erro contando leads: {e}")
        
        print("\n✅ Dados de teste criados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()