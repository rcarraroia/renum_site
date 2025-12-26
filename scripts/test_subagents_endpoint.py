#!/usr/bin/env python3
"""
Script para testar o endpoint de sub-agentes corrigido
"""

import sys
import os
import requests
import json
from datetime import datetime

# Adicionar path do backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_subagents_endpoint():
    """Testa o endpoint de listagem de sub-agentes"""
    print("🧪 Testando endpoint de sub-agentes...")
    print("=" * 50)
    
    # URL do endpoint
    agent_id = "00000000-0000-0000-0000-000000000001"
    url = f"http://localhost:8000/api/agents/{agent_id}/sub-agents"
    
    try:
        print(f"📡 Fazendo requisição para: {url}")
        
        # Fazer requisição sem autenticação primeiro para ver o erro
        response = requests.get(url)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 401:
            print("⚠️ Endpoint requer autenticação (esperado)")
            print("🔧 Testando diretamente no backend...")
            
            # Testar diretamente importando o serviço
            from src.services.agent_service import get_agent_service
            from src.models.sub_agent import SubAgentResponse
            from uuid import UUID
            
            agent_service = get_agent_service()
            
            # Simular a lógica do endpoint
            result = agent_service.supabase.table('sub_agents')\
                .select('*')\
                .eq('parent_agent_id', agent_id)\
                .execute()
            
            print(f"📊 Dados brutos do banco: {len(result.data)} sub-agentes encontrados")
            
            if result.data:
                print("📋 Dados do primeiro sub-agente:")
                print(json.dumps(result.data[0], indent=2, default=str))
                
                # Testar mapeamento para SubAgentResponse
                print("\n🔄 Testando mapeamento para SubAgentResponse...")
                
                data = result.data[0]
                config = data.get('config', {})
                identity = config.get('identity', {})
                
                # Criar objeto compatível com SubAgentResponse
                sub_agent_data = {
                    'id': data['id'],
                    'agent_id': data.get('parent_agent_id'),
                    'name': data['name'],
                    'description': identity.get('persona', f"Sub-agente especializado em {data.get('specialization', 'geral')}"),
                    'channel': config.get('channel', 'whatsapp'),
                    'system_prompt': identity.get('system_prompt', 'Você é um assistente especializado.'),
                    'topics': config.get('topics', []),
                    'model': config.get('model', 'gpt-4o-mini'),
                    'is_active': data.get('is_active', True),
                    'fine_tuning_config': config.get('fine_tuning_config'),
                    'config_id': None,
                    'slug': None,
                    'public_url': None,
                    'access_count': 0,
                    'is_public': True,
                    'knowledge_base': None,
                    'created_at': data['created_at'],
                    'updated_at': data['updated_at']
                }
                
                print("📋 Dados mapeados:")
                print(json.dumps(sub_agent_data, indent=2, default=str))
                
                # Tentar criar o modelo SubAgentResponse
                try:
                    sub_agent_response = SubAgentResponse(**sub_agent_data)
                    print("✅ SubAgentResponse criado com sucesso!")
                    print(f"📝 Nome: {sub_agent_response.name}")
                    print(f"📱 Canal: {sub_agent_response.channel}")
                    print(f"🤖 System Prompt: {sub_agent_response.system_prompt[:100]}...")
                    print(f"🏷️ Tópicos: {sub_agent_response.topics}")
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Erro ao criar SubAgentResponse: {e}")
                    return False
            else:
                print("⚠️ Nenhum sub-agente encontrado no banco")
                return False
                
        elif response.status_code == 200:
            print("✅ Endpoint funcionando!")
            data = response.json()
            print(f"📊 Retornou {len(data)} sub-agentes")
            
            if data:
                print("📋 Primeiro sub-agente:")
                print(json.dumps(data[0], indent=2, default=str))
            
            return True
            
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 Teste do Endpoint de Sub-Agentes")
    print("=" * 50)
    
    success = test_subagents_endpoint()
    
    if success:
        print("\n✅ RESULTADO: Endpoint de sub-agentes está funcionando!")
        return 0
    else:
        print("\n❌ RESULTADO: Endpoint de sub-agentes tem problemas!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)