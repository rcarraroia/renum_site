#!/usr/bin/env python3
"""
Script para verificar dados dos sub-agentes no banco
"""

import sys
import os
import json

# Adicionar path do backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def check_subagent_data():
    """Verifica dados dos sub-agentes no banco"""
    print("🔍 Verificando dados dos sub-agentes...")
    print("=" * 50)
    
    try:
        from src.services.agent_service import get_agent_service
        
        agent_service = get_agent_service()
        agent_id = "00000000-0000-0000-0000-000000000001"
        
        result = agent_service.supabase.table('sub_agents')\
            .select('*')\
            .eq('parent_agent_id', agent_id)\
            .execute()
        
        print(f"📊 Encontrados {len(result.data)} sub-agentes")
        
        if result.data:
            for i, data in enumerate(result.data):
                print(f"\n📋 Sub-agente {i+1}:")
                print(json.dumps(data, indent=2, default=str))
                
                # Analisar estrutura do config
                config = data.get('config', {})
                print(f"\n🔧 Estrutura do config:")
                print(f"  - Keys: {list(config.keys())}")
                
                if 'identity' in config:
                    identity = config['identity']
                    print(f"  - Identity keys: {list(identity.keys())}")
                    
        else:
            print("⚠️ Nenhum sub-agente encontrado")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_subagent_data()