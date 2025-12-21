#!/usr/bin/env python3
"""
Script para testar wizard end-to-end
MISSÃO: Correção Wizard - PASSO 2
"""

import requests
import json
import time
from datetime import datetime

BACKEND_URL = "http://localhost:8000"

def testar_backend_health():
    """Testa se backend está rodando"""
    print("🔍 1. Testando saúde do backend...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está rodando")
            return True
        else:
            print(f"⚠️ Backend respondeu com status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend não está acessível: {e}")
        return False

def testar_wizard_start():
    """Testa início do wizard"""
    print("\n🔍 2. Testando início do wizard...")
    
    try:
        data = {
            "client_id": None,
            "category": "b2c"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/agents/wizard/start",
            json=data,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            wizard_data = response.json()
            wizard_id = wizard_data.get('id')
            print(f"✅ Wizard iniciado com sucesso")
            print(f"   Wizard ID: {wizard_id}")
            return True, wizard_id
        else:
            print(f"❌ Erro ao iniciar wizard: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Erro testando wizard start: {e}")
        return False, None

def testar_wizard_step(wizard_id, step_number, step_data):
    """Testa salvamento de um step"""
    print(f"\n🔍 3.{step_number}. Testando Step {step_number}...")
    
    try:
        response = requests.put(
            f"{BACKEND_URL}/api/agents/wizard/{wizard_id}/step/{step_number}",
            json=step_data,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Step {step_number} salvo com sucesso")
            return True
        else:
            print(f"❌ Erro no Step {step_number}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro testando Step {step_number}: {e}")
        return False

def testar_wizard_publish(wizard_id):
    """Testa publicação do agente"""
    print(f"\n🔍 4. Testando publicação do agente...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/agents/wizard/{wizard_id}/publish",
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            agent_data = response.json()
            agent_id = agent_data.get('id')
            print(f"✅ Agente publicado com sucesso")
            print(f"   Agent ID: {agent_id}")
            return True, agent_id
        else:
            print(f"❌ Erro ao publicar agente: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Erro testando publicação: {e}")
        return False, None

def validar_agente_no_banco(agent_id):
    """Valida se agente foi criado no banco"""
    print(f"\n🔍 5. Validando agente no banco...")
    
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    connection_string = "postgresql://postgres:BD5yEMQ9iDMOkeGW@db.vhixvzaxswphwoymdhgg.supabase.co:5432/postgres"
    
    try:
        conn = psycopg2.connect(connection_string)
        
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT id, name, status, slug, created_at 
                FROM agents 
                WHERE id = %s
            """, (agent_id,))
            
            agent = cursor.fetchone()
            
            if agent:
                print(f"✅ Agente encontrado no banco:")
                print(f"   ID: {agent['id']}")
                print(f"   Nome: {agent['name']}")
                print(f"   Status: {agent['status']}")
                print(f"   Slug: {agent['slug']}")
                print(f"   Criado em: {agent['created_at']}")
                conn.close()
                return True
            else:
                print(f"❌ Agente não encontrado no banco")
                conn.close()
                return False
                
    except Exception as e:
        print(f"❌ Erro validando no banco: {e}")
        return False

def main():
    print("🎯 MISSÃO: Correção Wizard - PASSO 2")
    print("Objetivo: Testar wizard end-to-end via API")
    print("Tempo estimado: 1 hora")
    print("=" * 60)
    
    # 1. Testar backend
    if not testar_backend_health():
        print("\n❌ TESTE FALHOU - Backend não está rodando")
        print("🔧 Execute: docker-compose up -d backend")
        return False
    
    # 2. Iniciar wizard
    success, wizard_id = testar_wizard_start()
    if not success:
        print("\n❌ TESTE FALHOU - Não foi possível iniciar wizard")
        print("🚨 BUG ENCONTRADO: Endpoint /wizard/start com erro")
        return False
    
    # 3. Testar steps
    print("\n📋 Testando todos os 6 steps...")
    
    steps_data = [
        {
            "step": 1,
            "data": {
                "agent_type": "template",
                "category": "b2c",
                "niche": "odontologia",
                "marketplace_visible": False
            }
        },
        {
            "step": 2,
            "data": {
                "name": "Agente Teste Wizard",
                "description": "Agente criado para testar wizard end-to-end",
                "template_type": "clinica"
            }
        },
        {
            "step": 3,
            "data": {
                "personality": "professional",
                "tone_formal": 80,
                "tone_direct": 60,
                "system_prompt": "Você é um assistente profissional para clínicas odontológicas.",
                "custom_instructions": "Seja sempre educado e prestativo."
            }
        },
        {
            "step": 4,
            "data": {
                "standard_fields": {
                    "name": {"enabled": True, "required": True},
                    "email": {"enabled": True, "required": False},
                    "phone": {"enabled": True, "required": True}
                },
                "custom_fields": []
            }
        },
        {
            "step": 5,
            "data": {
                "channels": ["whatsapp", "web"],
                "model": "gpt-4o-mini",
                "integrations": {}
            }
        },
        {
            "step": 6,
            "data": {
                "ready_to_publish": True
            }
        }
    ]
    
    bugs_encontrados = []
    
    for step_info in steps_data:
        step_num = step_info["step"]
        step_data = step_info["data"]
        
        if not testar_wizard_step(wizard_id, step_num, step_data):
            bug_msg = f"Step {step_num} falhou"
            bugs_encontrados.append(bug_msg)
            print(f"🚨 BUG ENCONTRADO: {bug_msg}")
            # REGRA: Se aparecer bug, PARAR e reportar
            break
    
    if bugs_encontrados:
        print("\n" + "=" * 60)
        print("❌ TESTE FALHOU - BUGS ENCONTRADOS")
        print("=" * 60)
        print(f"Total de bugs: {len(bugs_encontrados)}")
        for i, bug in enumerate(bugs_encontrados, 1):
            print(f"{i}. {bug}")
        print("\n🚨 REGRA: Não tentar corrigir bugs além do 'status'")
        print("📋 RECOMENDAÇÃO: Migrar para Agent Builder")
        return False
    
    # 4. Publicar agente
    success, agent_id = testar_wizard_publish(wizard_id)
    if not success:
        print("\n❌ TESTE FALHOU - Não foi possível publicar agente")
        print("🚨 BUG ENCONTRADO: Endpoint /wizard/publish com erro")
        bugs_encontrados.append("Publicação falhou")
        return False
    
    # 5. Validar no banco
    if not validar_agente_no_banco(agent_id):
        print("\n❌ TESTE FALHOU - Agente não foi criado no banco")
        bugs_encontrados.append("Agente não persistiu no banco")
        return False
    
    # SUCESSO!
    print("\n" + "=" * 60)
    print("🎉 TESTE PASSOU - WIZARD 100% FUNCIONAL!")
    print("=" * 60)
    print("✅ Backend rodando")
    print("✅ Wizard iniciado")
    print("✅ Todos os 6 steps funcionaram")
    print("✅ Agente publicado")
    print("✅ Agente criado no banco")
    print(f"\n📊 Agente criado: {agent_id}")
    print(f"📊 Wizard usado: {wizard_id}")
    print("\n🔄 PRÓXIMO PASSO: Testar agente via interface web")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)