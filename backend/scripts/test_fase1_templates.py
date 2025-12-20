"""
Script de teste para validar Fase 1 - Templates
Testa criação de template, listagem e clonagem
"""
import asyncio
import sys
from pathlib import Path

# Adicionar backend ao path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from src.config.supabase import supabase_admin
from uuid import uuid4


async def test_migration():
    """Verifica se os campos de template foram criados"""
    print("\n=== Testando Migration ===")
    
    try:
        # Verificar se campos existem
        result = supabase_admin.table('agents').select('*').limit(1).execute()
        
        if result.data:
            agent = result.data[0]
            campos_template = [
                'is_template',
                'category',
                'niche',
                'marketplace_visible',
                'available_tools',
                'available_integrations'
            ]
            
            campos_existentes = [campo for campo in campos_template if campo in agent]
            campos_faltando = [campo for campo in campos_template if campo not in agent]
            
            print(f"✅ Campos existentes: {', '.join(campos_existentes)}")
            if campos_faltando:
                print(f"❌ Campos faltando: {', '.join(campos_faltando)}")
                return False
            
            print("✅ Migration executada com sucesso!")
            return True
        else:
            print("⚠️ Nenhum agente no banco para verificar")
            return True
    
    except Exception as e:
        print(f"❌ Erro ao verificar migration: {e}")
        return False


async def test_create_template():
    """Testa criação de um template"""
    print("\n=== Testando Criação de Template ===")
    
    try:
        template_id = uuid4()
        template_data = {
            'id': str(template_id),
            'name': 'Template de Teste - Vendas',
            'description': 'Template para agentes de vendas',
            'channel': 'web',
            'system_prompt': 'Você é um agente de vendas profissional',
            'model': 'gpt-4o-mini',
            'status': 'active',
            'is_template': True,
            'category': 'b2b',
            'niche': 'Vendas',
            'marketplace_visible': True,
            'available_tools': {
                'whatsapp': {'enabled_by_default': True, 'client_configurable': True},
                'email': {'enabled_by_default': False, 'client_configurable': True}
            },
            'config': {
                'model': 'gpt-4o-mini',
                'system_prompt': 'Você é um agente de vendas profissional'
            }
        }
        
        result = supabase_admin.table('agents').insert(template_data).execute()
        
        if result.data:
            print(f"✅ Template criado com sucesso! ID: {template_id}")
            return str(template_id)
        else:
            print("❌ Falha ao criar template")
            return None
    
    except Exception as e:
        print(f"❌ Erro ao criar template: {e}")
        return None


async def test_list_templates():
    """Testa listagem de templates"""
    print("\n=== Testando Listagem de Templates ===")
    
    try:
        result = supabase_admin.table('agents')\
            .select('*')\
            .eq('is_template', True)\
            .eq('marketplace_visible', True)\
            .execute()
        
        if result.data:
            print(f"✅ Encontrados {len(result.data)} templates no marketplace:")
            for template in result.data:
                print(f"  - {template['name']} ({template['category']}) - {template['niche']}")
            return True
        else:
            print("⚠️ Nenhum template encontrado no marketplace")
            return True
    
    except Exception as e:
        print(f"❌ Erro ao listar templates: {e}")
        return False


async def test_clone_template(template_id: str):
    """Testa clonagem de template"""
    print("\n=== Testando Clonagem de Template ===")
    
    try:
        # Buscar template
        template_result = supabase_admin.table('agents')\
            .select('*')\
            .eq('id', template_id)\
            .single()\
            .execute()
        
        if not template_result.data:
            print("❌ Template não encontrado")
            return False
        
        template = template_result.data
        
        # Criar agente clonado
        new_agent_id = uuid4()
        new_agent_data = {
            **template,
            'id': str(new_agent_id),
            'parent_id': template_id,
            'is_template': False,
            'marketplace_visible': False,
            'name': f"{template['name']} - Clonado",
            'status': 'active'
        }
        
        result = supabase_admin.table('agents').insert(new_agent_data).execute()
        
        if result.data:
            print(f"✅ Template clonado com sucesso! Novo ID: {new_agent_id}")
            return str(new_agent_id)
        else:
            print("❌ Falha ao clonar template")
            return None
    
    except Exception as e:
        print(f"❌ Erro ao clonar template: {e}")
        return None


async def cleanup(template_id: str = None, cloned_id: str = None):
    """Limpa dados de teste"""
    print("\n=== Limpando Dados de Teste ===")
    
    try:
        if cloned_id:
            supabase_admin.table('agents').delete().eq('id', cloned_id).execute()
            print(f"✅ Agente clonado removido: {cloned_id}")
        
        if template_id:
            supabase_admin.table('agents').delete().eq('id', template_id).execute()
            print(f"✅ Template de teste removido: {template_id}")
    
    except Exception as e:
        print(f"⚠️ Erro ao limpar dados: {e}")


async def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("TESTE DA FASE 1 - TEMPLATES E MARKETPLACE")
    print("=" * 60)
    
    # 1. Verificar migration
    if not await test_migration():
        print("\n❌ Migration não executada. Execute manualmente via Supabase Dashboard")
        print("SQL: backend/migrations/015_add_template_fields.sql")
        return
    
    # 2. Criar template de teste
    template_id = await test_create_template()
    if not template_id:
        return
    
    # 3. Listar templates
    await test_list_templates()
    
    # 4. Clonar template
    cloned_id = await test_clone_template(template_id)
    
    # 5. Limpar dados de teste
    await cleanup(template_id, cloned_id)
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
    print("\nPróximos passos:")
    print("1. Acessar http://localhost:8081/dashboard/admin/agents/templates")
    print("2. Clicar em 'Criar Novo Template'")
    print("3. Preencher Step 1 com:")
    print("   - Categoria: B2B")
    print("   - Nicho: Vendas")
    print("   - Publicar no Marketplace: ✓")
    print("4. Completar wizard")
    print("5. Verificar template na lista")


if __name__ == "__main__":
    asyncio.run(main())
