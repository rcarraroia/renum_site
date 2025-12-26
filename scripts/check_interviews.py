"""Script para verificar entrevistas recentes no banco"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from supabase import create_client

SUPABASE_URL = "https://vhixvzaxswphwoymdhgg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZoaXh2emF4c3dwaHdveW1kaGdnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Mzg1NzY1MywiZXhwIjoyMDc5NDMzNjUzfQ.xxxQfBujTru8UnmW-JKLzGBLGVDAVU4D1_5Q2fB49lw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=" * 80)
print("ANÁLISE DE ENTREVISTAS RECENTES")
print("=" * 80)

# Buscar últimas 15 entrevistas
response = supabase.table('interviews').select('id, created_at, status, subagent_id').order('created_at', desc=True).limit(15).execute()

print(f"\nÚltimas {len(response.data)} entrevistas:")
print("-" * 80)

for i, interview in enumerate(response.data, 1):
    print(f"{i}. ID: {interview['id'][:8]}... | Status: {interview['status']} | Criado: {interview['created_at']}")

# Contar entrevistas criadas hoje
from datetime import datetime, timedelta
today = datetime.now().strftime('%Y-%m-%d')

response_today = supabase.table('interviews').select('id', count='exact').gte('created_at', today).execute()
print(f"\n📊 Entrevistas criadas HOJE ({today}): {response_today.count}")

# Verificar mensagens da última entrevista
if response.data:
    last_interview_id = response.data[0]['id']
    print(f"\n📝 Mensagens da última entrevista ({last_interview_id[:8]}...):")
    print("-" * 80)
    
    messages = supabase.table('interview_messages').select('role, content, created_at').eq('interview_id', last_interview_id).order('created_at').execute()
    
    if messages.data:
        for msg in messages.data:
            role = "👤 USER" if msg['role'] == 'user' else "🤖 AGENT"
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"  {role}: {content}")
    else:
        print("  (Nenhuma mensagem encontrada)")

print("\n" + "=" * 80)
