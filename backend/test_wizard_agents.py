"""
Test script for Wizard with Agents table
Sprint 09 - Fase C validation

Tests that wizard correctly saves to agents table instead of sub_agents.
"""

import sys
import os
from uuid import UUID, uuid4

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.wizard_service import get_wizard_service
from src.config.supabase import supabase_admin


def test_wizard_with_agents():
    """Test wizard operations with agents table"""
    
    print("=" * 60)
    print("TESTE: Wizard com Tabela Agents")
    print("=" * 60)
    
    wizard_service = get_wizard_service()
    
    # Get a test client_id (use first client from database)
    print("\n1. Buscando client_id de teste...")
    clients_result = supabase_admin.table('clients').select('id').limit(1).execute()
    
    if not clients_result.data:
        print("❌ Nenhum client encontrado. Crie um client primeiro.")
        return False
    
    test_client_id = UUID(clients_result.data[0]['id'])
    print(f"✅ Client ID: {test_client_id}")
    
    # Test 1: Create wizard session
    print("\n2. Criando wizard session...")
    try:
        wizard_session = wizard_service.start_wizard(test_client_id)
        wizard_id = wizard_session.id
        print(f"✅ Wizard criado: {wizard_id}")
        print(f"   - Nome: {wizard_session.id}")
        print(f"   - Step atual: {wizard_session.current_step}")
    except Exception as e:
        print(f"❌ Erro ao criar wizard: {e}")
        return False
    
    # Test 2: Verify it was saved in agents table
    print("\n3. Verificando se foi salvo na tabela agents...")
    try:
        agent_result = supabase_admin.table('agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .single()\
            .execute()
        
        if agent_result.data:
            print("✅ Encontrado na tabela agents")
            print(f"   - Status: {agent_result.data['status']}")
            print(f"   - Channel: {agent_result.data['channel']}")
            print(f"   - Template: {agent_result.data['template_type']}")
        else:
            print("❌ NÃO encontrado na tabela agents")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar agents: {e}")
        return False
    
    # Test 3: Verify it was NOT saved in sub_agents table
    print("\n4. Verificando que NÃO foi salvo na tabela sub_agents...")
    try:
        subagent_result = supabase_admin.table('sub_agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .execute()
        
        if not subagent_result.data or len(subagent_result.data) == 0:
            print("✅ Confirmado: NÃO está na tabela sub_agents")
        else:
            print("❌ ERRO: Encontrado na tabela sub_agents (não deveria estar)")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar sub_agents: {e}")
        return False
    
    # Test 4: Save step 1
    print("\n5. Salvando Step 1...")
    try:
        step_1_data = {
            'name': 'Agente Teste Sprint 09',
            'description': 'Agente de teste para validar nova arquitetura',
            'template_type': 'custom',
            'niche': 'teste'
        }
        
        updated_session = wizard_service.save_step(wizard_id, 1, step_1_data)
        print("✅ Step 1 salvo")
        print(f"   - Nome atualizado: {updated_session.step_1_data.name if updated_session.step_1_data else 'N/A'}")
        print(f"   - Step atual: {updated_session.current_step}")
    except Exception as e:
        print(f"❌ Erro ao salvar step 1: {e}")
        return False
    
    # Test 5: Get wizard
    print("\n6. Recuperando wizard...")
    try:
        retrieved_session = wizard_service.get_wizard(wizard_id)
        if retrieved_session:
            print("✅ Wizard recuperado")
            print(f"   - ID: {retrieved_session.id}")
            print(f"   - Step atual: {retrieved_session.current_step}")
            print(f"   - Step 1 data: {'Presente' if retrieved_session.step_1_data else 'Ausente'}")
        else:
            print("❌ Wizard não encontrado")
            return False
    except Exception as e:
        print(f"❌ Erro ao recuperar wizard: {e}")
        return False
    
    # Test 6: List drafts
    print("\n7. Listando drafts do client...")
    try:
        drafts = wizard_service.list_drafts(test_client_id)
        print(f"✅ Encontrados {len(drafts)} draft(s)")
        for draft in drafts:
            print(f"   - {draft.id}: Step {draft.current_step}")
    except Exception as e:
        print(f"❌ Erro ao listar drafts: {e}")
        return False
    
    # Test 7: Delete wizard (cleanup)
    print("\n8. Deletando wizard (cleanup)...")
    try:
        deleted = wizard_service.delete_wizard(wizard_id, force=True)
        if deleted:
            print("✅ Wizard deletado")
        else:
            print("⚠️  Wizard não foi deletado (pode já ter sido removido)")
    except Exception as e:
        print(f"❌ Erro ao deletar wizard: {e}")
        return False
    
    # Test 8: Verify deletion
    print("\n9. Verificando deleção...")
    try:
        agent_result = supabase_admin.table('agents')\
            .select('*')\
            .eq('id', str(wizard_id))\
            .execute()
        
        if not agent_result.data or len(agent_result.data) == 0:
            print("✅ Confirmado: Wizard removido da tabela agents")
        else:
            print("⚠️  Wizard ainda existe na tabela agents")
    except Exception as e:
        print(f"❌ Erro ao verificar deleção: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    print("\nConclusão:")
    print("- Wizard agora salva corretamente na tabela 'agents'")
    print("- Wizard NÃO salva mais na tabela 'sub_agents'")
    print("- Todas as operações CRUD funcionam corretamente")
    print("- Hierarquia clients → agents → sub_agents implementada")
    
    return True


if __name__ == "__main__":
    try:
        success = test_wizard_with_agents()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
