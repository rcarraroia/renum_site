"""
Script de teste para validar API de leads
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.supabase import supabase_admin
from src.models.lead import LeadCreate, LeadUpdate
from src.services.lead_service import lead_service
import asyncio

async def test_leads():
    print("=" * 50)
    print("TESTE: API de Leads")
    print("=" * 50)
    
    # Teste 1: Verificar tabela
    print("\n1. Verificando tabela 'leads' no Supabase...")
    try:
        result = supabase_admin.table("leads").select("*").limit(1).execute()
        print(f"   ✅ Tabela existe! Colunas: {list(result.data[0].keys()) if result.data else 'Vazia'}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Listar leads
    print("\n2. Testando listagem de leads...")
    try:
        leads = await lead_service.get_all(page=1, limit=5)
        print(f"   ✅ Listagem OK! Total: {leads.total}, Itens: {len(leads.items)}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 3: Criar lead
    print("\n3. Testando criação de lead...")
    try:
        test_lead = LeadCreate(
            name="Lead Teste",
            phone="+5511999999999",
            email="teste@example.com",
            source="pesquisa",
            status="novo"
        )
        created = await lead_service.create(test_lead)
        print(f"   ✅ Lead criado! ID: {created.id}")
        test_id = created.id
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 4: Buscar por ID
    print("\n4. Testando busca por ID...")
    try:
        found = await lead_service.get_by_id(test_id)
        print(f"   ✅ Lead encontrado! Nome: {found.name}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 5: Atualizar lead
    print("\n5. Testando atualização...")
    try:
        update_data = LeadUpdate(status="qualificado", score=85)
        updated = await lead_service.update(test_id, update_data)
        print(f"   ✅ Lead atualizado! Status: {updated.status}, Score: {updated.score}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 6: Deletar lead
    print("\n6. Testando deleção...")
    try:
        await lead_service.delete(test_id)
        print(f"   ✅ Lead deletado!")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_leads())
    sys.exit(0 if result else 1)
