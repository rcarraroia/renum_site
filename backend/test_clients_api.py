"""
Script de teste para validar API de clientes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.supabase import supabase_admin
from src.models.client import ClientCreate, ClientUpdate, ContactInfo
from src.services.client_service import client_service
import asyncio

async def test_clients():
    print("=" * 50)
    print("TESTE: API de Clientes")
    print("=" * 50)
    
    # Teste 1: Verificar tabela
    print("\n1. Verificando tabela 'clients' no Supabase...")
    try:
        result = supabase_admin.table("clients").select("*").limit(1).execute()
        print(f"   ✅ Tabela existe! Colunas: {list(result.data[0].keys()) if result.data else 'Vazia'}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Listar clientes
    print("\n2. Testando listagem de clientes...")
    try:
        clients = await client_service.get_all(page=1, limit=5)
        print(f"   ✅ Listagem OK! Total: {clients.total}, Itens: {len(clients.items)}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 3: Criar cliente
    print("\n3. Testando criação de cliente...")
    try:
        test_client = ClientCreate(
            company_name="Empresa Teste LTDA",
            document="12345678000190",
            segment="Tecnologia",
            contact=ContactInfo(
                email="contato@teste.com",
                phone="+5511999999999"
            ),
            status="active"
        )
        created = await client_service.create(test_client)
        print(f"   ✅ Cliente criado! ID: {created.id}")
        test_id = created.id
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 4: Buscar por ID
    print("\n4. Testando busca por ID...")
    try:
        found = await client_service.get_by_id(test_id)
        print(f"   ✅ Cliente encontrado! Nome: {found.company_name}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 5: Atualizar cliente
    print("\n5. Testando atualização...")
    try:
        update_data = ClientUpdate(segment="Serviços", website="https://teste.com")
        updated = await client_service.update(test_id, update_data)
        print(f"   ✅ Cliente atualizado! Segmento: {updated.segment}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 6: Deletar cliente
    print("\n6. Testando deleção...")
    try:
        await client_service.delete(test_id)
        print(f"   ✅ Cliente deletado!")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_clients())
    sys.exit(0 if result else 1)
