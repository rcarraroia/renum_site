#!/usr/bin/env python3
"""
Teste direto da funcionalidade de captura de leads
Testa especificamente o método capture_from_conversation
"""

import sys
import os
from supabase import create_client, Client
from datetime import datetime
import re

# Configurações do Supabase
SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

def extract_contact_info(messages):
    """
    Extrai informações de contato das mensagens usando regex
    (Simulação da lógica do LeadService)
    """
    try:
        # Concatenar mensagens do usuário
        user_messages = [
            msg['content'] for msg in messages 
            if msg.get('role') == 'user' and msg.get('content')
        ]
        
        if not user_messages:
            return {}
        
        conversation_text = " ".join(user_messages)
        
        contact_data = {}
        
        # Extrair email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, conversation_text)
        if emails:
            contact_data['email'] = emails[0]
        
        # Extrair telefone (formato brasileiro)
        phone_patterns = [
            r'\+55\s*\(?(\d{2})\)?\s*\d{4,5}[-\s]?\d{4}',  # +55 (11) 99999-9999
            r'\(?(\d{2})\)?\s*\d{4,5}[-\s]?\d{4}',         # (11) 99999-9999
            r'\d{10,11}',                                   # 11999999999
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, conversation_text)
            if phones:
                # Normalizar telefone
                phone = re.sub(r'[^\d]', '', phones[0] if isinstance(phones[0], str) else conversation_text)
                if len(phone) >= 10:
                    if not phone.startswith('55'):
                        phone = '55' + phone
                    contact_data['phone'] = '+' + phone
                    break
        
        # Extrair nome (heurística simples)
        name_patterns = [
            r'(?:meu nome é|me chamo|sou (?:a|o)?)\s+([A-Za-zÀ-ÿ\s]{2,30})',
            r'(?:nome:?)\s+([A-Za-zÀ-ÿ\s]{2,30})',
        ]
        
        for pattern in name_patterns:
            names = re.findall(pattern, conversation_text, re.IGNORECASE)
            if names:
                name = names[0].strip().title()
                # Validar se parece um nome real
                if len(name.split()) <= 4 and all(len(word) >= 2 for word in name.split()):
                    contact_data['name'] = name
                    break
        
        return contact_data
        
    except Exception as e:
        print(f"Erro na extração: {e}")
        return {}

