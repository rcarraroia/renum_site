#!/usr/bin/env python3
"""
Verificar valores válidos para pattern_type
"""

import sys
from pathlib import Path

# Configurar path
backend_path = Path(__file__).parent
src_path = backend_path / "src"
sys.path.insert(0, str(src_path))

from config.supabase import supabase_admin

try:
    print("🔍 VERIFICANDO PATTERN TYPES VÁLIDOS")
    print("=" * 40)
    
    # Tentar inserir com diferentes valores para descobrir os válidos
    test_values = [
        "conversation", "response", "greeting", "question", 
        "action", "decision", "analysis", "recommendation"
    ]
    
    TEST_AGENT_ID = "37ae9902-24bf-42b1-9d01-88c201ee0a6c"
    TEST_CLIENT_ID = "9e26202e-7090-4051-9bfd-6b397b3947cc"
    
    valid_types = []
    
    for pattern_type in test_values:
        test_pattern = {
            'agent_id': TEST_AGENT_ID,
            'client_id': TEST_CLIENT_ID,
            'pattern_type': pattern_type,
            'trigger_context': {'test': True},
            'action_config': {'test': True},
            'success_rate': 0.5,
            'total_applications': 1,
            'successful_applications': 1,
            'is_active': True
        }
        
        try:
            result = supabase_admin.table('agent_behavior_patterns').insert(
                test_pattern
            ).execute()
            
            if result.data:
                created_id = result.data[0]['id']
                valid_types.append(pattern_type)
                print(f"✅ {pattern_type} - VÁLIDO")
                
                # Remover imediatamente
                supabase_admin.table('agent_behavior_patterns').delete().eq(
                    'id', created_id
                ).execute()
            else:
                print(f"❌ {pattern_type} - INVÁLIDO")
                
        except Exception as e:
            error_msg = str(e)
            if "pattern_type_valid" in error_msg:
                print(f"❌ {pattern_type} - CONSTRAINT VIOLATION")
            else:
                print(f"❌ {pattern_type} - ERRO: {error_msg[:50]}...")
    
    print(f"\n📝 Pattern types válidos encontrados: {valid_types}")
    
    if not valid_types:
        print("⚠️  Nenhum tipo válido encontrado. Verificando constraint...")
        
        # Tentar descobrir a constraint
        try:
            # Verificar se há dados existentes
            existing = supabase_admin.table('agent_behavior_patterns').select(
                'pattern_type'
            ).limit(10).execute()
            
            if existing.data:
                existing_types = list(set(r['pattern_type'] for r in existing.data))
                print(f"📊 Tipos existentes no banco: {existing_types}")
            else:
                print("📊 Nenhum padrão existente no banco")
                
        except Exception as e:
            print(f"❌ Erro ao verificar dados existentes: {e}")
    
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()