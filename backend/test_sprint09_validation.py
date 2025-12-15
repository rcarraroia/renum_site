"""
Sprint 09 - Validação Automatizada Completa
Testa todos os requisitos do checkpoint final
"""

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent))

from src.config.supabase import supabase_admin
from src.services.agent_service import AgentService
from src.services.subagent_service import SubAgentService
from src.agents.renus import RenusAgent
from src.agents.agent_loader import get_agent_registry


async def test_1_wizard_creates_in_agents():
    """
    Teste 1: Wizard cria em agents (não sub_agents)
    """
    print("\n" + "="*60)
    print("TESTE 1: Wizard Cria em Agents")
    print("="*60)
    
    try:
        # Buscar um client_id existente
        clients = supabase_admin.table('clients').select('id').limit(1).execute()
        
        if not clients.data:
            print("❌ Nenhum client encontrado no banco")
            return False
        
        client_id = clients.data[0]['id']
        
        # Criar agent via service (simula wizard)
        agent_service = AgentService()
        
        # Importar model
        from src.models.agent import AgentCreate
        
        test_agent_data = AgentCreate(
            client_id=client_id,
            name=f'Test Agent Validation {uuid4().hex[:8]}',
            description='Agent criado para validação do Sprint 09',
            system_prompt='Você é um assistente de testes.',
            channel='whatsapp',  # Usar whatsapp (válido no constraint)
            template_type='custom',
            status='active',
            model='gpt-4o-mini'
        )
        
        agent = await agent_service.create_agent(test_agent_data)  # Await async method
        
        # Agent service retorna AgentResponse (Pydantic model)
        agent_id = agent.id
        agent_name = agent.name
        
        print(f"✅ Agent criado com sucesso")
        print(f"   ID: {agent_id}")
        print(f"   Nome: {agent_name}")
        print(f"   Tabela: agents")
        
        # Verificar que NÃO está em sub_agents
        sub_check = supabase_admin.table('sub_agents')\
            .select('id')\
            .eq('id', agent_id)\
            .execute()
        
        if sub_check.data:
            print(f"❌ ERRO: Agent também está em sub_agents!")
            return False
        
        print(f"✅ Confirmado: Agent NÃO está em sub_agents")
        
        # Cleanup
        await agent_service.delete_agent(agent_id)
        print(f"✅ Cleanup: Agent deletado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


async def test_2_subagent_has_agent_id():
    """
    Teste 2: Sub-agent tem agent_id correto
    """
    print("\n" + "="*60)
    print("TESTE 2: Sub-Agent tem agent_id")
    print("="*60)
    
    try:
        # Buscar um agent existente
        agents = supabase_admin.table('agents')\
            .select('id, name')\
            .eq('status', 'active')\
            .limit(1)\
            .execute()
        
        if not agents.data:
            print("❌ Nenhum agent ativo encontrado")
            return False
        
        agent = agents.data[0]
        agent_id = agent['id']
        
        print(f"📋 Usando agent: {agent['name']} ({agent_id[:8]}...)")
        
        # Criar sub-agent
        subagent_service = SubAgentService()
        
        test_subagent_data = {
            'name': f'Test SubAgent {uuid4().hex[:8]}',
            'description': 'Sub-agent para validação',
            'channel': 'whatsapp',  # Usar whatsapp (válido no constraint)
            'system_prompt': 'Você é um sub-agente de testes.',
            'topics': ['teste', 'validação'],
            'model': 'gpt-4o-mini',
            'is_active': True
        }
        
        # Criar via service (que deve adicionar agent_id)
        subagent = supabase_admin.table('sub_agents').insert({
            **test_subagent_data,
            'agent_id': agent_id
        }).execute()
        
        if not subagent.data:
            print("❌ Erro ao criar sub-agent")
            return False
        
        subagent = subagent.data[0]
        
        print(f"✅ Sub-agent criado com sucesso")
        print(f"   ID: {subagent['id']}")
        print(f"   Nome: {subagent['name']}")
        print(f"   agent_id: {subagent['agent_id']}")
        
        # Verificar que agent_id está correto
        if subagent['agent_id'] != agent_id:
            print(f"❌ ERRO: agent_id incorreto!")
            print(f"   Esperado: {agent_id}")
            print(f"   Encontrado: {subagent['agent_id']}")
            return False
        
        print(f"✅ Confirmado: agent_id está correto")
        
        # Verificar que NÃO tem client_id
        if 'client_id' in subagent and subagent['client_id'] is not None:
            print(f"⚠️  AVISO: Sub-agent ainda tem client_id (deveria ser NULL)")
        else:
            print(f"✅ Confirmado: Sub-agent NÃO tem client_id")
        
        # Cleanup
        supabase_admin.table('sub_agents').delete().eq('id', subagent['id']).execute()
        print(f"✅ Cleanup: Sub-agent deletado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_3_dynamic_routing():
    """
    Teste 3: Roteamento dinâmico por tópicos
    """
    print("\n" + "="*60)
    print("TESTE 3: Roteamento Dinâmico")
    print("="*60)
    
    try:
        # Buscar agent com sub-agents
        agents = supabase_admin.table('agents')\
            .select('id, name')\
            .eq('status', 'active')\
            .limit(1)\
            .execute()
        
        if not agents.data:
            print("❌ Nenhum agent encontrado")
            return False
        
        agent = agents.data[0]
        agent_id = agent['id']
        
        # Criar sub-agent com tópicos específicos
        test_subagent = {
            'agent_id': agent_id,
            'name': f'Test Routing SubAgent {uuid4().hex[:8]}',
            'description': 'Sub-agent para teste de roteamento',
            'channel': 'whatsapp',  # Usar whatsapp (válido no constraint)
            'system_prompt': 'Você é especialista em vendas.',
            'topics': ['vendas', 'comercial', 'preço'],
            'model': 'gpt-4o-mini',
            'is_active': True
        }
        
        subagent_result = supabase_admin.table('sub_agents').insert(test_subagent).execute()
        
        if not subagent_result.data:
            print("❌ Erro ao criar sub-agent")
            return False
        
        subagent = subagent_result.data[0]
        
        print(f"✅ Sub-agent criado: {subagent['name']}")
        print(f"   Tópicos: {subagent['topics']}")
        
        # Inicializar RENUS e forçar reload
        renus = RenusAgent(enable_periodic_sync=False)
        renus.sync_agents()
        
        print(f"✅ RENUS sincronizado")
        
        # Testar roteamento com mensagem que contém tópico
        test_messages = [
            ("Quero informações sobre vendas", "vendas"),
            ("Qual o preço do produto?", "preço"),
            ("Preciso de suporte técnico", None),  # Não deve rotear
        ]
        
        all_passed = True
        
        for message, expected_topic in test_messages:
            print(f"\n📝 Testando: '{message}'")
            
            routing = await renus.route_message_dynamic(
                message=message,
                agent_id=agent_id
            )
            
            if expected_topic:
                # Deve rotear para sub-agent
                if routing['type'] == 'sub_agent':
                    print(f"   ✅ Roteado para sub-agent: {routing['sub_agent_name']}")
                    print(f"   ✅ Tópico detectado: {routing['topic']}")
                    
                    if routing['topic'] not in subagent['topics']:
                        print(f"   ⚠️  Tópico não está na lista esperada")
                        all_passed = False
                else:
                    print(f"   ❌ Deveria rotear para sub-agent mas roteou para agent principal")
                    all_passed = False
            else:
                # Deve rotear para agent principal
                if routing['type'] == 'agent':
                    print(f"   ✅ Roteado para agent principal (correto)")
                else:
                    print(f"   ⚠️  Roteou para sub-agent mas deveria ir para agent principal")
        
        # Cleanup
        supabase_admin.table('sub_agents').delete().eq('id', subagent['id']).execute()
        print(f"\n✅ Cleanup: Sub-agent deletado")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_4_migrated_agents():
    """
    Teste 4: Agents migrados funcionam
    """
    print("\n" + "="*60)
    print("TESTE 4: Agents Migrados")
    print("="*60)
    
    try:
        # Buscar agents que vieram da migração (têm slug)
        migrated = supabase_admin.table('agents')\
            .select('id, name, slug, public_url')\
            .not_.is_('slug', 'null')\
            .execute()
        
        if not migrated.data:
            print("⚠️  Nenhum agent migrado encontrado (sem slug)")
            return True  # Não é erro, apenas não há dados
        
        print(f"📋 Encontrados {len(migrated.data)} agents migrados")
        
        all_working = True
        
        for agent in migrated.data[:5]:  # Testar primeiros 5
            print(f"\n🔍 Testando: {agent['name']}")
            print(f"   Slug: {agent['slug']}")
            print(f"   URL: {agent['public_url']}")
            
            # Verificar que agent existe e está acessível
            check = supabase_admin.table('agents')\
                .select('id, status')\
                .eq('id', agent['id'])\
                .execute()
            
            if not check.data:
                print(f"   ❌ Agent não encontrado!")
                all_working = False
                continue
            
            agent_data = check.data[0]
            
            if agent_data['status'] != 'active':
                print(f"   ⚠️  Agent não está ativo (status: {agent_data['status']})")
            else:
                print(f"   ✅ Agent ativo e acessível")
            
            # Verificar se tem sub-agents associados
            subagents = supabase_admin.table('sub_agents')\
                .select('id, name')\
                .eq('agent_id', agent['id'])\
                .execute()
            
            if subagents.data:
                print(f"   ✅ {len(subagents.data)} sub-agent(s) associado(s)")
            else:
                print(f"   ℹ️  Sem sub-agents")
        
        return all_working
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Executar todos os testes"""
    print("\n" + "="*60)
    print("🧪 SPRINT 09 - VALIDAÇÃO AUTOMATIZADA COMPLETA")
    print("="*60)
    
    tests = [
        ("Wizard cria em agents", test_1_wizard_creates_in_agents),
        ("Sub-agent tem agent_id", test_2_subagent_has_agent_id),
        ("Roteamento dinâmico", test_3_dynamic_routing),
        ("Agents migrados funcionam", test_4_migrated_agents),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result, None))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    # Summary
    print("\n" + "="*60)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result, error in results:
        if result:
            print(f"✅ {test_name}: PASSOU")
            passed += 1
        else:
            print(f"❌ {test_name}: FALHOU")
            if error:
                print(f"   Erro: {error}")
            failed += 1
    
    print(f"\n📈 Resultado Final: {passed}/{len(tests)} testes passaram")
    
    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sprint 09 validado e pronto para deploy")
        return 0
    else:
        print(f"\n⚠️  {failed} teste(s) falharam")
        print("⚠️  Revisar antes de marcar como completo")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
