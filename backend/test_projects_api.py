"""
Script de teste para validar API de projetos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.config.supabase import supabase_admin
from src.models.project import ProjectCreate, ProjectResponse
from src.services.project_service import project_service
import asyncio

async def test_projects():
    print("=" * 50)
    print("TESTE: API de Projetos")
    print("=" * 50)
    
    # Teste 1: Verificar tabela no Supabase
    print("\n1. Verificando tabela 'projects' no Supabase...")
    try:
        result = supabase_admin.table("projects").select("*").limit(1).execute()
        print(f"   ✅ Tabela existe! Colunas: {list(result.data[0].keys()) if result.data else 'Vazia'}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 2: Listar projetos
    print("\n2. Testando listagem de projetos...")
    try:
        projects = await project_service.get_all(page=1, limit=5)
        print(f"   ✅ Listagem OK! Total: {projects.total}, Itens: {len(projects.items)}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 3: Criar projeto de teste
    print("\n3. Testando criação de projeto...")
    try:
        test_project = ProjectCreate(
            name="Projeto Teste API",
            type="AI Native",
            description="Projeto criado para teste",
            status="Em Andamento",
            progress=0
        )
        created = await project_service.create(test_project)
        print(f"   ✅ Projeto criado! ID: {created.id}")
        test_id = created.id
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 4: Buscar projeto por ID
    print("\n4. Testando busca por ID...")
    try:
        found = await project_service.get_by_id(test_id)
        print(f"   ✅ Projeto encontrado! Nome: {found.name}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 5: Atualizar projeto
    print("\n5. Testando atualização...")
    try:
        from src.models.project import ProjectUpdate
        update_data = ProjectUpdate(progress=50, status="Em Andamento")
        updated = await project_service.update(test_id, update_data)
        print(f"   ✅ Projeto atualizado! Progresso: {updated.progress}%")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    # Teste 6: Deletar projeto
    print("\n6. Testando deleção...")
    try:
        await project_service.delete(test_id)
        print(f"   ✅ Projeto deletado!")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_projects())
    sys.exit(0 if result else 1)