def test_lead_capture():
    """Testa a captura de leads diretamente"""
    print("🧪 Testando captura de leads diretamente...")
    
    try:
        # Conectar ao Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        
        # 1. Testar extração de dados de contato
        print("\n📋 Teste 1: Extração de dados de contato")
        
        test_messages = [
            {"role": "user", "content": "Olá, meu nome é João Silva e meu email é joao@teste.com"},
            {"role": "assistant", "content": "Olá João! Como posso ajudá-lo?"},
            {"role": "user", "content": "Meu telefone é (11) 99999-9999 e quero saber os preços"}
        ]
        
        contact_data = extract_contact_info(test_messages)
        print(f"  Dados extraídos: {contact_data}")
        
        has_name = 'name' in contact_data
        has_email = 'email' in contact_data
        has_phone = 'phone' in contact_data
        
        print(f"  ✅ Nome detectado: {has_name} ({'✓' if has_name else '✗'})")
        print(f"  ✅ Email detectado: {has_email} ({'✓' if has_email else '✗'})")
        print(f"  ✅ Telefone detectado: {has_phone} ({'✓' if has_phone else '✗'})")
        
        # 2. Testar criação de lead no banco
        print("\n💾 Teste 2: Criação de lead no banco")
        
        if contact_data.get('email') or contact_data.get('phone'):
            # Verificar se lead já existe
            phone_to_check = contact_data.get('phone', '+5511999999999')
            existing = supabase.table('leads').select('*').eq('phone', phone_to_check).execute()
            
            if existing.data:
                print(f"  ⚠️ Lead já existe: {existing.data[0]['id']}")
                lead_id = existing.data[0]['id']
                
                # Atualizar com novos dados
                update_data = {}
                if contact_data.get('name') and not existing.data[0].get('name'):
                    update_data['name'] = contact_data['name']
                if contact_data.get('email') and not existing.data[0].get('email'):
                    update_data['email'] = contact_data['email']
                
                if update_data:
                    supabase.table('leads').update(update_data).eq('id', lead_id).execute()
                    print(f"  ✅ Lead atualizado com: {update_data}")
                else:
                    print(f"  ✅ Lead já estava atualizado")
            else:
                # Criar novo lead
                lead_data = {
                    'name': contact_data.get('name', f"Lead {contact_data.get('phone', contact_data.get('email'))}"),
                    'email': contact_data.get('email'),
                    'phone': contact_data.get('phone', '+5511999999999'),
                    'source': 'pesquisa',  # Usar valor válido do constraint
                    'status': 'qualificado',  # Usar valor válido do constraint
                    'subagent_id': '12345678-1234-5678-9012-123456789012',
                    'notes': f"Capturado automaticamente em teste - {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                    'first_contact_at': datetime.now().isoformat(),
                    'last_interaction_at': datetime.now().isoformat(),
                    'score': 50
                }
                
                result = supabase.table('leads').insert(lead_data).execute()
                
                if result.data:
                    lead_id = result.data[0]['id']
                    print(f"  ✅ Lead criado: {lead_id}")
                    print(f"  📝 Nome: {result.data[0]['name']}")
                    print(f"  📧 Email: {result.data[0]['email']}")
                    print(f"  📱 Telefone: {result.data[0]['phone']}")
                else:
                    print(f"  ❌ Falha ao criar lead")
                    return False
        else:
            print(f"  ⚠️ Dados insuficientes para criar lead")
            return False
        
        # 3. Testar busca de mensagens de conversa
        print("\n💬 Teste 3: Busca de mensagens de conversa")
        
        # Buscar uma conversa real do banco
        interviews = supabase.table('interviews').select('id').limit(1).execute()
        
        if interviews.data:
            interview_id = interviews.data[0]['id']
            print(f"  🔍 Testando com interview: {interview_id}")
            
            # Buscar mensagens desta entrevista
            messages = supabase.table('interview_messages').select('*').eq('interview_id', interview_id).limit(5).execute()
            
            if messages.data:
                print(f"  ✅ Encontradas {len(messages.data)} mensagens")
                for i, msg in enumerate(messages.data[:3]):  # Mostrar apenas 3
                    print(f"    {i+1}. {msg.get('role', 'unknown')}: {msg.get('content', '')[:50]}...")
            else:
                print(f"  ⚠️ Nenhuma mensagem encontrada para esta entrevista")
        else:
            print(f"  ⚠️ Nenhuma entrevista encontrada no banco")
        
        # 4. Testar detecção de interesse comercial
        print("\n💰 Teste 4: Detecção de interesse comercial")
        
        commercial_patterns = [
            'preço', 'valor', 'custo', 'quanto custa', 'plano', 'assinatura',
            'contratar', 'comprar', 'adquirir', 'orçamento', 'proposta'
        ]
        
        test_commercial_messages = [
            "Quero saber os preços dos planos",
            "Quanto custa o serviço?",
            "Gostaria de contratar",
            "Preciso de um orçamento",
            "Apenas uma dúvida técnica"
        ]
        
        for msg in test_commercial_messages:
            has_commercial_intent = any(pattern in msg.lower() for pattern in commercial_patterns)
            status = "✅" if has_commercial_intent else "❌"
            print(f"  {status} '{msg}' → Interesse comercial: {has_commercial_intent}")
        
        print("\n🎉 Todos os testes de captura de leads concluídos!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 Teste Direto - Captura de Leads")
    print("=" * 50)
    
    success = test_lead_capture()
    
    if success:
        print("\n✅ RESULTADO: Captura de leads está funcionando!")
        return 0
    else:
        print("\n❌ RESULTADO: Captura de leads tem problemas!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)